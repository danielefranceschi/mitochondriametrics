# imports
import string
import cv2

class ImageSaver:

    def __init__(self, destinationPath=None, filenameSuffix="decorated"):
        self.fnSuffix=filenameSuffix
        self.destPath=destinationPath

    def appendSuffixToFilename(aFileName, aSuffix):
        parts = aFileName.split('.')
        return "".join(parts[:-1])+ '_' + aSuffix + '.' + parts[-1]

    def saveImage(img,aFileName):
        # TODO destpath
        cv2.SaveImage(appendSuffixToFilename(aFileName, fnSuffix), img)
