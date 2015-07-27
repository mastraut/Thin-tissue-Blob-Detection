import os
from math import sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage import filter
from skimage import exposure
from skimage.io import imread
from skimage.filter import canny
from skimage.feature import blob_log
from skimage.transform import resize
from skimage.draw import circle_perimeter
from skimage.transform import hough_circle
from skimage.feature import peak_local_max
from skimage.restoration import denoise_bilateral
from skimage.morphology import reconstruction, closing, square

for fn in os.listdir(os.getcwd()):
    #Place blob_detection.py inside same folder with images to begin....
    #Import next pic
    print fn
    raw = imread(str(fn))
    img = resize(raw, (1050,512))

    #Erosion low-intensity-gradient detail removal
    seed = np.copy(img)
    seed[1:-1,1:-1] = img.max()
    mask = img
    filled_in = reconstruction(seed, mask, method = 'erosion')
    diff = (img-filled_in)

    #Canny edge detection over eroded image
    lines = canny(diff, sigma = 4.5)

    #Close all detected edges to improve detection
    closed_surface = closing(lines, square(25))
    plt.imshow(closed_surface, cmap='gray', interpolation='nearest')
    plt.title('Image %s bubble detection prep' %fn)
    plt.show()

    #Blob detection using Laplacian of Gaussian filter
    print "Finding blobs in image..."
    try:
        blobs_log = blob_log(closed_surface, min_sigma=10)
        print 'Found %d bubbles' %len(blobs_log)
        blobs_list = [blobs_log]
        colors = ['red']
        titles = ['Laplacian of Gaussian']
        sequence = zip(blobs_list, colors, titles)

        for blobs, color, title in sequence:
            fig, ax = plt.subplots(1,1)
            ax.set_title(title)
            ax.imshow(img, cmap='gray', interpolation='nearest')
            for blob in blobs:
                y, x, r = blob
                c = plt.Circle((x,y),r, color = color, linewidth=1, fill=False)
                ax.add_patch(c)
        plt.title('Image %s bubble if present circled in red' %fn)
        plt.show() 
    except:
        print 'Found no bubbles'
       

    #Check image for curl
    val = filter.threshold_otsu(img)
    hist, bins_center = exposure.histogram(img)

    plt.figure(figsize=(9, 4))
    plt.subplot(131)
    plt.imshow(img, cmap='gray', interpolation='nearest')
    plt.axis('off')
    plt.subplot(132)
    plt.imshow(img < val, cmap='gray', interpolation='nearest')
    plt.axis('off')
    plt.subplot(133)
    plt.plot(bins_center, hist, lw=2)
    plt.axvline(val, color='k', ls='--')
    plt.tight_layout()
    plt.title("Camera (OTSU threshold) prep for shape evaluation")
    plt.show()

    shapely = img[img < val].shape[0]
    print 'Area of image... %d' %shapely
    if shapely < (537600 - 600):
        print 'Image shape not normal...curl likely.'
    else:
        print 'No sign of curl....'

