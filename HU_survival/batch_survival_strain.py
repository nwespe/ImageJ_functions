from ij import IJ, Macro
import java.lang.Thread as Thread
# from ij.gui import WaitForUserDialog
import glob, os

__author__ = 'Nichole Wespe'

inputDir = IJ.getDirectory("Choose Source Directory ")
outputDir = IJ.getDirectory("Choose Destination Directory ")

for d in os.listdir(inputDir):
    S, strain = os.path.basename(os.path.normpath(d)).split("_")
    pattern = os.path.join(inputDir, d, "*.jpg")
    print pattern
    fileList = glob.glob(pattern)
    print "Found " + str(len(fileList)) + " montage files for strain " + strain
    if len(fileList) == 0:
        continue
    for f in fileList:
        date, sample, strain, condition = os.path.basename(f).split("_")
        date = str(date)
        path = os.path.join(outputDir, sample)
        condition = condition.rstrip(".jpg")
        print date + " " + sample + " " + condition
        args = "date=[" + date + "] sample=[" + sample + "] strain =[" + strain + "] condition=[" + condition + \
               "] file=[" + f + "] path=[" + path + "]"
        Macro.setOptions(Thread.currentThread(), args)
        IJ.run("analyze pixels", args)
    IJ.saveAs("Results", outputDir + "/" + strain + "_results.csv")
    IJ.selectWindow("Results")
    IJ.run("Close")
