# import the necessary packages
import string
import cv2
import numpy as np

class ImageDecorator:

    @staticmethod
    def drawDot(img,x,y,color,size=5):
        cv2.circle(img, (int(x), int(y)), size, color, -1)

    @staticmethod
    def decorateImage(img, features, pixelsPerMetric=1, drawMidPoints=True):

        # working copy
        originalImage = img.copy()

        # loop over the features individually
        for om in features:

            box=om.getBoundingBox()
            box2=np.array(box, dtype="int")
            cv2.drawContours(originalImage, [box2.astype("int")], -1, (0, 255, 0), 2)

            # loop over the original points and draw them
            for (x, y) in box2:
                ImageDecorator.drawDot(originalImage,x,y,(0, 0, 255))

            if drawMidPoints:
                # unpack the ordered bounding box, then compute the midpoint
                # between the top-left and top-right coordinates, followed by
                # the midpoint between bottom-left and bottom-right coordinates
                (tltrX, tltrY) = om.midPoint(om.tl, om.tr)
                (blbrX, blbrY) = om.midPoint(om.bl, om.br)

                # compute the midpoint between the top-left and top-right points,
                # followed by the midpoint between the top-right and bottom-right
                (tlblX, tlblY) = om.midPoint(om.tl, om.bl)
                (trbrX, trbrY) = om.midPoint(om.tr, om.br)

                # draw the midpoints on the image
                ImageDecorator.drawDot(originalImage,tltrX,tltrY,(255, 0, 0))
                ImageDecorator.drawDot(originalImage,blbrX,blbrY,(255, 0, 0))
                ImageDecorator.drawDot(originalImage,tlblX,tlblY,(255, 0, 0))
                ImageDecorator.drawDot(originalImage,trbrX,trbrY,(255, 0, 0))

                # draw lines between the midpoints
                cv2.line(originalImage, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
                cv2.line(originalImage, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)

            
            # get the size of the object
            (dimA, dimB) = om.scaledDimensions(pixelsPerMetric)

            # draw the object sizes on the image
            
            cv2.putText(originalImage, "{:.1f}".format(dimA),
                (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)
            cv2.putText(originalImage, "{:.1f}".format(dimB),
                (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)

        return originalImage
