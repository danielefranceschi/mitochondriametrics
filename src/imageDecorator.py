# import the necessary packages
import string
import cv2

class ImageDecorator:

    def drawDot(img,x,y,color,size=5):
        cv2.circle(img, (int(x), int(y)), size, color, -1)

    def decorateImage(img, features, pixelsPerMetric=1, drawMidPoints=False):

        # working copy
        originalImage = img.copy()

        # loop over the features individually
        for om in features:

            box=om.getBoundingBox()
            cv2.drawContours(originalImage, [box.astype("int")], -1, (0, 255, 0), 2)

            # loop over the original points and draw them
            for (x, y) in box:
                drawDot(originalImage,x,y,(0, 0, 255))

            if drawMidPoints:
                # unpack the ordered bounding box, then compute the midpoint
                # between the top-left and top-right coordinates, followed by
                # the midpoint between bottom-left and bottom-right coordinates
                (tltrX, tltrY) = om.midpoint(tl, tr)
                (blbrX, blbrY) = om.midpoint(bl, br)

                # compute the midpoint between the top-left and top-right points,
                # followed by the midpoint between the top-right and bottom-right
                (tlblX, tlblY) = om.midpoint(tl, bl)
                (trbrX, trbrY) = om.midpoint(tr, br)

                # draw the midpoints on the image
                drawDot(originalImage,tltrX,tltrY,(255, 0, 0))
                drawDot(originalImage,blbrX,blbrY,(255, 0, 0))
                drawDot(originalImage,tlblX,tlblY,(255, 0, 0))
                drawDot(originalImage,trbrX,trbrY,(255, 0, 0))

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
