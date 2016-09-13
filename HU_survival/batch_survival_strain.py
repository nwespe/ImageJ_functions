from ij import IJ, Macro
import java.lang.Thread as Thread
# from ij.gui import WaitForUserDialog
import glob, os

__author__ = 'Nichole Wespe'

inputDir = IJ.getDirectory("Choose Source Directory ")
outputDir = IJ.getDirectory("Choose Destination Directory ")

strain_dirs = [d for d in os.listdir(inputDir) if not d[0] == "."]

for d in strain_dirs:
    S, strain = os.path.basename(os.path.normpath(d)).split("_")
    roi_path = os.path.join(inputDir, d, "Regions")
    if not os.path.exists(roi_path):
        os.mkdir(roi_path)
    pattern = os.path.join(inputDir, d, "*.jpg")
    fileList = glob.glob(pattern)
    print "Found " + str(len(fileList)) + " montage files for strain " + strain
    if len(fileList) == 0:
        continue
    for f in fileList:
        date, well, strain, condition = os.path.basename(f).split("_")
        date = str(date)
        condition = condition.rstrip(".jpg")
        args = "date=[" + date + "] well=[" + well + "] strain =[" + strain + "] condition=[" + condition + \
               "] file=[" + f + "] path=[" + roi_path + "]"
        Macro.setOptions(Thread.currentThread(), args)
        IJ.run("analyze pixels", args)
    IJ.saveAs("Results", outputDir + "/" + strain + "_results.csv")
    IJ.selectWindow("Results")
    IJ.run("Close")
