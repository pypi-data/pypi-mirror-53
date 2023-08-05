"""A home for common data load nodes"""

from copy import deepcopy
import csv
from email.message import EmailMessage
import shutil
import sqlite3
import tempfile

import pandas as pd
from pandas.io.common import get_filepath_or_buffer
import requests
from tlbx import st, pp, create_email, send_email, sqlformat

from glide.core import Node, SQLNode, PandasSQLNode
from glide.sql_utils import (
    TemporaryTable,
    SQLiteTemporaryTable,
    get_bulk_replace,
    get_bulk_statement,
    get_temp_table,
)
from glide.utils import (
    dbg,
    warn,
    save_excel,
    find_class_in_dict,
    get_class_list_docstring,
)


class Logger(Node):
    """Simple logging node"""

    def run(self, item):
        """Pretty print the item and then push"""
        print("---- %s ----" % self.name)
        pp(item)
        self.push(item)


# -------- Pandas Loaders


class DataFrameCSVLoader(Node):
    """Load data into a CSV from a Pandas DataFrame"""

    def begin(self):
        """Initialize state for CSV writing"""
        self.wrote_header = False

    def run(self, df, f, push_file=False, dry_run=False, **kwargs):
        """Use Pandas to_csv to output a DataFrame

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame to load to a CSV
        f : file or buffer
            File to write the DataFrame to
        push_file : bool, optional
            If true, push the file forward instead of the data
        dry_run : bool, optional
            If true, skip actually loading the data
        **kwargs
            Keyword arguments passed to DataFrame.to_csv

        """
        if "header" not in kwargs:
            kwargs["header"] = not self.wrote_header
            if not self.wrote_header:
                self.wrote_header = True

        if dry_run:
            warn("dry_run=True, skipping load in %s.run" % self.__class__.__name__)
        else:
            df.to_csv(f, **kwargs)

        if push_file:
            self.push(f)
        else:
            self.push(df)

    def end(self):
        """Reset state in case the node gets reused"""
        self.wrote_header = False


class DataFrameExcelLoader(Node):
    """Load data into an Excel file from a Pandas DataFrame"""

    def run(self, df_or_dict, f, push_file=False, dry_run=False, **kwargs):
        """Use Pandas to_excel to output a DataFrame

        Parameters
        ----------
        df_or_dict
            DataFrame or dict of DataFrames to load to an Excel file. In the
            case of a dict the keys will be the sheet names.
        f : file or buffer
            File to write the DataFrame to
        push_file : bool, optional
            If true, push the file forward instead of the data
        dry_run : bool, optional
            If true, skip actually loading the data
        **kwargs
            Keyword arguments passed to DataFrame.to_excel

        """

        if dry_run:
            warn("dry_run=True, skipping load in %s.run" % self.__class__.__name__)
        else:
            if isinstance(df_or_dict, dict):
                with pd.ExcelWriter(f) as writer:
                    for sheet_name, df in df_or_dict.items():
                        df.to_excel(writer, sheet_name=sheet_name)
            else:
                df_or_dict.to_excel(f, **kwargs)

        if push_file:
            self.push(f)
        else:
            self.push(df_or_dict)


class DataFrameSQLLoader(PandasSQLNode):
    """Load data into a SQL db from a Pandas DataFrame"""

    def run(self, df, conn, table, push_table=False, dry_run=False, **kwargs):
        """Use Pandas to_sql to output a DataFrame

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame to load to a SQL table
        conn
            Database connection
        table : str
            Name of a table to write the data to
        push_table : bool, optional
            If true, push the table forward instead of the data
        dry_run : bool, optional
            If true, skip actually loading the data
        **kwargs
            Keyword arguments passed to DataFrame.to_sql

        """
        if dry_run:
            warn("dry_run=True, skipping load in %s.run" % self.__class__.__name__)
        else:
            df.to_sql(table, conn, **kwargs)

        if push_table:
            self.push(table)
        else:
            self.push(df)


