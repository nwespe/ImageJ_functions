macro "save ROI" {
	Dialog.create("Save ROI");
	Dialog.addString("sample:", "new");
	Dialog.addString("path:", "new");
	Dialog.addNumber("x:", 160);
	Dialog.addNumber("y:", 200);
	Dialog.addNumber("w:", 130);
	Dialog.addNumber("h:", 480);
	Dialog.show();
	sample = Dialog.getString();
	path = Dialog.getString();
	x = Dialog.getNumber();
	y = Dialog.getNumber();
	w = Dialog.getNumber();
	h = Dialog.getNumber();
	// print("Values received are "+sample+" "+path+" "+x+" "+y+" "+w+" "+h);
	setBatchMode(true);
	makeRectangle(x, y, w, h);
	run("Copy");
	newImage(sample, "8-bit black", w, h, 1);
	run("Paste");
	saveAs("Jpeg", path);
	close();
}