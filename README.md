# Thin-tissue-Blob-Detection

Blob detection is the identifying of anomalous sections of an image.  This code is for detecting erroneous details on tissue scans.  The two big items of interest were air bubbles that refract the light, distorting the image, and sample curl (results in complete opacity of the image covered).  

Air bubbles produce a high gradient effect at the edge of the bubble where the light is mostly dissipated by the refraction angle.  This shows up as a black ring on the image.  To extract this feature, I subtracted off all the similar intensity regions of the image using an erosion method from Scikit-image.  On this, the Scikit-image canny filter returned lines over the lowest intensity areas of the image that was closed to form blobs of the areas denoted by the canny filter.  After tuning the parameters of the canny and closing methods, the algorithm returns a blacked-out image with white ‘blobs’ denoting the bubbles.  The Laplacian of Gaussian method then is used to determine the location and radius of the blob, and it is circled on the image.

Detecting non-uniform tissue sizes is even easier.  Applying the Scikit-image camera filter with OTSU filter threshold selects only the high intensity parts of the image and ignores the background which shows up as the solid black region at the edge of the image.  If the area of this filtered image is smaller than the expected size of the tissue slice, the image has had a corner of the image compromised by the curl obstruction to the camera.


## Instructions
This script depends on the following packages:
- Pandas
- Numpy
- Scikit-Image
- Matplotlib
- OS
- Math

To run, save the script to the same directory as the images to analyzed and launch from the terminal.
The script assumes you will acknowledge/close or save the reference images generated.
