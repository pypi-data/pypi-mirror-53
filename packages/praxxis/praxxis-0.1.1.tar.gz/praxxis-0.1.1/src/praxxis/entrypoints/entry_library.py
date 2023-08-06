"""
This file handles the library functions of the CLI.
"""

from src.praxxis.util.roots import _library_root
from src.praxxis.util.roots import _library_db
from src.praxxis.util.roots import _git_root
from src.praxxis.util.roots import _query_start
from src.praxxis.util.roots import _query_end


def init_library(library_root = _library_root, 
                 library_db = _library_db):
    """handles the initialization of the library dbs and directories"""
    import os
    from src.praxxis.sqlite import sqlite_init
    from src.praxxis.display import display_library
    
    os.mkdir(library_root)
    display_library.display_init_libraries_folder(library_root)
    sqlite_init.init_library_db(library_db)
    display_library.display_init_libraries_db(library_db)


def add_library(arg,
                library_db = _library_db,
                git_root = _git_root):
    """handles adding a library"""
    from src.praxxis.library import add_library

    
    add_library.add_library(arg, library_db, git_root)


def remove_library(arg, 
                   library_db = _library_db,
                   query_start = _query_start,
                   query_end = _query_end,): 
    """handles removing a library"""
    from src.praxxis.library import remove_library

    remove_library.remove_library(arg, library_db, query_start, query_end)


def list_library(arg, 
                 library_db = _library_db,
               query_start = _query_start,
                query_end = _query_end):
    """handles listing loaded libraries"""
    from src.praxxis.library import list_library

    list_library.list_library(library_db,query_start, query_end)


def sync_library(arg, 
                 library_root = _library_root,
                 library_db = _library_db):
    """handles loading libraries"""
    from src.praxxis.library import sync_library

    sync_library.sync_library(library_root, library_db)
