import cv2
import os
import glob
import sys
import scipy
import numpy as np


def findMinimum(img):
    pass


def cropConcaveDistorted(colored):
    gray = cv2.cvtColor(colored, cv2.COLOR_BGR2GRAY)
    x = int(gray.shape[1] * 0.5)
    y = int(gray.shape[0] * 0.5)

    # Height
    column = gray[:, x]
    nz = np.sort(np.where(column > 0))
    min_y = np.min(nz)
    max_y = np.max(nz)

    # Width
    row = gray[y, :]
    nz = np.sort(np.where(row > 0))
    min_x = np.min(nz)
    max_x = np.max(nz)

    crop = colored[min_y:max_y, min_x:max_x, :]
    return crop


def cropToRatio(colored, ratio, rescale_height=None):
    h, w, c = colored.shape
    nw = int(colored.shape[1])
    nh = int(nw / convertion_ratio)
    y = int((h - nh) / 2)
    crop = colored[y: y + nh, :]

    if rescale_height is not None:
        crop = cv2.resize(crop, (int(rescale_height * ratio), rescale_height))
    return crop


ext = "png"
source_folder = sys.argv[1]
output_folder = sys.argv[2]
convertion_ratio = 2.0

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


files = sorted(glob.glob(os.path.join(source_folder, "*." + ext)))

r_counter = 0
d_counter = 0
for i, f in enumerate(files):

    colored = cv2.imread(f)
    if 'Rectified' in f:
        output_filename_base = "{}".format(str(r_counter).zfill(5))
        r_counter += 1
        crop = cropConcaveDistorted(colored)
        crop2 = cropToRatio(crop, convertion_ratio, rescale_height=None)

        crop_filename = "rectified_" + output_filename_base
        crop2_filename = "rectified_" + output_filename_base + "_reduced"

        cv2.imwrite(os.path.join(output_folder,
                                 crop_filename + "." + ext), crop)
        cv2.imwrite(os.path.join(output_folder,
                                 crop2_filename + "." + ext), crop2)
    else:
        output_filename_base = "{}".format(str(d_counter).zfill(5))
        d_counter += 1
        crop = cropToRatio(colored, convertion_ratio, rescale_height=None)

        original_filename = "distorted_" + output_filename_base
        crop_filename = "distorted_" + output_filename_base + "_reduced"

        cv2.imwrite(os.path.join(output_folder,
                                 original_filename + "." + ext), colored)
        cv2.imwrite(os.path.join(output_folder,
                                 crop_filename + "." + ext), crop)
