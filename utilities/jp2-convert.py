import glob
import imageio
import os
import sys


# Use `imageio` + `freeimage` plugin for `.jp2` support. See: http://imageio.readthedocs.io/en/latest/format_jp2-fi.html#jp2-fi. From interactive REPL session, import `imageio` and then run `imageio.plugins.freeimage.download()`. This will check if the requirement is satisfied and download it if not.

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        sys.exit("USAGE: python -m scripts.convert_jp2 <DIR>")

    # get all jpegs in a specified folder
    directory_path = os.path.join(sys.argv[1], "*.jp2")
    path_list = glob.glob(directory_path)
    

    # still having issues with JP2 conversion...
    # just use direct JPEG download from PH lesson
    for path in path_list:
        img = imageio.imread(path)
        imageio.imwrite(path, img, format="jpg")