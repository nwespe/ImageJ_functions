macro "Count colonies automatically" {
	dirSource = getDirectory("Choose Source Directory ");
	dirAdj = dirSource + "Adjusted" + File.separator;
	File.makeDirectory(dirAdj);
	dirOut = dirSource + "Outlines" + File.separator;
	File.makeDirectory(dirOut);
	list = getFileList(dirSource);
	print(list.length);
	setBatchMode(true);
	for (i=0; i<list.length; i++) {
		if(endsWith(list[i], ".tif")){
			showProgress(i+1, list.length);
			open(dirSource+list[i]);
			filename = File.nameWithoutExtension();
			ID = getImageID();
			run("8-bit");
			run("Duplicate...", "title=mask");
			setAutoThreshold("Default");
			//run("Threshold...");
			run("Convert to Mask");
			setThreshold(255, 255);
			run("Create Selection");
			run("Fit Circle");
			run("Enlarge...", "enlarge=-50 pixel");
			roiManager("Add");
			selectImage(ID);
			run("Subtract Background...", "rolling=20 light");
			saveAs("TIFF", dirAdj+filename+" adjusted");
			run("Restore Selection");
			run("Clear Outside");
			setAutoThreshold("Default");
			//run("Threshold...");
			run("Convert to Mask");
			setThreshold(255, 255);
			run("Watershed");
			run("Analyze Particles...", "size=10-Infinity circularity=0.5-1.00 show=[Overlay Outlines] display clear summarize add");
			saveAs("ZIP", dirOut+filename+" outlines");
			close();
		}
		selectWindow("Summary");
		saveAs("Text", dirSource + "Summary.txt");
	}
}