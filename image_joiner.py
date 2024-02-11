""" image_joiner_for_pages

    Utility for joining (stitching) images that have some overlap

"""

import img2pdf
from PIL import Image
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

def trim_images():
    """ Cut relevant parts of the screenshots from input images

        Generate new filenames
    """

    config_ok = check_config(verbose=True)

    input_folder = Path(settings["INPUT_FOLDER"])
    trim_folder = Path(settings["WORKING_FOLDER"])

    first_to_join = settings["PAGE_STITCH_FIRST"]
    last_to_join = settings["PAGE_STITCH_LAST"]

    crop_window_even = (settings["PAGE_EVEN_LEFT"],settings["PAGE_EVEN_TOP"],settings["PAGE_EVEN_RIGHT"],settings["PAGE_EVEN_BOTTOM"])
    crop_window_odd = (settings["PAGE_ODD_LEFT"],settings["PAGE_ODD_TOP"],settings["PAGE_ODD_RIGHT"],settings["PAGE_ODD_BOTTOM"])
        
    file_list = get_file_list(input_folder, "*.png")
    # print(f"Have {len(file_list)} files to process")

    image_info = dict()
    image_sizes = dict()

    file_index = 0
    output_page_num = 0
    for each_file in file_list:
        file_index += 1
        
        with Image.open(each_file) as input_img:
            this_size = input_img.size
            new_count = image_sizes.get(this_size, 0) + 1
            image_sizes[this_size] = new_count
            output_page_num = int((file_index + 2) /2)
            crop_window = crop_window_even
            if file_index in range(first_to_join, last_to_join + 1):
                if (file_index % 2) == 0:   # Even so left side
                    output_page_suffix = "_L"
                    crop_window = crop_window_even
                else:
                    output_page_suffix = "_R"
                    crop_window = crop_window_odd
            else:
                output_page_suffix = ""
            output_filedesc = f"Page_{output_page_num:02}{output_page_suffix}"
            output_filename = trim_folder / f"{output_filedesc}.png"
            print(f"File: {file_index:02} : {each_file.name} - {output_filedesc}")
            cropped_img = input_img.crop(crop_window)
            cropped_img.save(output_filename)

    print(f"Input image sizes: {image_sizes}")

    return output_page_num


def stitch_images(last_page=False):
    """ Join input images

        Generate new filenames
    """

    assert last_page, "Invalid page number"

    trim_folder = Path(settings["WORKING_FOLDER"])
    output_folder = Path(settings["OUTPUT_FOLDER"])

    crop_window_left = (settings["PAGE_EVEN_LEFT"],settings["PAGE_EVEN_TOP"],settings["PAGE_EVEN_RIGHT"],settings["PAGE_EVEN_BOTTOM"])
    crop_window_right = (settings["PAGE_ODD_LEFT"],settings["PAGE_ODD_TOP"],settings["PAGE_ODD_RIGHT"],settings["PAGE_ODD_BOTTOM"])
    
    crop_size_offset_x = settings["POINT_OFFSET_X"]

    size_left_x = crop_window_left[2] - crop_window_left[0] + 1
    size_left_y = crop_window_left[3] - crop_window_left[1] + 1

    size_right_x = crop_window_right[2] - crop_window_right[0] + 1
    size_right_y = crop_window_right[3] - crop_window_right[1] + 1
    
    size_output = (crop_size_offset_x + size_right_x, size_left_y)

    print(f"Sizes are L:{size_left_x}x{size_left_y} and R:{size_right_x}x{size_right_y}")
    source_file_list = get_file_list(trim_folder, "*.png")

    for output_page_num in range(1, last_page + 1):
        # Get a list of files with "Page_nn" in the file name
        source_pages = [input_page for input_page in source_file_list if (f"Page_{output_page_num:02}" in input_page.name)]
        # print(f"Page {output_page_num:02} has {len(source_pages)} source files")
        assert len(source_pages) in range(1,3), f"Unexpected number of source images for page {output_page_num}"
        output_filename = output_folder / f"Page_{output_page_num:02}.png"
        img_output =Image.new("RGB", size_output, "white")
        with(img_output):
            if len(source_pages) == 1:
                img_left = source_pages[0]
                with Image.open(img_left) as input_img:
                    img_output.paste(input_img,(0,0))
                #this_size = input_img.size
            else:
                img_left = source_pages[0]
                img_right = source_pages[1]
                with Image.open(img_left) as input_img:
                    img_output.paste(input_img,(0,0))
                with Image.open(img_right) as input_img:
                    img_output.paste(input_img,(crop_size_offset_x,0))

            img_output.save(output_filename)

    return last_page


def create_pdf(last_page=False):
    """ Create a singe PDF for the images
    """

    assert last_page, "Invalid page number"

    output_folder = Path(settings["OUTPUT_FOLDER"])
    output_filename = output_folder / "Compiled_pdf_output.pdf"

    source_image_list = get_file_list(output_folder, "*.png")
    count_pages = 0

    with open(output_filename, "wb") as pdf_file:
        for input_image in source_image_list:
            count_pages += 1
        pdf_file.write(img2pdf.convert(source_image_list))

    return count_pages

def _process_all_files():
    
    """ This is the main program logic 
    

    """

    # First stage is to trim the whitespace from the images
    # page_count = trim_images()

    # The second stage is to stitch the images togeher
    # page_count = 41
    # page_count = stitch_images(page_count)

    # The third stage is to create a single pdf
    page_count = 41
    page_count = create_pdf(page_count)

    print(f"Finished creating pdf from {page_count} images")

if __name__ == "__main__":
    _process_all_files()