class DataFrameSQLTempLoader(PandasSQLNode):
    """Load data into a SQL temp table from a Pandas DataFrame"""

    def run(self, df, conn, schema=None, dry_run=False, **kwargs):
        """Use Pandas to_sql to output a DataFrame to a temporary table. Push a
        reference to the temp table forward.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame to load to a SQL table
        conn
            Database connection
        schema : str, optional
            schema to create the temp table in
        dry_run : bool, optional
            If true, skip actually loading the data
        **kwargs
            Keyword arguments passed to DataFrame.to_sql

        """
        assert not isinstance(
            conn, sqlite3.Connection
        ), "sqlite3 connections not supported due to bug in Pandas' has_table()?"

        table = get_temp_table(conn, df, schema=schema, create=True)
        if dry_run:
            warn("dry_run=True, skipping load in %s.run" % self.__class__.__name__)
        else:
            df.to_sql(table.name, conn, if_exists="append", **kwargs)

        self.push(table.name)


# -------- Row-based Loaders


class RowCSVLoader(Node):
    """Load data into a CSV using DictWriter"""

    def begin(self):
        """Initialize state for CSV writing"""
        self.writer = None

    def run(self, rows, f, push_file=False, dry_run=False, **kwargs):
        """Use DictWriter to output dict rows to a CSV.

        Parameters
        ----------
        rows
            Iterable of rows to load to a CSV
        f : file or buffer
            File to write rows to
        push_file : bool, optional
            If true, push the file forward instead of the data
        dry_run : bool, optional
            If true, skip actually loading the data
        **kwargs
            Keyword arguments passed to csv.DictWriter

        """
        close = False
        fo = f
        if isinstance(f, str):
            fo = open(f, "w")
            close = True

        try:
            if dry_run:
                warn("dry_run=True, skipping load in %s.run" % self.__class__.__name__)
            else:
                if not self.writer:
                    self.writer = csv.DictWriter(
                        fo, fieldnames=rows[0].keys(), **kwargs
                    )
                    self.writer.writeheader()
                self.writer.writerows(rows)
        finally:
            if close:
                fo.close()

        if push_file:
            self.push(f)
        else:
            self.push(rows)

    def end(self):
        """Reset state in case the node gets reused"""
        self.writer = None


class RowExcelLoader(Node):
    """Load data into an Excel file using pyexcel"""

    def run(
        self,
        rows,
        f,
        dict_rows=False,
        sheet_name="Sheet1",
        push_file=False,
        dry_run=False,
        **kwargs
    ):
        """Use DictWriter to output dict rows to a CSV.

        Parameters
        ----------
        rows
            Iterable of rows to load to an Excel file, or a dict of
            sheet_name->iterable for multi-sheet loads.
        f : file or buffer
            File to write rows to
        dict_rows : bool, optional
            If true the rows of each sheet will be converted from dicts to lists
        sheet_name : str, optional
            Sheet name to use if input is an iterable of rows. Unused otherwise.
        push_file : bool, optional
            If true, push the file forward instead of the data
        dry_run : bool, optional
            If true, skip actually loading the data
        **kwargs
            Keyword arguments passed to pyexcel

        """
        data = rows
        if not isinstance(rows, dict):
            # Setup as a single sheet
            data = {sheet_name: rows}

        if dict_rows:
            for sheet_name, sheet_data in data.items():
                header = [list(sheet_data[0].keys())]
                data[sheet_name] = header + [list(x.values()) for x in sheet_data]

        if dry_run:
            warn("dry_run=True, skipping load in %s.run" % self.__class__.__name__)
        else:
            save_excel(f, data, **kwargs)

        if push_file:
            self.push(f)
        else:
            self.push(rows)


