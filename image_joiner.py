""" image_joiner_for_pages

    Utility for joining (stitching) images that have some overlap

"""

from config import settings

def check_config(verbose=False):
    """ Checks that we have enough information to actually perfrom some operations
    
    """

    config_ok = False

    if verbose:
        print(f"Checking configuration for {__file__}")
        config_ok = True

    return config_ok

def join_images():
    """ This is the main program logic """

    config_ok = check_config(verbose=True)


    print(f"Image joiner")

if __name__ == "__main__":
    join_images()
