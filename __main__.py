## SETTINGS ##

TopPadding = 100
SidePadding = 30

PageWidth = 612
PageHeight = 1008

FontSize = 10

## END SETTINGS ##

import xlrd
import fitz
import glob
from random import shuffle
from PIL import Image, ImageOps

# how many question we jave
questionCounter = 0

# were on the last page a new question should be added
position = TopPadding

def trimWhiteSpaceFromImages():
    # get all the pngs
    filePaths = glob.glob("data/*.PNG")

    for filePath in filePaths:
        # load the image
        image = Image.open(filePath)
        image.load()

        # remove alpha channel
        invert_im = image.convert("RGB")

        # invert image (so that white is 0)
        invert_im = ImageOps.invert(invert_im)
        imageBox = invert_im.getbbox()

        # crop and save the image
        cropped = image.crop(imageBox)
        cropped.save(filePath)

def addQuestion(src):
    global questionCounter
    global position

    # increase the current count of question by 1
    questionCounter += 1

    # load the image
    pix = fitz.Pixmap(src)

    # is their enough space left on this page for the question?
    if (position + pix.height > PageHeight - TopPadding):
        # reset the position to the top of the page
        position = TopPadding

        # we need a new page
        pdf.newPage(-1, PageWidth, PageHeight)

    # coordinates of question 
    X0 = SidePadding
    Y0 = position
    X1 = PageWidth - SidePadding
    Y1 = position + pix.height

    # get last page
    page = pdf[-1]

    # add the problem number 
    page.insertText(fitz.Point(X0 + 10, Y0 + FontSize + 10), str(questionCounter), fontsize=FontSize)

    # insert the picture of the multiple choice question
    page.insertImage(fitz.Rect(X0 + 25, Y0, X0 + 25 + pix.width, Y1), pixmap=pix)

    # draw the rectang around the question
    page.drawRect( fitz.Rect(X0, Y0, X1, Y1) )

    # shift down the position to the end of this question
    position = Y1

def loadRandomizedAnswers(src, sheet="Sheet1"):
    # load in the awser from an exel sheet
    doc = xlrd.open_workbook(src)

    # get the sheet with the awsers on it
    sheet = doc.sheet_by_name(sheet)

    # make a list of all the anwers in the sheet
    answers = []
    for rownum in range(sheet.nrows):
        answers.append( sheet.row_values(rownum) )

    # shuffle the list of answers
    shuffle(answers)

    # and finally awnser
    return answers

trimWhiteSpaceFromImages()

answers = loadRandomizedAnswers("data/answers.xlsx")

# create a new page
pdf = fitz.open()

# add a page to the begining
pdf.newPage(-1, PageWidth, PageHeight)

# add a bunch of questions
for answer in answers:
    addQuestion(f"data/{str(int(answer[0]) % 4 + 1)}.PNG")

# save the pdf
pdf.save("out.pdf")