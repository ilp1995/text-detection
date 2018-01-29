# FEDERAL RURAL UNIVERSITY OF PERNAMBUCO
# DISCIPLINE OF IMAGE PROCESSING
# PROFESSOR VALMIR MACARIO
# STUDENT IVERSON LUIS PEREIRA
# COURSE OF COMPUTER SCIENCE
import math
import numpy as np
import cv2
import os
import sys
from time import time
from scipy.spatial import KDTree
from matplotlib import pyplot as plt

#paramenters that can to influence the result
CANNY_THRESHOLD_MIN = 250
CANNY_THRESHOLD_MAX = 400
WITH_HIST_EQU = False
WITH_MORPH_DIL = False
MORPH_WINDOW = (7, 7)
INTERATIONS_MORPH = 1
MAX_RAY_LEN = 100
MAX_ANGL_DIFF = math.pi/2

def pre_processing(img_path):
    """
    improve the image to a best edge detection
    """
    img_original = cv2.imread(img_path)    
    img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    if WITH_HIST_EQU:
        return cv2.equalizeHist(img_gray)
    else:
        return img_gray     

def edge_detection(img_preprocessed):
    """
    detects edges of an image
    """
    img_edges = cv2.Canny(img_preprocessed, CANNY_THRESHOLD_MIN, CANNY_THRESHOLD_MAX)   
    if WITH_MORPH_DIL:
        kernel = np.ones(MORPH_WINDOW, np.uint8)
        dilated = cv2.dilate(img_edges, kernel, INTERATIONS_MORPH)
        return dilated
    else:
        return img_edges

def gradient_detection(img_preprocessed):
    """
    detects the horizontal and vertical gradients
    """
    sobelx64f = cv2.Sobel(img_preprocessed, cv2.CV_64F, 1, 0, ksize=5)
    sobely64f = cv2.Sobel(img_preprocessed, cv2.CV_64F, 0, 1, ksize=5)
    theta = np.arctan2(sobely64f, sobelx64f)

    return sobelx64f, sobely64f, theta

def stroke_width_transform(theta, edges, sobelx64f, sobely64f, verbose=0):
    """
    find the stroke of edges
    """
    swt = np.empty(theta.shape)
    swt[:] = np.Infinity
    rays = []

    step_x = -1 * sobelx64f
    step_y = -1 * sobely64f
    mag = np.sqrt(step_x * step_x + step_y * step_y)

    with np.errstate(divide='ignore', invalid='ignore'):
        d_all_x = step_x / mag
        d_all_y = step_y / mag

    for p_x in range(edges.shape[1]):
        for p_y in range(edges.shape[0]):

            if edges[p_y, p_x] > 0:
                d_p_x = d_all_x[p_y, p_x]
                d_p_y = d_all_y[p_y, p_x]
                if math.isnan(d_p_x) or math.isnan(d_p_y):
                    continue
                ray = [(p_x, p_y)]
                prev_x, prev_y, i = p_x, p_y, 0

                while True:
                    i += 1
                    q_x = math.floor(p_x + d_p_x * i)
                    q_y = math.floor(p_y + d_p_y * i)
                    if q_x != prev_x or q_y != prev_y:
                        try:                            
                            if edges[q_y, q_x] > 0:
                                ray.append((q_x, q_y))                               
                                if len(ray) > MAX_RAY_LEN:
                                    break                                
                                delta = max(min(d_p_x * -d_all_x[q_y, q_x] + d_p_y * -d_all_y[q_y, q_x], 1.0), -1.0)
                                if not math.isnan(delta) and math.acos(max([-1.0, min([1.0, delta])])) < MAX_ANGL_DIFF:
                                    ray_len = math.sqrt((q_x - p_x) ** 2 + (q_y - p_y) ** 2)
                                    for (rp_x, rp_y) in ray:
                                        swt[rp_y, rp_x] = min(ray_len, swt[rp_y, rp_x])
                                    rays.append(np.asarray(ray))
                                break                           
                            ray.append((q_x, q_y))                      
                        except IndexError:
                            break
                        prev_x = q_x
                        prev_y = q_y

    for ray in rays:
        median = np.median(swt[ray[:, 1], ray[:, 0]])
        for (p_x, p_y) in ray:
            swt[p_y, p_x] = min(median, swt[p_y, p_x])

    if verbose > 0:
        cv2.imwrite('output/swt.jpg', swt * 100)

    return swt

def connected_components():
    """
    detects the connected components from swt result image, verifying each stroke width
    """
    #TODO

def main():
    """
    run the program to detect text in images
    """
    filepath = sys.argv[1]
    img = pre_processing(filepath)
    cv2.imwrite("preprocessing.jpg", img)
    img2 = edge_detection(img)
    cv2.imwrite("edges.jpg", img2)


#start the program
main()
