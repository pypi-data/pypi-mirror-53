#!/usr/bin/env python3
from copy_spotlights import copy_spotlights_images
from argparse import ArgumentParser
from pathlib import Path


def main():

    # Argument Parser to enable use of this program using bash terminal
    parser = ArgumentParser()
    parser.add_argument("save_dir", type=str, help="directory location where spotlight images will be copied to")
    parser.add_argument("--no-split", dest="no_split", action="store_true", help="portrait and landscape images will not be placed into separate folders")
    parser.add_argument("--min-res", dest="min_res", type=int, help="ignore images with horizontal or vertical resolution lower than min_res value, default:1920", default=1920)
    parser.add_argument("--dir-land", dest="dir_land", type=str, help="directory name in which to store landscape images, default:landscape", default="landscape")
    parser.add_argument("--dir-port", dest="dir_port", type=str, help="directory name in which to store portrait images, default:portrait", default="portrait")
    parser.add_argument("--dir-other", dest="dir_other", type=str, help="directory name in which to store images of equal resolution, default:other", default="other")
    args = parser.parse_args()

    # Known directory location path where windows stores spotlight images
    home = Path.home()
    spotlight_dir = Path.joinpath(home, Path('AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets'))

    save_dir = args.__getattribute__("save_dir")
    split = not args.__getattribute__("no_split")
    min_res = args.__getattribute__("min_res")
    dir_land = args.__getattribute__("dir_land")
    dir_port = args.__getattribute__("dir_port")
    dir_other = args.__getattribute__("dir_other")

    copy_spotlights_images(spotlight_dir, save_dir, split, min_res, dir_land, dir_port, dir_other)


if __name__ == "__main__":
    main()
