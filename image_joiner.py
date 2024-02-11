""" image_joiner_for_pages

    Utility for joining (stitching) images that have some overlap

"""

from config import settings
from pathlib import Path

def check_config(verbose=False):
    """ Checks that we have enough information to actually perfrom some operations
    
    """

    config_ok = True

    if verbose:
        print(f"Checking configuration for {__file__}")

    folder_input = Path(settings['INPUT_FOLDER'])
    if not folder_input.is_dir():
        print(f"No input directory at: {folder_input}")
        config_ok = False
    else:
        if verbose:
            print(f"Input folder is {folder_input}")


    return config_ok

def get_file_list(source_folder, file_filter="*.*"):
    """ retrieves a list of files in the provided folder """

    all_files = Path(source_folder).glob(file_filter)

    sorted_list = sorted(list(all_files))

    return sorted_list

def join_images():
    """ This is the main program logic """

    config_ok = check_config(verbose=True)

    input_folder = Path(settings["INPUT_FOLDER"])
    file_list = get_file_list(input_folder, "*.png")
    print(f"Have {len(file_list)} files to process")

    count_files = 0
    for each_file in file_list:
        count_files += 1
        print(f"File: {count_files:02} : {each_file.name}")

    print(f"\nAll done")

if __name__ == "__main__":
    join_images()
