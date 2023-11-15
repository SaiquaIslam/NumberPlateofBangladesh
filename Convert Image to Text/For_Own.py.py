import cv2
from PIL import Image as pil_image
from PIL import Image
import glob
import os
image_list = []
for filename in glob.glob('New new/*.jpg'):
    print("The size of the image before conversion : ", end="")
    #print(os.path.getsize("geeksforgeeks.png"))

    # converting to jpg
    rgb_im = im.convert("RGB")

    # exporting the image
    rgb_im.save("geeksforgeeks_jpg.jpg")
    print("The size of the image after conversion : ", end="")
    print(os.path.getsize("geeksforgeeks_jpg.jpg"))