"""
This file deletes a scene.
"""


def delete_scene(args, scene_root, history_db):
    """deletes a specified scene, including all its data"""
    import shutil
    import os

    from src.praxxis.scene import current_scene
    from src.praxxis.sqlite import sqlite_scene
    from src.praxxis.display import display_scene
    from src.praxxis.util import error
    from src.praxxis.scene import scene

    if hasattr(args, "name"):
        if(args.name is None):
            name = sqlite_scene.get_current_scene(history_db)
        else:
            name = args.name
    else:
        name = args

    try:
        tmp_name = scene.get_scene_by_ordinal(args, name, history_db)
    except error.SceneNotFoundError as e:
        raise e
    except error.EndEndedSceneError as e:
        pass
        
    if tmp_name is not None:
        name = tmp_name

    directory = os.path.join(scene_root, name)

    if os.path.exists(directory):
        from src.praxxis.util import rmtree
        try:
            sqlite_scene.delete_scene(history_db, name)
            rmtree.rmtree(directory)
            display_scene.display_delete_scene_success(name)
            return name
        except error.LastActiveSceneError as e:
            raise e
    else:
        raise error.SceneNotFoundError(name)
