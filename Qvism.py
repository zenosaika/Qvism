# brew install tesseract tesseract-lang
# pip install pytesseract
# export TESSDATA_PREFIX=/opt/homebrew/Cellar/tesseract/5.3.4/share/tessdata
# https://github.com/tesseract-ocr/tessdata_best/tree/main

import os
import cv2
import numpy as np
import pytesseract
from PIL import Image

config = r'--tessdata-dir "/opt/homebrew/Cellar/tesseract/5.3.4/share/tessdata"'

# check available langs
# print(pytesseract.get_languages(config=config))

filename = 'SRS.jpg'
lang = 'thai_best+eng_best'

# read image
img = Image.open(f'images/{filename}')

# increase dpi to 300
img.save('images/tmp.png', dpi=(300,300))
tmp = Image.open('images/tmp.png')
os.remove('images/tmp.png')

# convert to grayscale
img_gray = tmp.convert("L")

# apply erosion & dilation
# kernel = np.ones((3,3), np.uint8)
# conv_img = np.array(img_gray)
# dilation_img = cv2.dilate(conv_img, kernel, iterations=1)
# erosion_img = cv2.erode(conv_img, kernel, iterations=1)
# erosion_img = Image.fromarray(np.uint8(erosion_img))
# erosion_img.save('images/erosion.png')

# thresholding
# blur = cv2.GaussianBlur(np.array(img_gray),(5,5),0)
# ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret, thresh = cv2.threshold(np.array(img_gray), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
thresh = Image.fromarray(np.uint8(thresh))
thresh.save('images/thresh.png')

# execute tesseract ocr
print('[Qvism]: Loading...')
txt = pytesseract.image_to_string(thresh, lang=lang, config=config)
print('[Qvism]: Finished!')
print('*'*70, '\n\n', txt, '\n', '*'*70)

with open('output.txt', 'w') as f:
    f.write(txt)
    