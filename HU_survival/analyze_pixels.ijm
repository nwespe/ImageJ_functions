macro "analyze pixels" {
	Dialog.create("Analyze Pixels");
	Dialog.addString("date:", "new");
	Dialog.addString("well:", "new");
	Dialog.addString("strain:", "new");
	Dialog.addString("condition:", "new");
	Dialog.addString("file:", "new");
	Dialog.addString("path:", "new");
	Dialog.show();
	date = Dialog.getString();
	well = Dialog.getString();
	strain = Dialog.getString();
	condition = Dialog.getString();
	file = Dialog.getString();
	path = Dialog.getString();
	setBatchMode(true);
	open(file);
	run("Set Measurements...", "area redirect=None decimal=3");
	run("Options...", "iterations=1 count=1 black");
	main=getTitle();
	name=File.nameWithoutExtension();
	region_image = name+"_regions.jpg";
	newImage(region_image, "RGB white", 480, 275, 1);
	colors=newArray("red", "yellow", "blue", "green");
	selectWindow(main);
	for (y=0; y<150; y+=145) // y vals are 0, 145
	{
	    if (y==0)
	        time="start";
	    else
	        time="end";
	    makeRectangle(0, y, 480, 130);
	    run("Duplicate...", "title="+time);
	    run("Threshold...");
	    setThreshold(100, 255);
	    setOption("BlackBackground", true);
	    run("Convert to Mask");
	    i=0;
	    for (x=10; x<360; x+=115) // x vals are 10, 125, 240, 355
	    {
	    	makeRectangle(x, 0, 125, 130);
	    	roiManager("Add");
	    	roiManager("Select", i);
            roiManager("Set Color", colors[i]);
            roiManager("Set Line Width", 0);
            run("Add Selection...");
            run("Hide Overlay");
			run("Duplicate...", "title="+i);
            run("Invert");
	        run("Create Selection");
	        run("Measure");
	        if (getResult("Area")==16250) // total image area
	        	setResult("Area", nResults-1, "0"); // there was no selection
	        setResult("Dilution", nResults-1, i+1);
	        setResult("Date", nResults-1, date);
	        setResult("Well", nResults-1, well);
	        setResult("Strain", nResults-1, strain);
	        setResult("Condition", nResults-1, condition);
	        setResult("Time", nResults-1, time);
	        close(); // closes spot image
	        i++;
	        selectWindow(time);
	    }
	    roiManager("Show All");
        run("Flatten");
        run("Select All");
        run("Copy");
        close(); // closes flattened image (start or end)
        close(time);
        roiManager("Select All");
        roiManager("Delete");
        selectWindow(region_image); // save thresholded image with rois marked
        makeRectangle(0, y, 480, 130);
	    run("Paste");
	    selectWindow(main);
	}
	close(); // closes montage image
	saveAs("Jpeg", path+"/"+region_image);
	close(); // closes thresholded image
}