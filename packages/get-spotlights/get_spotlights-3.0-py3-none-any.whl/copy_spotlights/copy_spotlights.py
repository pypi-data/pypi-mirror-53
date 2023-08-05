from os import path, makedirs, listdir
from shutil import copy

from PIL import Image


def find_images(dir):
    """Given a directory, finds out which files in the root of the directory are images

    Arguments:
      dir {str} -- directory location to scan for image files

    Raises:
      AssertionError -- if given directory is not valid

    Returns:
      list -- list of filenames found in the given directory which are images
    """
    assert path.isdir(dir)==True

    im_files = []

    for item in listdir(dir):
        item_path = path.normpath(path.join(dir, item))

        if path.isfile(item_path):
            try:
                Image.open(item_path)
                im_files.append(item)
            except IOError:
                pass

    return im_files


def copy_spotlights_images(spotlights_dir, save_dir, split=True, min_res=1920, dir_land="landscape", dir_port="portrait", dir_other="other"):
    """For Windows 10 users, copies beautiful images stored on their machine, called 'Windows Spotlights' to a directory of their choice.

    Arguments:
      spotlights_dir {str} -- directory location where windows 10 stores spotlight images
      save_dir {str} -- directory location where spotlight images will be copied to

    Keyword Arguments:
      split {bool} -- split images into different folders based on types such as landscape and portrait (default: {True})
      min_res {int} -- only include images with width or height greater than or equal to {min_res}
      dir_land {str} -- directory name in which to store landscape images (default: {"landscape"})
      dir_port {str} -- directory name in which to store portrait images (default: {"portrait"})
      dir_other {str} -- directory name in which to store images other than portrait or landscape type (default: {"other"})

    Raises:
      Exception -- raises exception if save_dir is not valid
    """
    if not path.isdir(save_dir):
        raise Exception(f"'{save_dir}' does not seem to be a valid directory!")
    min_res = int(min_res)

    complete_landscape_path, complete_portrait_path, complete_other_path = "", "", ""

    if split:
        # get complete paths to landscape, portrait, and other directories inside the save directory
        complete_landscape_path = path.normpath(path.join(save_dir, dir_land))
        complete_portrait_path = path.normpath(path.join(save_dir, dir_port))
        complete_other_path = path.normpath(path.join(save_dir, dir_other))

        # make required directories if they don't exist
        if not path.isdir(complete_landscape_path):
            makedirs(complete_landscape_path)
        if not path.isdir(complete_portrait_path):
            makedirs(complete_portrait_path)
        if not path.isdir(complete_other_path):
            makedirs(complete_other_path)

    else:
        # don't copy spotlight images into different folders
        complete_landscape_path, complete_portrait_path, complete_other_path = save_dir, save_dir, save_dir

    for image_file in find_images(spotlights_dir):
        image_file_full_path = path.normpath(path.join(spotlights_dir, image_file))

        im = Image.open(image_file_full_path)

        # save image with an extension as read by PIL.Image module
        save_image_file_name = image_file + "." + im.format
        where = None

        im_width, im_height = int(im.size[0]), int(im.size[1])

        if im_width >= min_res or im_height >= min_res:
            if (im_height < im_width):
                where = path.normpath(path.join(complete_landscape_path, save_image_file_name))

            elif (im_width < im_height):
                where = path.normpath(path.join(complete_portrait_path, save_image_file_name))

            else:
                where = path.normpath(path.join(complete_other_path, save_image_file_name))

        if where is not None:
            copy(image_file_full_path, where)
