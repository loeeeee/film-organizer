import re
import os
import yaml
import json
import helper
from logger import Logger
from config import Config

main_file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class Extension:
    VideoExtension = {
        "mp4",
        "mkv",
        "mov",
        "avi",
        "webm",
        "ts",
        "ogg"
    }
    SubtitleExtension = {
        "ass",
        "ssa",
        "srt",
        "vtt",
        "pgssub",
        "vobsub"
    }


# Procedures

def extract_film_info(full_path: str) -> dict:
    film_info = {
        "name": "",
        "year": "",
        "language": "",
        "imbdid": "",
        "tmbdid": "",
    }

    film_info["name"] = _extract_film_name(full_path)

    return film_info

def format_name(film_attribute: dict):
    # Format film name according to jellyfin requirements

    return

def _extract_film_name(full_path: str) -> str:
    film_name = ""
    if os.path.isdir(full_path):
        last_path = os.path.basename(os.path.normpath(full_path))
        film_name = clean_name(last_path)
    elif os.path.isfile(full_path):
        # Parse
        last_path = os.path.basename(os.path.normpath(full_path))
        [name, extension] = os.path.splitext(last_path)
        Logger.debug(f"Film name after removing extension {name}")
        film_name = clean_name(name)
    else:
        Logger.error(f"Not file or folder! {full_path}")
    return film_name

def clean_name(name: str) -> str:
    # Remove meta
    filter_construct_middleware = [f"({i})" for i in Config.config["Media Meta"]]
    combined = "|".join(filter_construct_middleware).replace(".", "\.").replace("-", "\-")
    reg = re.compile(rf"{combined}", flags=re.IGNORECASE)
    name = re.sub(reg, "%ReM0vE%", name)
    Logger.debug(f"Film name after removing meta {name}")

    # Remove REMOVE tag
    #reg = r"\[([^\]]*?[(%ReM0vE%)]+[^\[]*?)+?\]"
    reg = r"\[[^\]]*?(%ReM0vE%)[^\[]*?\]"
    name = re.sub(reg, "", name)
    Logger.debug(f"Film name after removing remove tag {name}")


    # Remove REMOVE tag
    #reg = r"\[([^\]]*?[(%ReM0vE%)]+[^\[]*?)+?\]"
    reg = r"[\b\.]*?(%ReM0vE%)[\b\.]*?"
    name = re.sub(reg, "", name)
    Logger.debug(f"Film name after removing remove tag {name}")

    # Remove [Weired characters]
    reg = r"\[\W*?\]"
    name = re.sub(reg, "", name)

    # Clean up
    reg = r"\[[(\s)-]*\]" # Remove [ ], []
    name = re.sub(reg, "", name)

    # Force additional spacing
    name = name.replace("-", " - ")

    # Remove comma
    name = name.replace(".", " ").title().strip()

    # Remove rip group name
    reg = r"-\s+[\w\[\]]+$"
    name = re.sub(reg, " ", name)

    # Clean duplicate space
    reg = r"\s+"
    name = re.sub(reg, " ", name)

    return name.strip()

# Main
def main():
    Logger.info("Main process starts.")

    # Walk the directory
    source_dir = os.path.join(main_file_path, Config.config["source"])
    target_dir = os.path.join(main_file_path, Config.config["target"])
    for path in os.listdir(source_dir):
        Logger.info(f"Looking at {path}.")
        full_path = os.path.join(source_dir, path)

        # Infer film info from source folder name
        film_info = extract_film_info(full_path)
        print(json.dumps(film_info, indent=2))

        # Handle null situation
        if not film_info["name"]:
            Logger.warning(f"{full_path} cannot be extracted.")
            continue

        # Create folder if source is a file
        
        mapped_target_folder_path = os.path.join(target_dir, film_info["name"])
        helper.create_folder_if_not_exists(mapped_target_folder_path)
        # mapped_target_film_path = os.path.join(mapped_target_folder_path, film_info["name"], )
        if os.path.isdir(full_path):
            for _path in os.listdir(full_path):
                _full_path = os.path.join(full_path, _path)
                if os.path.isfile(_full_path):
                    os.symlink(full_path, mapped_target_folder_path)
        # else:
        #     pass
    return

if __name__ == "__main__":
    main()