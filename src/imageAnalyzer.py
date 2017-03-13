# based on http://www.pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/

# import the necessary packages
from imutils import contours
import cv2

class ImageAnalyzer:

    def __init__(self, minimumFeatureSize=1024):
        self.minimumSize=minimumFeatureSize

    def measureImage(self,imgFileName):

        # load the image, convert it to grayscale, and blur it slightly
        image = cv2.imread(imgFileName)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (11, 11), 0)

        # dump out background
        ret,th4 = cv2.threshold(gray,64,255,cv2.THRESH_TOZERO)
        
        # perform a dilation + erosion to close gaps in between object edges
        dilated = cv2.dilate(th4, None, iterations=3)
        eroded = cv2.erode(dilated, None, iterations=5)

        # finally remove noise
        final = cv2.medianBlur(eroded, 31)
        
        # find contours in the edge map
        cnts = cv2.findContours(final.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # sort the contours from left-to-right
        (cnts, _) = contours.sort_contours(cnts[1])

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
