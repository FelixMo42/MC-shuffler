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

    questionCounter += 1

    pix = fitz.Pixmap(image)

    if (position + pix.height * Scale > PageHeight - TopPadding):
        position = TopPadding

        pdf.newPage(-1, PageWidth, PageHeight)


    X = SidePadding + 25
    Y = position

    # get last page
    page = pdf[-1]

    # add the problem number 
    page.insertText( fitz.Point(SidePadding + 10, Y + FontSize) , str(questionCounter), fontsize=FontSize )

    # insert the image
    page.insertImage( fitz.Rect(X, Y, X + pix.width * Scale, Y + pix.height * Scale).round() , pixmap=pix)

    #
    page.drawRect( fitz.Rect(SidePadding, Y, PageWidth - SidePadding, Y + pix.height * Scale) )

    # shift down the position by position of the scaled height of the picture
    position += pix.height * Scale

pdf = fitz.open()
pdf.newPage(-1, PageWidth, PageHeight)

addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")
addQuestion("ipsum1.png")

pdf.save("out.pdf")