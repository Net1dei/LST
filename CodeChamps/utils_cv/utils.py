
import os
from CodeChamps.utils_cv.args import PATH_TO_SAVE_PREDICTIONS
import shutil
 
def delete_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Ошибка при удалении файла {file_path}. {e}')

def create_data_dir(path_=PATH_TO_SAVE_PREDICTIONS):
    path_ = path_
    if not os.path.exists(path_):
        os.makedirs(path_)
        os.makedirs(path_+'/images')
        os.makedirs(path_+'/labels')

    else:
        shutil.rmtree(path_)
        create_data_dir(path_)

def save_results_to_txt(results,count):
    with open(f"{PATH_TO_SAVE_PREDICTIONS}/labels/{count}.txt", "w") as file:
        file.writelines([f"0 {int(box[0])} {int(box[1])} {int(box[2])} {int(box[3])}" for box in results])
        
    




