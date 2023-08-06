"""
This file contains the sqlite functions for notebooks
"""


def list_notebooks(library_db, query_start, query_end):
    """lists all loaded notebooks"""
    from src.praxxis.sqlite import connection

    conn = connection.create_connection(library_db)
    cur = conn.cursor()
    list_libraries = 'SELECT Notebook, Path, Library, RawUrl FROM "Notebooks" LIMIT ?, ?'
    cur.execute(list_libraries, (query_start, query_end))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_notebook(library_db, notebook, library = None):
    """returns a specific notebook"""
    from src.praxxis.sqlite import connection
    from src.praxxis.util import error

    conn = connection.create_connection(library_db)
    cur = conn.cursor()
    if not library is None:
        get_notebook = 'SELECT * FROM "Notebooks" WHERE Notebook = ? AND Library = ?'
        cur.execute(get_notebook, (notebook, library))
    else:
        get_notebook = 'SELECT * FROM "Notebooks" WHERE Notebook = ?'
        cur.execute(get_notebook, (notebook,))

    conn.commit()
    rows = cur.fetchall()
    conn.close()
    if rows == []:
        raise error.NotebookNotFoundError(notebook)
    return rows


def get_notebook_by_ord(current_scene_db, ordinal):
    """Returns list item referenced by input ordinal"""
    from src.praxxis.sqlite import connection
    from src.praxxis.util import error
    conn = connection.create_connection(current_scene_db)
    cur = conn.cursor()
    query = 'SELECT Notebook, Library FROM NotebookList WHERE ID = ? LIMIT 0, 1'
    cur.execute(query, (ordinal,))
    conn.commit()
    item = cur.fetchone()
    conn.close()

    if item is None:
        raise error.NotebookNotFoundError
    return item


def write_list(current_scene_db, notebook_list, path_list = []):
    """creates the list of notebooks in list"""
    from src.praxxis.sqlite import connection

    conn = connection.create_connection(current_scene_db)
    cur = conn.cursor()
    clear_list = 'DELETE FROM "NotebookList"'
    reset_counter = "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='NotebookList'"
    insert_line = 'INSERT INTO "NotebookList" (Notebook, Path, Library, RawUrl) VALUES (?,?,?,?)'
    cur.execute(clear_list)
    cur.execute(reset_counter)
    if path_list == []:
        cur.executemany(insert_line, notebook_list)
    else:
        cur.executemany(insert_line, (notebook_list, path_list))
    conn.commit()
    conn.close()


def get_notebook_path(library_db, notebook, library):
    """gets notebook path from libraries/notebooks"""
    from src.praxxis.sqlite import connection

    conn = connection.create_connection(library_db)
    cur = conn.cursor()
    get_notebook_path = "SELECT Path FROM 'Notebooks' WHERE Notebook=? AND Library=?"
    cur.execute(get_notebook_path, (notebook, library))
    conn.commit()
    path = cur.fetchone()
    conn.close()
    if path is None:
        return None
    return path[0]


def get_notebook_library(library_db, notebook):
    """gets all possible libraries for a notebook name"""
    from src.praxxis.sqlite import connection

    conn = connection.create_connection(library_db)
    cur = conn.cursor()
    get_notebook_library = "SELECT Library FROM 'NotebookList' WHERE Notebook=?"
    cur.execute(get_notebook_library, (notebook,))
    conn.commit()
    path = cur.fetchall()
    conn.close()
    if path is None:
        return None
    return path


def check_notebook_exists(library_db, notebook):
    from src.praxxis.sqlite import connection
    from src.praxxis.util import error

    conn = connection.create_connection(library_db)
    cur = conn.cursor()
    check_exists = 'Select * FROM Notebooks WHERE Notebook = ?'
    cur.execute(check_exists, (notebook,))
    conn.commit()
    rows = cur.fetchall()
    conn.close()

    if rows == []:
        raise error.NotebookNotFoundError(notebook)
    else:
        return 0


def search_notebooks(library_db, search_term, query_start, query_end):
    """searches notebooks for search term"""
    from src.praxxis.sqlite import connection

    conn = connection.create_connection(library_db)
    cur = conn.cursor()
    list_param = 'SELECT Notebook, Path, Library, RawUrl FROM "Notebooks" WHERE Notebook LIKE "%{}%" ORDER BY ' \
                 'Notebook LIMIT ?, ?'.format(search_term)
    cur.execute(list_param, (query_start, query_end))
    conn.commit()
    rows = cur.fetchall()
    conn.close()
    return rows
