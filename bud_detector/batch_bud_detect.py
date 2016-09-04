from ij import IJ, Macro
import java.lang.Thread as Thread
# from ij.gui import WaitForUserDialog
import glob, os

__author__ = 'Nichole Wespe'

inputDir = IJ.getDirectory("Choose Source Directory ")
outputDir = IJ.getDirectory("Choose Destination Directory ")

for d in os.listdir(inputDir):
    strain = os.path.basename(os.path.normpath(d)).split("_")
    pattern = os.path.join(inputDir, d, "*.tif")
    print pattern
    fileList = glob.glob(pattern)
    print "Found " + str(len(fileList)) + " microscopy files to analyze."
    if len(fileList) == 0:
        continue
    n=0
    for f in fileList:
        date, sample, strain, condition = os.path.basename(f).split("_")
        date = str(date)
        path = os.path.join(outputDir, sample)
        condition = condition.rstrip(".jpg")
        print date + " " + sample + " " + condition
        args = "date=[" + date + "] sample=[" + sample + "] strain =[" + strain + "] condition=[" + condition + \
               "] file=[" + f + "] path=[" + path + "] number=[" + n + "]"
        Macro.setOptions(Thread.currentThread(), args)
        IJ.run("detect buds", args)
        n+=1
    IJ.saveAs("Results", outputDir + "/" + strain + "_results.csv")
    IJ.selectWindow("Results")
    IJ.run("Close")
