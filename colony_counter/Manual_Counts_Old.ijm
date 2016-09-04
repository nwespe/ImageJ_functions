macro "Count colonies manually" {
	dirSource = getDirectory("Choose Directory of Original Files ");
	dirAdj = dirSource + "Adjusted" + File.separator;
	dirOut = dirSource + "Outlines" + File.separator;
	dirManual = dirSource + "Manual Counts" + File.separator;
	File.makeDirectory(dirManual);
	list = getFileList(dirOut);
	newColonies = newArray(list.length);
	for (i=0; i<list.length; i++) {
		showProgress(i+1, list.length);
		open(dirOut+ "/" +list[i]);
		run("To ROI Manager");
		zipName = list[i];
		tifName = replace(zipName, "outlines.zip", "adjusted.tif");
		open(dirAdj+tifName);	
		run("From ROI Manager");
		setTool("multipoint");
		waitForUser("Click on unmarked colonies and click OK when finished");
		numPoints=0;
		if (selectionType()!=-1) {
			getSelectionCoordinates(x, y);
			numPoints = x.length;
		}
		newColonies[i] = numPoints;
		filename = replace(zipName, "outlines.zip", "");
		print(filename + "," + newColonies[i]);
		clickName = replace(zipName, "outlines.zip", "clicked.tif");
		run("Flatten");
		saveAs("TIFF", dirManual+clickName);
		roiManager("Reset");
		while (nImages>0) { 
	          selectImage(nImages); 
	          close(); 
	      }
	saveAs("Text", dirManual+"Clicked colonies");
	}
}