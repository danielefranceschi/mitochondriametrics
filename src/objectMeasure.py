# class holding the result of the object recognition
from scipy.spatial import distance as dist
from imutils import perspective
import cv2
import numpy as np

class ObjectMeasure:

    def __init__(self, c):

        # compute the rotated bounding box of the contour
        box = cv2.minAreaRect(c)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # order the points in the contour such that they appear in
        # top-left, top-right, bottom-right, and bottom-left order
        box = perspective.order_points(box)

        # unpack the ordered bounding box, then compute the midpoint
        # between the top-left and top-right coordinates, followed by
        # the midpoint between bottom-left and bottom-right coordinates
        (self.tl, self.tr, self.br, self.bl) = box
        (tltrX, tltrY) = self.midPoint(self.tl, self.tr)
        (blbrX, blbrY) = self.midPoint(self.bl, self.br)

        # compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-right and bottom-right
        (tlblX, tlblY) = self.midPoint(self.tl, self.bl)
        (trbrX, trbrY) = self.midPoint(self.tr, self.br)

        # compute the Euclidean distance between the midpoints
        self.dimA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        self.dimB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    def scaledDimensions(self,pixelsPerMetric=1):
        return (self.dimA / pixelsPerMetric, self.dimB / pixelsPerMetric)

    def getBoundingBox(self):
        return (self.tl, self.tr, self.br, self.bl)
    
    @staticmethod
    def midPoint(ptA, ptB):
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)