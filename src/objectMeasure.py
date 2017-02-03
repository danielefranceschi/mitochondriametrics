# class holding the result of the object recognition
from scipy.spatial import distance as dist
from imutils import perspective
import cv2
import numpy as np

class ObjectMeasure:

    def midpoint(ptA, ptB):
           return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

    def __init__(self, c):

        # compute the rotated bounding box of the contour
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # order the points in the contour such that they appear in
        # top-left, top-right, bottom-right, and bottom-left order
        box = perspective.order_points(box)

        # unpack the ordered bounding box, then compute the midpoint
        # between the top-left and top-right coordinates, followed by
        # the midpoint between bottom-left and bottom-right coordinates
        (self.tl, self.tr, self.br, self.bl) = box
        (tltrX, tltrY) = midpoint(self.tl, self.tr)
        (blbrX, blbrY) = midpoint(self.bl, self.br)

        # compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-right and bottom-right
        (tlblX, tlblY) = midpoint(self.tl, self.bl)
        (trbrX, trbrY) = midpoint(self.tr, self.br)

        # compute the Euclidean distance between the midpoints
        self.dimA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        self.dimB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    def scaledDimensions(pixelsPerMetric=1):
        return (self.dimA / pixelsPerMetric, self.dimB / pixelsPerMetric)

    def getBoundingBox():
        return (self.tl, self.tr, self.br, self.bl)
