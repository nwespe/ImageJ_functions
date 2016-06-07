macro "convert filetype" {
	Dialog.create("Convert file from TIFF to JPEG");
	Dialog.addString("input:", "new");
	Dialog.addString("output:", "new");
	Dialog.show();
	input = Dialog.getString();
	output = Dialog.getString();
	setBatchMode(true);
	open(input);
	saveAs("Jpeg", output);
	close();
}