class RowSQLLoader(SQLNode):
    """Generic SQL loader"""

    def run(
        self,
        rows,
        conn,
        table,
        cursor=None,
        commit=True,
        stmt_type="REPLACE",
        odku=False,
        push_table=True,
        dry_run=False,
    ):
        """Form SQL statement and use bulk execute to write rows to table

        Parameters
        ----------
        rows
            Iterable of rows to load to the table
        conn
            Database connection
        table : str
            Name of a table to write the data to
        cursor : optional
            Database connection cursor
        commit : bool, optional
            If true and conn has a commit method, call conn.commit
        stmt_type : str, optional
            Type of SQL statement to use (REPLACE, INSERT, etc.). **Note:** Backend
            support for this varies.
        odku : bool or list, optional
            If true, add ON DUPLICATE KEY UPDATE clause for all columns. If a
            list then only add it for the specified columns. **Note:** Backend
            support for this varies.
        push_table : bool
            If true, push the table forward instead of the data
        dry_run : bool, optional
            If true, skip actually loading the data

        """
        sql = self.get_bulk_statement(conn, stmt_type, table, rows, odku=odku)
        dbg("Loading %d rows\n%s" % (len(rows), sqlformat(sql)), indent="label")

        if dry_run:
            warn("dry_run=True, skipping load in %s.run" % self.__class__.__name__)
        else:
            if not cursor:
                cursor = self.get_sql_executor(conn)
            self.sql_executemany(conn, cursor, sql, rows)
            if commit and hasattr(conn, "commit"):
                conn.commit()

        if push_table:
            self.push(table)
        else:
            self.push(rows)


class RowSQLTempLoader(SQLNode):
    """Generic SQL temp table loader"""

    def run(self, rows, conn, cursor=None, schema=None, commit=True, dry_run=False):
        """Create and bulk load a temp table

        Parameters
        ----------
        rows
            Iterable of rows to load to the table
        conn
            Database connection
        cursor : optional
            Database connection cursor
        schema : str, optional
            Schema to create temp table in
        commit : bool, optional
            If true and conn has a commit method, call conn.commit
        dry_run : bool, optional
            If true, skip actually loading the data

        """
        table = get_temp_table(conn, rows, create=True, schema=schema)
        sql = self.get_bulk_statement(conn, "REPLACE", table.name, rows)
        dbg("Loading %d rows\n%s" % (len(rows), sqlformat(sql)), indent="label")

        if dry_run:
            warn("dry_run=True, skipping load in %s.run" % self.__class__.__name__)
        else:
            if not cursor:
                cursor = self.get_sql_executor(conn)
            self.sql_executemany(conn, cursor, sql, rows)
            if commit and hasattr(conn, "commit"):
                conn.commit()

        self.push(table.name)


# -------- Other Loaders


class FileLoader(Node):
    """Load raw content to a file"""

    def run(self, data, f, open_flags="w", push_file=False, dry_run=False):
        """Load raw data to a file or buffer

        Parameters
        ----------
        data
            Data to write to file
        f : file path or buffer
            File path or buffer to write
        open_flags : str, optional
            Flags to pass to open() if f is not already an opened buffer
        push_file : bool
            If true, push the file forward instead of the data
        dry_run : bool, optional
            If true, skip actually loading the data

        """
        fo, encoding, compression, should_close = get_filepath_or_buffer(f)
        close = False or should_close
        decode = False
        if isinstance(fo, str):
            fo = open(fo, open_flags)
            close = True

        try:
            if dry_run:
                warn("dry_run=True, skipping load in %s.run" % self.__class__.__name__)
            else:
                fo.write(data)
        finally:
            if close:
                try:
                    fo.close()
                except ValueError:
                    pass

        if push_file:
            self.push(f)
        else:
            self.push(data)


