from ij import IJ, Macro
import java.lang.Thread as Thread
# from ij.gui import WaitForUserDialog
import glob, os

__author__ = 'Nichole Wespe'

inputDir = IJ.getDirectory("Choose Source Directory ")
outputDir = IJ.getDirectory("Choose Destination Directory ")
pattern = os.path.join(inputDir, "*Montage.jpg")
fileList = glob.glob(pattern)
print "Found " + str(len(fileList)) + " montage files."

for f in fileList: # get date, sample from filename before opening
    # get date, sample from filename before opening
    date, sample, style = os.path.basename(f).split(" ")  # style is "Montage.tif"
    date = str(date)
    path = os.path.join(outputDir, sample)
    print date + " " + sample
    args = "date=["+ date +"] sample=["+ sample +"] file=["+ f +"] path=["+ path +"]"
    Macro.setOptions(Thread.currentThread(), args)
    IJ.run("analyze pixels", args)
IJ.saveAs("Results", outputDir+"/Results.csv")
