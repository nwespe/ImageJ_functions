macro "Count colonies automatically" {
	dirSource = getDirectory("Choose Source Directory ");
	//dirAdj = dirSource + "Adjusted" + File.separator;
	//File.makeDirectory(dirAdj);
	dirOut = dirSource + "Outlines" + File.separator;
	File.makeDirectory(dirOut);
	allFiles = getFileList(dirSource);
	numFiles = 0;
	for (i=0; i<allFiles.length; i++) {
	    if(endsWith(allFiles[i], ".tif")){
            numFiles += 1;
	    }
	}
	showMessage("There are "+numFiles+" image files to process");
	setBatchMode(true);
	for (i=0; i<allFiles.length; i++) {
		if(endsWith(allFiles[i], ".tif")){
			showProgress(i+1, numFiles);
			open(dirSource+allFiles[i]);
			filename = File.nameWithoutExtension();
			ID = getImageID();
			run("8-bit");
			run("Duplicate...", "title=mask");
			setAutoThreshold("Default");
			run("Convert to Mask");
			setThreshold(255, 255);
			run("Create Selection");
			run("Fit Circle");
			run("Enlarge...", "enlarge=-50 pixel");
			roiManager("Add");
			selectImage(ID);
			run("Subtract Background...", "rolling=20 light");
			run("Colors...", "foreground=black background=white");
			run("Restore Selection");
			run("Clear Outside");
			setAutoThreshold("Default");
			run("Convert to Mask");
			setThreshold(255, 255);
			run("Watershed");
			run("Analyze Particles...", "size=10-Infinity pixel circularity=0.5-1.00 show=[Overlay Outlines] display clear summarize add");
			saveAs("ZIP", dirOut+filename+" outlines");
			close();
		}
	}
	selectWindow("Results");
	run("Close");
	selectWindow("Summary");
	saveAs("Text", dirSource + "Summary.txt");
	showMessage("Automatic count is finished");
}