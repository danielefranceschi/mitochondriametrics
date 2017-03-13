# imports
import string
import cv2

class ImageSaver:

    def __init__(self, destinationPath=None, filenameSuffix="decorated"):
        self.fnSuffix=filenameSuffix
        self.destPath=destinationPath

    def saveImage(self,img,aFileName):
        # TODO destpath
        parts = aFileName.split('.')
        newFileName= "".join(parts[:-1])+ '_' + self.fnSuffix + '.' + parts[-1]
        cv2.imwrite(newFileName, img)
