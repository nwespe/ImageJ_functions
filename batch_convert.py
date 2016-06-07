from ij import IJ, Macro
import java.lang.Thread as Thread
# from ij.gui import WaitForUserDialog
import glob, os

__author__ = 'Nichole Wespe'

inputDir = IJ.getDirectory("Choose Source Directory ")
outputDir = IJ.getDirectory("Choose Destination Directory ")
pattern = os.path.join(inputDir, "*.tif")
fileList = glob.glob(pattern)
print "Found " + str(len(fileList)) + " tiff sample files to convert."

for f in fileList:
    basename = os.path.basename(f).strip('.tif')
    output_name = basename + '.jpg'
    path = os.path.join(outputDir, output_name)
    args = "input=[" + f + "] output=[" + path + "]"
    Macro.setOptions(Thread.currentThread(), args)
    IJ.run("convert filetype", args)