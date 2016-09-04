macro "detect buds" {
	Dialog.create("Detect Buds");
	Dialog.addString("date:", "new");
	Dialog.addString("strain:", "new");
	Dialog.addString("condition:", "new");
	Dialog.addString("time:", "new");
	Dialog.addString("file:", "new");
	Dialog.addString("path:", "new");
	Dialog.addString("number:", "new");
	Dialog.show();
	date = Dialog.getString();
	strain = Dialog.getString();
	condition = Dialog.getString();
	time = Dialog.getString();
	file = Dialog.getString();
	path = Dialog.getString();
	number = Dialog.getString();
	setBatchMode(true);
	open(file);
	run("Options...", "iterations=1 count=1 black");
	main=File.nameWithoutExtension();
	run("Threshold...");
	setThreshold(100, 255);
	setOption("BlackBackground", true);
	run("Convert to Mask");
	run("Analyze Particles...", "size=50-600 show=Overlay display exclude clear summarize add");
    saveAs("Jpeg", path+"/"+main+"_numbered.jpg");
    bud=0;
    nobud=0;
    check=0;
    for (i=0 ; i<roiManager("count"); i++) {
        roiManager("select", i);
        run("To Bounding Box");
        run("Enlarge...", "enlarge=10");
        run("Duplicate...", "title="+i);
        circ=getResult("Circ.", i);
        if (circ>=0.85) {
            saveAs(path+"/nobud/"+main+"_"+i+".jpg");
            nobud++;
        } else if (circ<0.85 && circ>0.65) {
            saveAs(path+"/check/"+main+"_"+i+".jpg");
            check++;
        } else if (circ<=0.65) {
            saveAs(path+"/budded/"+main+"_"+i+".jpg");
            bud++;
        }
    IJ.renameResults("ROI Results");
    saveAs("ROI Results", path + "/" + main + "_roi_results.csv");
    selectWindow("ROI Results");
    run("Close");
    setResult("Label", number, main);
    setResult("circ >= 0.85", number, nobud);
    setResult("circ <= 0.65", number, bud);
    setResult("0.65 < circ < 0.85", number, check);
    IJ.renameResults("Cell counts");
}

