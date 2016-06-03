#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, argparse, csv, glob, fnmatch, shutil
# from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea

__author__ = 'Nichole Wespe'


class Image(object):
    """Each image file has attributes path, date, sample ID, strain, and medium.
    """
    def __init__(self, path, date, ID, strain, medium, x_loc):
        self.path = path
        self.date = date
        self.ID = ID
        self.strain = strain
        self.medium = medium
        self.x_loc = x_loc

#run for each experiment separately
def main():
    parser = argparse.ArgumentParser(description='Specify a data file to be sorted and a location of the strain files.')
    parser.add_argument('-f', '--data_file', required=True, help='Full path to data file.')
    parser.add_argument('-m', '--montage_directory', default='./', help='Full path to directory containing montages.')
    parser.add_argument('-o', '--output_directory', default='./', help='Full path to output directory.')
    args = parser.parse_args()
    data_file = args.data_file
    montage_dir = args.montage_directory
    output_dir = args.output_directory
    sort_images_by_strain(data_file, montage_dir, output_dir)


def sort_images_by_strain(data_file, montage_dir, output_dir):

    montage_files = glob.glob(os.path.join(montage_dir, '*Montage.tif'))
    # read info file
    csv_open = open(data_file, 'rU')
    csv_reader = csv.reader(csv_open) ## columns are date, sample, strain, media - use first two to find montage file
    row1 = next(csv_reader)  ## skip header row

    for row in csv_reader:  ## loop over rows
        date = str(row[0])
        sample = str(row[1])
        image_file = fnmatch.filter(montage_files, date+' '+sample+'*')  ## match to file in montage_files list
        if len(image_file) > 1:  ## check number of files matched - should be at most one
            print 'More than one montage file found for '+date+' '+sample
            continue
        elif len(image_file) == 0:
            print 'No montage file found for '+date+' '+sample
            continue
        strain = str(row[2])
        medium = str(row[3])
        strain_directory = glob.glob(os.path.join(output_dir, 'Strain_'+strain))
        if len(strain_directory) == 0:  ## create one if not found
            os.makedirs(strain_directory)
        # copy file with new name and place into folder for strain
        dest = os.path.join(strain_directory, date+'_'+sample+'_'+strain+'_'+medium+'.tif')
        shutil.copy(image_file, dest)


def compile_strain_files(strains_dir, output_dir):
    media_dict = {'YPD': 580, '0.5 M NaCl': 1240, '0.5 M KCl': 1900, '1 M sorbitol': 2560}  # x location in pixels
    for d in glob.glob(os.path.join(strains_dir, 'Strain_*/')): # for each strain directory containing tiffs
        image_files = os.listdir(d)
        current_strain = os.path.basename(os.path.normpath(d)).split('_')[1]
        dates = set(); media = set()
        image_objects = []
        for image in image_files:
            date, sample, strain, medium = os.path.basename(image).split('_')
            if strain != current_strain:
                print 'Mismatched strain file found: '+ str(image)
                continue
            dates.add(date)
            media.add(medium)
            x_loc = media_dict[medium]
            image_objects.append(Image(os.path.abspath(image), date, sample, strain, medium, x_loc)) # initialize Image objects
        (h, w) = (len(dates)*655+400, len(media)*660+400) # determine size of compilation file
        ax, fig = plt.subplots(1, 1)  # initialize plot
        # add image files by date
        img_y_loc = 400
        for curr_date in sorted(dates):
            date_set = [f for f in image_objects if f.date == curr_date]  # get image files from image_objects list
            date_set.sort(key=lambda x: x.ID[1:])  # now sort by number in sample ID - letter doesn't matter
            # first half of samples get first y_loc, second half get second y_loc (+ 320)
            i = 0
            while i < len(date_set)/2:
                img = date_set[i] # place image files using img.x_loc, img_y_loc
                ax.imshow(img.path, extent=[img.x_loc, img.x_loc+480, img_y_loc+275,
                                            img_y_loc]) # not sure about pixels as coordinates
                i += 1
            img_y_loc += 320
            while i < len(date_set):
                img = date_set[i]  # place image files using img.x_loc, img_y_loc
                ax.imshow(img.path, extent=[img.x_loc, img.x_loc + 480, img_y_loc + 275,
                                            img_y_loc])  # not sure about pixels as coordinates
                i += 1
            img_y_loc += 335 # change after placing all images

        plt.draw()
'''     plt.savefig('destination_path.eps', format='eps', dpi=1000)

    strain_file = glob.glob(os.path.join(args.output_directory, strain+'*.tif')) ## find strain master file
    if len(strain_file) == 0:  ## or create one if not found
        # make new file - set y_loc for first sample
    elif len(strain_file) > 1:  ## check number of files matched - should be at most one
        print 'More than one strain file found for ' + strain + '. Using file '+ str(image_file[0])
'''

    #

    #   ## this defines what column to place the sample results in

    # montage = plt.imread(

    # send strain_file[0] to imagej to be opened and modified
    # send date, image file, and x_loc to imagej macro for placing image file in strain file

#	macro { - adapt “place image” macro
#		open montage file
#		open master sheet
#		add montage image and date / media - get width and height of image, adjust to include new image
# x location based on media type,
# y location based on number of samples in image
# (get image size, expand by x and paste onto end - only for ypd samples?)
#	}
'''

