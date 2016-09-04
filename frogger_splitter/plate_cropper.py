from ij import IJ, ImagePlus, Macro
import java.lang.Thread as Thread
from ij.gui import WaitForUserDialog
import glob, os

__author__ = 'Nichole Wespe'

imp = IJ.getImage()
directory = IJ.getDirectory("image")
f = str(imp.getTitle())
date, rows, columns, time_tif = str.split(f)  # deconstruct filename
time = time_tif.replace('tif','jpg')  # need to remove .tif from time
row_IDs = list(6*rows[0] + 6*rows[1])
column_IDs = [str(i) for i in 2*(range(int(columns[0]), int(columns[0]) + 6))]
zipped = zip(row_IDs, column_IDs)
sample_names = ["".join(values) for values in zipped]


IJ.setMinAndMax(1900, 11717) # adjust brightness and contrast
IJ.run("Apply LUT")
IJ.makeRectangle(200, 50, 730, 950) # initialize selection
dial = WaitForUserDialog("Adjust selection area")
dial.show() # ask user to place selection appropriately
IJ.run("Crop")
adjDir = os.path.join(directory, "Adjusted")
if not os.path.exists(adjDir):
	os.mkdir(adjDir)
adjImage = os.path.join(adjDir, "Adj " + f)
IJ.saveAs("Jpeg", adjImage)

## make ROI list
w = 130
h = 480
x_vals = 2*[10, 128, 246, 360, 478, 596]
y1 = 0
y2 = 470
y_vals = [y1, y1, y1, y1, y1, y1, y2, y2, y2, y2, y2, y2]
ROIs = zip(x_vals, y_vals)

# for region in ROIs:
subDir = os.path.join(directory, "Individual")
if not os.path.exists(subDir):
	os.mkdir(subDir)

## call separate macro to run in batch mode and send parameters as options - x, y, w, h, slice_name, path_name
i = 0
for x, y in ROIs:
	slice_name = " ".join([date, sample_names[i], time])
	path_name = os.path.join(subDir, slice_name)
	args = "sample=["+slice_name +"] path=["+ path_name +"] x="+ str(x) +" y="+ str(y) +" w="+ str(w) +" h="+ str(h)
	Macro.setOptions(Thread.currentThread(), args)
	IJ.run("save ROI", args)
	i += 1