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


def cropToSlices(colored, ratio, steps, delta):
    h, w, c = colored.shape
    nw = int(colored.shape[1])
    nh = int(nw / convertion_ratio)
    y = int((h - nh) / 2)

    versions = [colored[y: y + nh, :].copy()]

    for s in range(0, steps):
        ny1 = y - s * delta
        ny2 = ny1 + nh
        if ny1 < 0:
            break
        versions.append(colored[ny1: ny2, :].copy())

    for s in range(0, steps):
        ny1 = y + s * delta
        ny2 = ny1 + nh
        if ny2 >= h:
            break
        versions.append(colored[ny1: ny2, :].copy())

    return versions


ext = "png"
img_file = sys.argv[1]
output_folder = sys.argv[2]
convertion_ratio = 2.0

img = cv2.imread(img_file)

versions = cropToSlices(img, 2, 1000, 50)

for i, v in enumerate(versions):
    outname = "{}.png".format(str(i).zfill(5))
    outname = os.path.join(output_folder, outname)
    cv2.imwrite(outname, v)

whole = np.vstack(versions)

print(len(versions))
cv2.namedWindow("whole", cv2.WINDOW_NORMAL)
cv2.imshow("ciao", img)
cv2.imshow("whole", whole)
cv2.waitKey(0)
