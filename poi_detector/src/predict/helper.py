from os.path import join as os_path_join
from os import mkdir as os_mkdir
from os import mkdir as os_mkdir
from os.path import join as os_path_join
from os import rename as os_rename

def keep_files(files_list: list, extention: str):
    final_list = []
    for file in files_list:
        if (extention in file[-3:]) and (extention != file):
            final_list.append(file)

    return final_list


def create_sub_dir(playlist_dir: str, sub_folder_name: str):
    new_path = os_path_join(playlist_dir, sub_folder_name)
    try:
        os_mkdir(new_path)
    except FileExistsError:
        pass
    return new_path

def move_file(from_path: str, to_path: str):
    os_rename(from_path, to_path)