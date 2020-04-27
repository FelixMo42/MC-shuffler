## SETTINGS ##

TopPadding = 100
SidePadding = 50

PageWidth = 612
PageHeight = 1008

FontSize = 10
Scale = 0.40

## END SETTINGS ##

import fitz

questionCounter = 0
position = TopPadding

def addQuestion(image):
    global questionCounter
    global position

    # increase the current count of question by 1
    questionCounter += 1

    # load the image
    pix = fitz.Pixmap(image)

    # is their enoght space left on this page for the question?
    if (position + pix.height * Scale > PageHeight - TopPadding):
        # reset the position to the top of the page
        position = TopPadding

        # we need a new page
        pdf.newPage(-1, PageWidth, PageHeight)

    # coordinates of question 
    X0 = SidePadding
    Y0 = position
    X1 = PageWidth - SidePadding
    Y1 = Y0 + pix.height * Scale

    # get last page
    page = pdf[-1]

    # add the problem number 
    page.insertText( fitz.Point(X0 + 10, Y0 + FontSize) , str(questionCounter), fontsize=FontSize )

    # insert the picture of the multiple choice question
    page.insertImage( fitz.Rect(X0 + 50, Y0, X0 + 50 + pix.width * Scale, Y1).round() , pixmap=pix)

    # draw the rectang around the question
    page.drawRect( fitz.Rect(X0, Y0, X1, Y1) )

    # shift down the position by position of the scaled height of the picture
    position += pix.height * Scale

# create a new page
pdf = fitz.open()

# add a page to the begining
pdf.newPage(-1, PageWidth, PageHeight)

# add a bunch of questions
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")

# save the pdf
pdf.save("out.pdf")