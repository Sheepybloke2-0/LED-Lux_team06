import numpy as np
import cv2
from matplotlib import pyplot as plt

vid = cv2.VideoCapture(0)
fist = cv2.imread("right_fist.jpg", 0)

fist_roi = fist[100:500, 300:700]

orb_vid = cv2.ORB_create(1000)
orb_pic = cv2.ORB_create(100)

kp_pic, desc_pic = orb_pic.detectAndCompute(fist_roi, None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

while(1):
    err, img = vid.read()
    if err == True:
        kp_vid = orb_vid.detect(img,None)
        kp_vid, desc_vid = orb_vid.compute(img, kp_vid)
        matches = bf.match(desc_vid, desc_pic)
        matches = sorted(matches, key = lambda x:x.distance)

        # img2 = cv2.drawKeypoints(img, kp_vid, None, color=(255,0,0), flags=0)
        matched_img = cv2.drawMatches(img, kp_vid, fist_roi, kp_pic, matches[:100], img, \
                                    matchColor=(200,200,0), singlePointColor=(201,0,200), flags=2)

        # cv2.imshow("img", img2)
        cv2.imshow("img", matched_img)

    else:
        break
    k = cv2.waitKey(60) & 0xFF
    if k == 27:
        break

vid.release()
