from ij import IJ
# from ij.gui import WaitForUserDialog
import glob, os

__author__ = 'Nichole Wespe'

inputDir = IJ.getDirectory("Choose Source Directory ")
pattern = os.path.join(inputDir, "*.tif")
fileList = glob.glob(pattern)
print "Found " + str(len(fileList)) + " tiff files to process."

for f in fileList:
	IJ.open(f)
	IJ.run("plate cropper")
	imp = IJ.getImage()
	imp.close()