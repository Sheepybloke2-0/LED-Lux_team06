import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

vid = cv2.VideoCapture(0)
fist = cv2.imread("right_fist.jpg", 0)

fist_roi = fist[100:500, 300:700]

sift = cv2.xfeatures2d.SIFT_create(1000)

kp_pic, desc_pic = sift.detectAndCompute(fist_roi, None)

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

while(1):
    err, img = vid.read()
    if err == True:
        kp_vid, desc_vid = sift.detectAndCompute(img, None)
        matches = flann.knnMatch(desc_vid, desc_pic, k=2)

        # Need to draw only good matches, so create a mask
        matchesMask = [[0,0] for i in xrange(len(matches))]
        # ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.7*n.distance:
                matchesMask[i]=[1,0]
        # img2 = cv2.drawKeypoints(img, kp_vid, None, color=(255,0,0), flags=0)
        matched_img = cv2.drawMatchesKnn(img, kp_vid, fist_roi, kp_pic, matches, None, \
                                    matchColor=(200,200,0), singlePointColor=None, \
                                    matchesMask=matchesMask, flags=2)

        # cv2.imshow("img", img2)
        cv2.imshow("img", matched_img)

    else:
        break
    k = cv2.waitKey(60) & 0xFF
    if k == 27:
        break

vid.release()
