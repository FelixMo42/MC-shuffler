## SETTINGS ##

TopPadding = 100
SidePadding = 30

PageWidth = 612
PageHeight = 1008

FontSize = 10

Scale = 0.7

## END SETTINGS ##

import xlrd
import fitz
import glob
import csv
import shutil
import os
from random import shuffle
from PIL import Image, ImageOps, ImageFilter

def exportTest(out="."):
    if not os.path.exists(out):
        os.makedirs(out)

    def addQuestion(src):
        nonlocal questionCounter
        nonlocal position

        # increase the current count of question by 1
        questionCounter += 1

        # load the image
        pix = fitz.Pixmap(src)

        width = pix.width
        height = pix.height

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
        page.insertImage(fitz.Rect(X0 + 50, Y0 + 10, X0 + 50 + width, Y1 - 10), pixmap=pix)

        # draw the rectang around the question
        page.drawRect( fitz.Rect(X0, Y0, X1, Y1) )

        # shift down the position to the end of this question
        position = Y1

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
    pdf.save(f"{out}/test.pdf")

    # export the a csv with the new awser key
    with open(f'{out}/key.csv', 'w', newline='') as csvfile:
        awnsers = csv.writer(csvfile)
        i = 1
        for question in questions:
            awnsers.writerow([i, question[1]])
            i += 1

def getAllInFolder(src, ext):
    files = os.listdir(src)

    return filter(lambda path: path.endswith(ext) or path.endswith(ext.upper()), files)

def trimWhiteSpaceFromImages(src, out):
    # remove the output folder if it exist
    if os.path.isdir(out):
        os.rmdir(out)
    
    # then create a new fresh empty one
    os.mkdir(out)

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

        # resize it
        image = image.resize( (int(image.width * Scale), int(image.height * Scale)), Image.ANTIALIAS )

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
    shuffle(questions)

    # and finally awnser
    return questions

# trimWhiteSpaceFromImages("data", "tmp")
for i in range(0, 15):
    exportTest(f"out/{i}")