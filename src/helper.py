import os
import logger

def create_folder_if_not_exists(folder_path: str) -> bool:
    # Return if the folder exists
    # It only create one folder at a time
    
    if os.path.isfile(folder_path):

        return