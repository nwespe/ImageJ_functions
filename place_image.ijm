macro "place image" {
	Dialog.create("Place and Label Image");
	Dialog.addString("label:", "new");
	Dialog.addString("file:", "new");
	Dialog.addNumber("x:", 160)
	Dialog.addNumber("y:", 200)
	Dialog.show();
	label = Dialog.getString();
	file = Dialog.getString();
	x = Dialog.getNumber();
	y = Dialog.getNumber();
	// print("Arguments received are "+ sample +" "+ x +" "+ y);
	setBatchMode(true);
	open(file);
	run("Select All");
	run("Copy");
	close();
	makeRectangle(x, y, 480, 275);
	run("Paste");
	setColor(0, 0, 0);
	setFont("SansSerif", 60, "antialiased");
	setJustification("center");
	drawString(label, x-70, y+170);
}