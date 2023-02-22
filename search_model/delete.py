import os
folder_path = "results_copy"

for dir in os.listdir(folder_path):
    for file in os.listdir(os.path.join(folder_path,dir)):
        file_name = os.path.basename(file).split('.')[0]
        if file_name == dir:
            os.remove(os.path.join(folder_path,dir,file))