class URLLoader(Node):
    """Load data to URL with requests"""

    def run(
        self,
        data,
        url,
        data_param="data",
        session=None,
        raise_for_status=True,
        dry_run=False,
        **kwargs
    ):
        """Load data to URL using requests and push response.content. The url maybe be
        a string (POST that url) or a dictionary of args to requests.request:

        http://2.python-requests.org/en/master/api/?highlight=get#requests.request

        Parameters
        ----------
        data
            Data to load to the URL
        url : str or dict
            If str, a URL to POST to. If a dict, args to requets.request
        data_param : str, optional
            parameter to stuff data in when calling requests methods
        session : optional
            A requests Session to use to make the request
        raise_for_status : bool, optional
            Raise exceptions for bad response status
        dry_run : bool, optional
            If true, skip actually loading the data
        **kwargs
            Keyword arguments to pass to the request method. If a dict is
            passed for the url parameter it overrides values here.

        """
        requestor = requests
        if session:
            requestor = session

        if dry_run:
            warn("dry_run=True, skipping load in %s.run" % self.__class__.__name__)
        else:
            if isinstance(url, str):
                assert not (
                    "data" in kwargs or "json" in kwargs
                ), "Overriding data/json params is not allowed"
                kwargs[data_param] = data
                resp = requestor.post(url, **kwargs)
            elif isinstance(url, dict):
                kwargs_copy = deepcopy(kwargs)
                kwargs_copy.update(url)
                assert not (
                    "data" in kwargs_copy or "json" in kwargs_copy
                ), "Overriding data/json params is not allowed"
                kwargs_copy[data_param] = data
                resp = requestor.request(**kwargs_copy)
            else:
                assert False, "Input url must be a str or dict type, got %s" % type(url)

            if raise_for_status:
                resp.raise_for_status()

        self.push(data)


class EmailLoader(Node):
    """Load data to email via SMTP"""

    def run(
        self,
        data,
        frm=None,
        to=None,
        subject=None,
        body=None,
        html=None,
        attach_as="attachment",
        attachment_name=None,
        formatter=None,
        client=None,
        host=None,
        port=None,
        username=None,
        password=None,
        dry_run=False,
    ):
        """Load data to email via SMTP.

        Parameters
        ----------
        data
            EmailMessage or data to send. If the latter, the message will be
            created from the other node arguments.
        frm : str, optional
            The from email address
        to : str or list, optional
            A str or list of destination email addresses
        subject : str, optional
            The email subject
        body : str, optional
            The email text body
        html : str, optional
            The email html body
        attach_as : str
            Where to put the data in the email message if building the message
            from node arguments. Options: attachment, body, html.
        attachment_name: str, optional
            The file name to write the data to when attaching data to the
            email. The file extension will be used to infer the mimetype of
            the attachment. This should not be a full path as a temp directory
            will be created for this.
        formatter : callable
            A function to format and return a string from the input data if
            attach_as is set to "body" or "html".
        client : optional
            A connected smtplib.SMTP client
        host : str, optional
            The SMTP host to connect to if no client is provided
        port : int, optional
            The SMTP port to connect to if no client is provided
        username : str, optional
            The SMTP username for login if no client is provided
        password : str, optional
            The SMTP password for login if no client is provided
        dry_run : bool, optional
            If true, skip actually loading the data

        """

        if isinstance(data, EmailMessage):
            msg = data
        else:
            # Assume its data that needs to be converted to attachments and sent
            assert (
                frm and to and subject
            ), "Node context must have frm/to/subject set to create an email msg"
            assert isinstance(
                data, str
            ), "data must be passed as raw str content, got %s" % type(data)

            attachments = None
            tmpdir = None

            if attach_as == "attachment":
                assert (
                    attachment_name
                ), "Must specify an attachment_name when attach_as = attachment"
                tmpdir = tempfile.TemporaryDirectory()
                filename = tmpdir.name + "/" + attachment_name
                with open(filename, "w") as f:
                    f.write(data)
                attachments = [filename]
            else:
                fmt_data = formatter(data) if formatter else data
                if attach_as == "body":
                    body = (body or "") + fmt_data
                elif attach_as == "html":
                    html = (html or "") + fmt_data
                else:
                    assert False, (
                        "Invalid attach_as value: %s, options: attachment, body, html"
                        % attach_as
                    )

            msg = create_email(
                frm, to, subject, body=body, html=html, attachments=attachments
            )

            if tmpdir:
                tmpdir.cleanup()

        if dry_run:
            warn("dry_run=True, skipping load in %s.run" % self.__class__.__name__)
        else:
            dbg("Sending msg %s to %s" % (msg["Subject"], msg["To"]))
            send_email(
                msg,
                client=client,
                host=host,
                port=port,
                username=username,
                password=password,
            )

        self.push(data)


node_names = find_class_in_dict(Node, locals(), "Load")
if node_names:
    __doc__ = __doc__ + get_class_list_docstring("Nodes", node_names)
