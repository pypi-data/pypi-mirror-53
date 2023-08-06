"""
Searches notebooks for search term using a sql query, and calls the display function
"""


def search_notebook(args, library_db, current_scene_db, query_start, query_end):
    """searches and displays loaded notebooks"""
    from src.praxxis.sqlite import sqlite_notebook
    from src.praxxis.display import display_notebook

    search_term = args.term
    notebooks = sqlite_notebook.search_notebooks(library_db, search_term, query_start, query_end)
    display_notebook.display_search(search_term, notebooks)
    sqlite_notebook.write_list(current_scene_db, notebooks)
    return notebooks
