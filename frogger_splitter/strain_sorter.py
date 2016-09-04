#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, argparse, csv, fnmatch, shutil

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


def sort_images_by_strain(data_file, montage_dir, output_dir):

    montage_files = []
    for r, d, f in os.walk(montage_dir):
        for filename in fnmatch.filter(f, '*Montage.jpg'):
            montage_files.append(os.path.join(r, filename))
    # print montage_files[:5]

    # read info file
    csv_open = open(data_file, 'rU')
    csv_reader = csv.reader(csv_open)  # columns are date, sample, strain, media - use first two to find montage file
    row1 = next(csv_reader)  # skip header row

    for row in csv_reader:  # loop over rows
        date = str(row[0])
        sample = str(row[1])
        # print 'Now matching file for ' + date + ' ' + sample
        image_file = fnmatch.filter(montage_files, '*' + date + ' ' + sample + ' *')
        if len(image_file) > 1:  # check number of files matched - should be at most one
            print 'More than one montage file found for '+date+' '+sample
            continue
        elif len(image_file) == 0:
            print 'No montage file found for '+date+' '+sample
            continue
        # else:
        #    print 'Match found for '+date+' '+sample+': '+image_file[0]
        strain = str(row[2])
        medium = str(row[3])
        strain_directory = os.path.join(output_dir, 'Strain_'+strain)
        if not os.path.exists(strain_directory):  # create one if not found
            os.makedirs(strain_directory)
        # copy file with new name and place into folder for strain
        dest = os.path.join(strain_directory, date+'_'+sample+'_'+strain+'_'+medium+'.jpg')
        shutil.copy(image_file[0], dest)


def rename_plate_file(image_dir):

    for f in os.listdir(image_dir):
        filename = os.path.basename(f)
        #try:
        date, time, rows, columns_tif = str.split(filename)
        #except:
        #    try: date, time, rows, columns, rep_tif = str.split(filename)
        #    except:
        #        pass
        columns = columns_tif.rstrip('.tif')
        dest = os.path.join(image_dir, date + ' ' + rows + ' ' + columns + ' ' + time + '.tif')
        # print os.path.join(image_dir, f), dest
        os.rename(os.path.join(image_dir, f), dest)


def main():
    parser = argparse.ArgumentParser(description='Specify a data file to be sorted and a location of the strain files.')
    parser.add_argument('-f', '--data_file', required=True,
                        help='Full path to data file.')
    parser.add_argument('-m', '--montage_directory', default='./',
                        help='Full path to directory containing montages. Images can be in subdirectories.')
    parser.add_argument('-o', '--output_directory', default='./',
                        help='Full path to output directory for strain folders.')
    args = parser.parse_args()
    data_file = args.data_file
    montage_dir = args.montage_directory
    output_dir = args.output_directory
    sort_images_by_strain(data_file, montage_dir, output_dir)


if __name__ == "__main__":
    main()

