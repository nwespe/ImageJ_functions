import java.lang.Thread as Thread
from ij import IJ, Macro
# from ij.gui import WaitForUserDialog
import glob, os

__author__ = 'Nichole Wespe'

inputDir = IJ.getDirectory("Choose Source Directory ")
outputDir = IJ.getDirectory("Choose Destination Directory ")
pattern = os.path.join(inputDir, "*Montage.tif")
fileList = glob.glob(pattern)
print "Found " + str(len(fileList)) + " montage files."

row_dict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}

currentDate = "blank"
expt_imp = None
for f in fileList:
	# get date, sample from filename before opening
	date, sample, style = os.path.basename(f).split(" ") # style is "Montage.tif"
	date = str(date)
	print date +" "+ sample
	r = row_dict[sample[0]]
	c = int(sample[1:])-1
	x = r*660+180
	y = c*320+30
	if currentDate != date:
		print "Found new experiment: " + date
		if expt_imp:
			print "Saving and closing previous experiment."
			IJ.selectWindow(expt_name)
			expt_path = os.path.join(outputDir, expt_name)
			IJ.saveAs("Tiff", expt_path)
			expt_imp.close()
		currentDate = date
		print "Current date is now " + currentDate
		expt_name = " ".join([currentDate, "Results.tif"])
		IJ.newImage(expt_name, "16-bit white", 5280, 3885, 1)
		expt_imp = IJ.getImage()
	args = "label=["+sample +"] file=["+ f +"] x="+ str(x) +" y="+ str(y)
	Macro.setOptions(Thread.currentThread(), args)
	IJ.run("place image", args)

IJ.selectWindow(expt_name)
expt_path = os.path.join(outputDir, expt_name)
IJ.saveAs("Tiff", expt_path)

expt_imp.close()