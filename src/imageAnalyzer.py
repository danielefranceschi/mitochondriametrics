# based on http://www.pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/

# import the necessary packages
from imutils import contours
import cv2

class ImageAnalyzer:

    def __init__(self, minimumFeatureSize=100):
        self.minimumSize=minimumFeatureSize

    def measureImage(imgFileName):

        # load the image, convert it to grayscale, and blur it slightly
        image = cv2.imread(imgFileName)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # perform edge detection, then perform a dilation + erosion to
        # close gaps in between object edges
        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        # find contours in the edge map
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # sort the contours from left-to-right
        (cnts, _) = contours.sort_contours(cnts)

        # initialize result list
        result=[]

        # loop over the contours individually
        for c in cnts:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(c) < self.minimumSize: continue
            # create the single object measure
            om=ObjectMeasure(c)
            # add it to the result list
            result.append(om)

        return result
