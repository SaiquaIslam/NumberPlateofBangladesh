import pytesseract
import cv2
try:
    from PIL import Image
except ImportError:
    import Image
import os
import numpy as np
import bangla
from googletrans import Translator

gray = cv2.imread("112.PNG", 0)
height,width=gray.shape
gray = cv2.resize( gray, None, fx = 100/height, fy = 200/width, interpolation = cv2.INTER_CUBIC)
#cv2.imshow("Gray", gray)
#cv2.waitKey(0)
blur = cv2.GaussianBlur(gray, (3,3), 0)
#gray = cv2.medianBlur(blur, 3)
# perform otsu thresh (using binary inverse since opencv contours work better with white text)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
#cv2.imshow("Otsu", gray)
#cv2.waitKey(0)
rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

# apply dilation
dilation = cv2.dilate(thresh, rect_kern, iterations = 3)
cv2.imshow("dilation", dilation)
cv2.waitKey(0)
try:
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
except:
    ret_img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

# create copy of image
im2 = gray.copy()

plate_num = ""
# loop through contours and find letters in license plate
for cnt in sorted_contours:
    #print("hello")
    x, y, w, h = cv2.boundingRect(cnt)
    height, width = im2.shape

    # if height of box is not a quarter of total height then skip
    #if height / float(h) > 6: continue
    ratio = h / float(w)
    # if height to width ratio is less than 1.5 skip
    if ratio < .4: continue
    area = h * w
   # print(area)
    # if width is not more than 25 pixels skip
    if width / float(w) > 15: continue
    # if area is less than 100 pixels skip
    if area <1500: continue
    # draw the rectangle
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    roi = thresh[y - 5:y + h + 5, x - 5:x + w + 5]
    roi = cv2.bitwise_not(roi)
    roi = cv2.medianBlur(roi, 5)
    #cv2.imshow("ROI", roi)
    #cv2.waitKey(0)
    custom_config = r' tessedit_char_whitelist=০১২৩৪৫৬৭৮৯ঢাকা -l ben --psm 8 --oem 3'
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/tesseract-ocr/tesseract.exe"
    text = pytesseract.image_to_string(gray, lang="ben", config=custom_config)
    #text=bangla.convert_english_digit_to_bangla_digit(text)
    #print(height)
    plate_num += text

print(plate_num)
outF = open("myOutFile.txt", "w",encoding = 'utf-8')
for line in plate_num:
    outF.write(line)
outF.close()


cv2.imshow("Character's Segmented", im2)
cv2.waitKey(0)
cv2.destroyAllWindows()
