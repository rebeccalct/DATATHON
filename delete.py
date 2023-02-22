import os

folder_path = "/path/to/folder"
folder_name = os.path.basename(folder_path)

file_path = os.path.join(folder_path, folder_name)

if os.path.isfile(file_path):
    os.remove(file_path)
