#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, glob
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

__author__ = 'Nichole Wespe'


media_dict = {'YPD': 0, '0.5 M NaCl': 1, '0.5 M KCl': 2, '1 M sorbitol': 3}


class Sample(object):

    def __init__(self, expt_date, wellID, medium, mfile):
        self.date = expt_date
        self.wellID = wellID
        self.medium = medium
        self.mfile = mfile
        self.image = Image(mfile)
        self.image.drawHeight = 1.25 * inch * self.image.drawHeight / self.image.drawWidth
        self.image.drawWidth = 1.25 * inch


class Experiment(object):

    def __init__(self, expt_date, samples):
        self.date = expt_date
        self.samples = samples  # list of Sample objects with this date
        self.date_tuples = []
        self.ordered_samples = []

    def sort_samples(self, samples, r):  # now determine replicate number, row, and column of each sample
        rows = set()
        for s in samples:
            other_samples = filter(lambda i: i != s, samples)
            rep_match = filter(lambda x: x.medium == s.medium, other_samples)[0]
            s.replicate = sorted([s.wellID, rep_match.wellID]).index(s.wellID)  # need to sort by samples by wellID
            s.row = r + s.replicate  # assign row to sample
            s.col = media_dict[s.medium]  # assign column to sample
            s.info = (s.row, s.col, s)  # create tuple for sorting later
            self.date_tuples.append(s.info)
            rows.add(s.row)  # get row numbers
            # print 'Sample '+str(s.wellID)+' is in row '+str(s.row)+' and column '+str(s.col)
        self.date_tuples.sort()  # order samples into list based on row and column
        sorted_samples = [i[2] for i in self.date_tuples]  # get only sample objects from tuples
        first, second = sorted(list(rows))
        row1_first = [[f.wellID, f.image] for f in sorted_samples if f.row == first]
        row1 = []
        for s in row1_first:  # flatten list for each item to be in separate cell of table
            row1.extend(s)
        row2_first = [[f.wellID, f.image] for f in sorted_samples if f.row == second]
        row2 = []
        for s in row2_first:
            row2.extend(s)
        self.ordered_samples = [[self.date] + row1,  # add date to start of list for each row
                                [self.date] + row2]


def create_sample_list(strain_directory):
    current_strain = os.path.basename(os.path.normpath(strain_directory)).split('_')[1]
    date_set = set()
    media_set = set()
    image_files = os.listdir(strain_directory)
    all_samples = []
    for mfile in image_files:
        mfile = strain_directory + '/' + mfile
        date, wellID, strain, medium = os.path.basename(mfile).split('_')
        medium = medium.strip('.jpg')
        if strain != current_strain:
            print 'Mismatched strain file found: ' + str(image)
            continue
        date_set.add(date)
        dates = sorted(list(date_set))
        media_set.add(medium)
        # convert media set to list and arrange by media_dict
        media = [0]*len(media_set)  # initialize list of 0s according to number of different media
        for m in media_set:
            i = media_dict[m]
            media[i] = m  # place media in list according to index from media_dict
        all_samples.append(Sample(date, wellID, medium, mfile))
    return current_strain, dates, media, all_samples


def group_by_expt(dates, all_samples):
    experiments = []
    r = 0
    for current_date in dates:
        samples_subset = [s for s in all_samples if s.date == current_date]
        expt = Experiment(current_date, samples_subset)
        expt.sort_samples(samples_subset, r)
        experiments.append(expt)
        r += 2  # increment by 2 because each date should have two samples and therefore two rows
    return experiments


def create_report(strain, output_directory, media, experiments):

    doc = SimpleDocTemplate(os.path.join(output_directory, strain + '_report.pdf'),
                            pagesize=landscape(letter))  # initialize canvas with filename and pagesize
    # width, height = letter  # can define margins relative to these variables
    elements = []

    styles = getSampleStyleSheet()
    title = 'Strain yNMC' + strain + ' Hydroxyurea Survival Assay Results'
    elements.append(Paragraph(title, styles['Normal']))  # add title to doc
    elements.append(Spacer(1,24))  # I think the options are (w,h) in points

    empty_cells = ['']*len(media)  # need to add empty cell before each member of media list and one at beginning
    row1_tuples = zip(empty_cells, media)
    row1 = [i for s in row1_tuples for i in s]
    data = [['Date:'] + row1]

    for expt in experiments:
        data.extend(expt.ordered_samples)

    t = Table(data,  # data is sequence of sequences of cell values (strings or Flowables)
              colWidths=None, rowHeights=None, hAlign='LEFT', style=None, spaceBefore=None, spaceAfter=None)
    t.setStyle(TableStyle(
        [('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]
    ))
    elements.append(t)
    doc.build(elements)


def main(input_dir, output_dir):  # receives arguments strain directory and output directory

    strain_directory = input_dir
    output_directory = output_dir
    strain, dates, media, all_samples = create_sample_list(strain_directory)
    experiments = group_by_expt(dates, all_samples)
    create_report(strain, output_directory, media, experiments)


def batch_compile_reports(strains_dir, output_dir):
    for d in glob.glob(os.path.join(strains_dir, 'Strain_*/')): # for each strain directory containing images
        # print 'Now creating report for strain samples in ' + str(d)
        main(d, output_dir)
    # strain_file = glob.glob(os.path.join(args.output_directory, strain+'*.jpg')) ## find strain master file
    # print strain_file

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

