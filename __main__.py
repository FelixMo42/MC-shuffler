## SETTINGS ##

TopPadding = 100
SidePadding = 30

PageWidth = 612
PageHeight = 1008

FontSize = 8

Scale = 0.64

TestIdStart = 1
NumTest = 15

## END SETTINGS ##

import xlrd
import fitz
import glob
import csv
import shutil
import os
import zipfile
import random
from PIL import Image, ImageOps

def addColumnToCSV(src, col):
    data = []

    with open(src, "r") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            # append the corresponding item from the collumn
            row.append(col[reader.line_num - 1])

            # append this row to the data
            data.append(row)

    with open(src, 'w+') as csvfile:
        writer = csv.writer(csvfile)

        for row in data:
            writer.writerow(row)

def exportTest(out=".", name="test"):
    def addQuestion(src):
        nonlocal questionCounter
        nonlocal position

        # increase the current count of question by 1
        questionCounter += 1

        # load the image
        pix = fitz.Pixmap(src)

        # scale down the width and height
        width = pix.width * Scale
        height = pix.height * Scale

        # is their enough space left on this page for the question?
        if (position + height > PageHeight - TopPadding):
            # reset the position to the top of the page
            position = TopPadding

            # we need a new page
            pdf.newPage(-1, PageWidth, PageHeight)

        # coordinates of question 
        X0 = SidePadding
        Y0 = position
        X1 = PageWidth - SidePadding
        Y1 = position + 20 + height

        # get last page
        page = pdf[-1]

        # add the problem number 
        page.insertText(fitz.Point(X0 + 10, Y0 + FontSize + 10), str(questionCounter), fontsize=FontSize)

        # insert the picture of the multiple choice question
        page.insertImage(fitz.Rect(
            X0 + 50        , Y0 + 10,
            X0 + 50 + width, Y0 + 10 + height
        ), pixmap=pix)

        # draw the rectang around the question
        page.drawRect( fitz.Rect(X0, Y0, X1, Y1) )

        # shift down the position to the end of this question
        position = Y1

    # creat the output directory if it dosent exist
    if not os.path.exists(out):
        os.makedirs(out)

    # how many question we have
    questionCounter = 0

    # were on the last page a new question should be added
    position = TopPadding

    # load in the questions
    questions = loadRandomizedQuestions("data/answers.xlsx")

    # create a new pdf
    pdf = fitz.open()

    # add a page to the begining
    pdf.newPage(-1, PageWidth, PageHeight)

    # add a bunch of questions
    for question in questions:
        addQuestion(f"tmp/{str(int(question[0]))}.PNG")

    # save the pdf
    pdf.save(f"{out}/{name}.pdf")

    # add the questions to the awnser key
    addColumnToCSV(f'{out}/key.csv', [str(name), *map(lambda question : question[1], questions)])

def openSheet(src, sheet):
    # load in the awser from an exel sheet
    doc = xlrd.open_workbook(src)

    # get the sheet with the awsers on it
    return doc.sheet_by_name(sheet)

def createAwnserKey(out, src, sheet="Sheet1"):
    awnser = openSheet(src, sheet)

    with open(out, 'w+') as csvfile:
        writer = csv.writer(csvfile)

        # add an empty header row
        writer.writerow([ " " ])

        # right in all the numbers
        for i in range(awnser.nrows):
            writer.writerow([ i + 1 ])

def getAllInFolder(src, ext):
    # get the list of files
    files = os.listdir(src)

    # return a filter list that end in the right extention
    return filter(lambda path: path.endswith(ext) or path.endswith(ext.upper()), files)

def trimWhiteSpaceFromImages(src, out):
    # make sure an output directory exist
    if not os.path.isdir(out):
        os.mkdir(out)

    # trim and scale all the images
    for path in getAllInFolder("data", ".png"):
        # load the image
        image = Image.open(f"{src}/{path}")
        image.load()

        # remove alpha channel
        invert_im = image.convert("RGB")

        # invert image (so that white is 0)
        invert_im = ImageOps.invert(invert_im)
        imageBox = invert_im.getbbox()

        # crop the image
        image = image.crop(imageBox)

        # save it
        image.save(f"{out}/{path}")

def loadRandomizedQuestions(src, sheet="Sheet1"):
    # load in the awser from an exel sheet
    doc = xlrd.open_workbook(src)

    # get the sheet with the awsers on it
    sheet = doc.sheet_by_name(sheet)

    # make a list of all the anwers in the sheet
    questions = []
    for rownum in range(sheet.nrows):
        questions.append( sheet.row_values(rownum) )

    # shuffle the list of questions
    random.shuffle(questions)

    # and finally awnser
    return questions

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

trimWhiteSpaceFromImages("data", "tmp")
createAwnserKey("out/key.csv", "data/answers.xlsx")


for i in range(TestIdStart, TestIdStart + NumTest):
    exportTest("out", i + 1)

# zip the output directory
zipf = zipfile.ZipFile('out.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('out/', zipf)
zipf.close()