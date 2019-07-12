import glob
import os
from PIL import Image

def convert_image_formats(data_dir, inputfileext, outputfileext):

    data_filepath = os.path.join(os.getcwd(), data_dir)
    
    # UserWarning: Palette images with Transparency expressed in bytes should 
    # be converted to RGBA images "Palette images with Transparency expressed 
    # in bytes should be "
    images_to_convert = glob.glob(os.path.join(data_filepath, f"*.{inputfileext}"))
    for image in images_to_convert:
        im = Image.open(image)
        rgb_im = im.convert("RGB")
        filename = os.path.basename(image).split(".")[0]
        rgb_im.save(f"./data/images/{filename}.jpg")
        os.remove(image)

if __name__ == "__main__":

    convert_image_formats("data/images", "png", "jpg")