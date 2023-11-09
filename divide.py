import cv2
import pytesseract
import numpy as np
import io
from PIL import Image as pil_image
from PIL import Image
import glob
image_list = []
for filename in glob.glob('New new/*.jpg'): #assuming gif
    img = Image.open(filename)
    image_list.append(img)
    with open(filename, 'rb') as f:
        img = pil_image.open(io.BytesIO(f.read()))
        pass

#cv2.imshow("Original Image", image)
#cv2.waitKey(0)
    plate_num = ""
    height, width = img.shape[:2]
    print (img.shape)
    start_row, start_col = int(0), int(0)
    end_row, end_col = int(height * .5), int(width)
    cropped_top = (img[start_row:end_row , start_col:end_col])
    print(start_row, end_row)
    print(start_col, end_col)

    #cv2.imshow("Cropped Top", cropped_top)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    cropped_top = cv2.resize(cropped_top, None, fx =170/height , fy = 320/width , interpolation = cv2.INTER_CUBIC)
    cropped_top=np.gra
    cv2.imshow("Cropped Top", cropped_top)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #cropped_top = cv2.GaussianBlur(cropped_top, (5,5), 0)
    #ret, thresh = cv2.threshold(cropped_top, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)


    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilation = cv2.dilate(cropped_top, rect_kern, iterations = 1)
    cv2.imshow("dilation", dilation)
    cv2.waitKey(0)

    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    erosion1=cv2.erode(dilation,rect_kern,iterations=1)
    cv2.imshow("erosion", erosion1)
    cv2.waitKey(0)

    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    dilation1 = cv2.dilate(erosion1, rect_kern, iterations = 1)
    cv2.imshow("dilation", dilation1)
    cv2.waitKey(0)



    custom_config = r' tessedit_char_whitelist=০১২৩৪৫৬৭৮৯ঢাকা -l ben --psm 8 --oem 3'
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/tesseract-ocr/tesseract.exe"
    text = pytesseract.image_to_string(erosion1, lang="ben", config=custom_config)

    plate_num += text

    print(plate_num)

    plate_num = ""
    # Let's get the starting pixel coordiantes (top left of cropped bottom)
    start_row, start_col = int(height * .5), int(0)
    # Let's get the ending pixel coordinates (bottom right of cropped bottom)
    end_row, end_col = int(height), int(width)
    cropped_bot = image[start_row:end_row , start_col:end_col]
    print(start_row, end_row)
    print(start_col, end_col)

    cv2.imshow("Cropped Bot", cropped_bot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cropped_bot = cv2.resize(cropped_bot, None, fx = 100/height, fy = 200/width, interpolation = cv2.INTER_CUBIC)
    custom_config = r' tessedit_char_whitelist=০১২৩৪৫৬৭৮৯ঢাকা -l ben --psm 8 --oem 3'
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/tesseract-ocr/tesseract.exe"
    text = pytesseract.image_to_string(cropped_bot, lang="ben", config=custom_config)

    plate_num += text

    print(plate_num)