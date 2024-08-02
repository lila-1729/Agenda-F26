# README
# Pagesize      = 11.6cm x 18.2cm ~ 328 x 515 (actual 328.3 x 515.3) 
#               = 328.82 x 515.88 
# Line Height   = 4mm   = 11.34pt ~ 11
# Outer Margin  = 4mm   = 11.34pt ~ 11
# Inner Margin  = 1.0cm = 28.35pt ~ 28
# Timeduration  = 1.2cm = 34.02pt ~ 34
# Timeinterval  = 1.1cm = 31.18pt ~ 31
# Overview Grid Length (3x)       = 86 
# Overview Grid Space (2x)        = 7  


# Import Packages
import calendar 
import datetime
import reportlab.rl_config
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPM

# Constants
CALENDAR_START = datetime.date(2024,12,30) 
CALENDAR_RANGE = 52
OVERVIEW_YEARS = [2025,2026]

DOC_HEIGHT = 515
DOC_WIDTH = 328

GRID_WIDTH = 160-28
GRID_HEIGHT = 11.34

CUT_WIDTH = 0.3
CUT_OPACITY = 0.7
CUT_DASHLINE = 20
CUT_DASHSPACE = 20

PATH_FREITAGLOGO = "/home/..."

# Output File
Output = canvas.Canvas("Calendar.pdf",
                       pagesize=(DOC_WIDTH+CUT_WIDTH,DOC_HEIGHT+CUT_WIDTH)) 

# Fonts
FontList = Output.getAvailableFonts()
pdfmetrics.registerFont(TTFont('Courier', 'CourierPrime-Regular.ttf'))
pdfmetrics.registerFont(TTFont('CourierIt', 'CourierPrime-Italic.ttf'))
pdfmetrics.registerFont(TTFont('CourierBd', 'CourierPrime-Bold.ttf'))

# Cutting Grid
def Cut():
    Output.setLineWidth(CUT_WIDTH)
    Output.setStrokeGray(CUT_OPACITY)
    Output.setDash(CUT_DASHLINE,CUT_DASHSPACE)

    Output.line(0,DOC_HEIGHT-CUT_WIDTH,DOC_WIDTH,DOC_HEIGHT-CUT_WIDTH)
    Output.line(CUT_WIDTH,0,CUT_WIDTH,DOC_HEIGHT)
    Output.line(DOC_WIDTH-CUT_WIDTH,0,DOC_WIDTH-CUT_WIDTH,DOC_HEIGHT)
    Output.line(0,1,DOC_WIDTH,1)


# Calendar List
OffsetDay = datetime.timedelta(days=1)
OffsetWeek = datetime.timedelta(weeks=1)
CalendarList = []
for i in range(CALENDAR_RANGE):
    WeekList = []
    for i in range(7):
        WeekList.append(CALENDAR_START)
        CALENDAR_START += OffsetDay 
    CalendarList.append(WeekList)

# Overview List - 2 years
OverviewCalendar = calendar.Calendar(firstweekday=0)  
OverviewList = []
for year in OVERVIEW_YEARS:
    YearList = []
    for month in range(12):
        MonthList = []
        OverviewTable = OverviewCalendar.monthdatescalendar(year, month+1)
        for week in OverviewTable:
            WeekList = []
            for day in week:
                if int(day.strftime("%-m")) == month+1:
                    WeekList.append(day)
            MonthList.append(WeekList)
        YearList.append(MonthList)
    OverviewList.append(YearList)




# Calendar
def Calendar():
    RightDesign(CalendarList[0][4]-OffsetWeek,CalendarList[0][5]-OffsetWeek,CalendarList[0][6]-OffsetWeek)
    for WeekCount in range(CALENDAR_RANGE):
        LeftDesign(CalendarList[WeekCount][0],CalendarList[WeekCount][1],CalendarList[WeekCount][2],CalendarList[WeekCount][3])
        RightDesign(CalendarList[WeekCount][4],CalendarList[WeekCount][5],CalendarList[WeekCount][6])
    LeftDesign(CalendarList[-1][0]+OffsetWeek,CalendarList[-1][1]+OffsetWeek,CalendarList[-1][2]+OffsetWeek,CalendarList[-1][3]+OffsetWeek)
    Output.showPage()

def LeftDesign(DAY_0, DAY_1, DAY_2, DAY_3):
    Output.setLineWidth(.6)
    Output.setStrokeGray(0.5)

    LineY = []
    lineNumber = 42 # must be even
    chopped = int(lineNumber /2)
    for count in range(lineNumber):
        #502 originally
        LineY.append(480-count*GRID_HEIGHT)  
    LineX1= [14,52,160] 
    LineX2= [168,192,300]
    LineY1, LineY2 = LineY[:chopped], LineY[chopped:]

    Output.grid(LineX1,LineY2)
    Output.grid(LineX1,LineY1)
    Output.grid(LineX2,LineY1)
    Output.grid(LineX2,LineY2)

    Padding = 0.3
    Output.setFillGray(0.90)
    Output.rect(LineX1[0]+Padding,LineY1[1]+Padding,GRID_WIDTH-2*Padding,GRID_HEIGHT-2*Padding, stroke=0, fill=1)
    Output.rect(LineX2[0]+Padding,LineY1[1]+Padding,GRID_WIDTH-2*Padding,GRID_HEIGHT-2*Padding, stroke=0, fill=1)
    Output.rect(LineX1[0]+Padding,LineY2[1]+Padding,GRID_WIDTH-2*Padding,GRID_HEIGHT-2*Padding, stroke=0, fill=1)
    Output.rect(LineX2[0]+Padding,LineY2[1]+Padding,GRID_WIDTH-2*Padding,GRID_HEIGHT-2*Padding, stroke=0, fill=1)
    Output.setFillGray(0)

    Output.setFont('CourierBd', 9)
    Output.drawString(LineX1[0]+3,LineY1[1]+3,DAY_0.strftime("%-d"))
    Output.drawString(LineX2[0]+3,LineY1[1]+3,DAY_1.strftime("%-d"))
    Output.drawString(LineX1[0]+3,LineY2[1]+3,DAY_2.strftime("%-d"))
    Output.drawString(LineX2[0]+3,LineY2[1]+3,DAY_3.strftime("%-d"))

    Output.setFont('Courier', 9)
    Output.drawString(LineX1[1]+3,LineY1[1]+3,DAY_0.strftime("%A"))
    Output.drawString(LineX2[1]+3,LineY1[1]+3,DAY_1.strftime("%A"))
    Output.drawString(LineX1[1]+3,LineY2[1]+3,DAY_2.strftime("%A"))
    Output.drawString(LineX2[1]+3,LineY2[1]+3,DAY_3.strftime("%A"))

    Output.setFont('Courier', 11)
    if DAY_0.strftime("%B") == DAY_3.strftime("%B"):
        Output.drawString(28,490,DAY_0.strftime("%B"))
    else:
        Output.drawString(28,490,DAY_0.strftime("%B")+" - "+DAY_3.strftime("%B"))

    Output.setFont('Courier', 9)
    Output.drawRightString(300,490,DAY_0.strftime("Week %-W"))

    Cut()

    Output.showPage()

def RightDesign(DAY_4, DAY_5, DAY_6):
    Output.setLineWidth(.6)
    Output.setStrokeGray(0.5)


    LineY = []
    lineNumber = 42 # must be even
    chopped = int(lineNumber /2)
    for count in range(lineNumber):
        #502 originally
        LineY.append(480-count*GRID_HEIGHT)  
    LineX1= [28,52,160] 
    LineX2= [168,192,314]
    LineNotes = [168,314]
    LineY1, LineY2 = LineY[:chopped], LineY[chopped:]

    Output.grid(LineX1,LineY2)
    Output.grid(LineX1,LineY1)
    Output.grid(LineX2,LineY1) 
    Output.grid(LineNotes,LineY2)

    Padding = 0.3
    Output.setFillGray(0.90)
    Output.rect(LineX1[0]+Padding,LineY1[1]+Padding,GRID_WIDTH-2*Padding,GRID_HEIGHT-2*Padding, stroke=0, fill=1)
    Output.rect(LineX2[0]+Padding,LineY2[1]+Padding,GRID_WIDTH-2*Padding,GRID_HEIGHT-2*Padding, stroke=0, fill=1)
    Output.rect(LineX2[0]+Padding,LineY1[1]+Padding,GRID_WIDTH-2*Padding,GRID_HEIGHT-2*Padding, stroke=0, fill=1)
    Output.rect(LineX1[0]+Padding,LineY2[1]+Padding,GRID_WIDTH-2*Padding,GRID_HEIGHT-2*Padding, stroke=0, fill=1)
    Output.setFillGray(0)

    Output.setFont('CourierBd', 9)
    Output.drawString(LineX1[0]+3,LineY1[1]+3,DAY_4.strftime("%-d"))
    Output.drawString(LineX2[0]+3,LineY1[1]+3,DAY_5.strftime("%-d"))
    Output.drawString(LineX1[0]+3,LineY2[1]+3,DAY_6.strftime("%-d"))

    Output.setFont('Courier', 9)
    Output.drawString(LineX1[1]+3,LineY1[1]+3,DAY_4.strftime("%A"))
    Output.drawString(LineX2[1]+3,LineY1[1]+3,DAY_5.strftime("%A"))
    Output.drawString(LineX1[1]+3,LineY2[1]+3,DAY_6.strftime("%A"))
    Output.drawString(LineX2[0]+3,LineY2[1]+3,"Notes")
    #Output.drawString(LineX2[1]+3,LineY2[1]+3,DAY_4.strftime("%A"))

    Output.setFont('Courier', 11)
    if DAY_4.strftime("%B") == DAY_6.strftime("%B"):
        Output.drawRightString(300,490,DAY_4.strftime("%B"))
    else:
        Output.drawRightString(300,490,DAY_4.strftime("%B")+" - "+DAY_6.strftime("%B"))

    Output.line(0,0,400,0)
    Output.setFont('Courier', 9)
    Output.drawString(28,490,DAY_4.strftime("Week %-W"))

    Cut() 

    Output.showPage()


def Cover():
    #Output.rect(0,38,240,10, stroke=0, fill=1)
    #Output.setFillGray(0.8)
    Output.rect(0,13,30,490, stroke=0, fill=1)
    Output.setFillGray(0)
    Output.setFont('CourierBd', 28)
    Output.drawString(50,350+40,"AGENDA")
    Output.setFont('Courier', 20)
    Output.drawString(50,325+40,"2024")
    Output.setFont('CourierBd', 10)
    Output.setFillGray(1)
    #Output.drawString(50,40,"Design by")
    Output.setFillGray(0)
    #Output.drawString(243,40,"design")
    Output.drawInlineImage(PATH_FREITAGLOGO,
                           50 ,450,1024/15,341/15)
    Output.showPage()
    Output.showPage()



def Overview():
    Output.setLineWidth(.6)
    Output.setStrokeGray(0.5)
    Output.setFont('Courier', 9)
    Padding = 3
       
    # For 3 columns
    #LineX1 = [28,114] 
    #LineX2 = [121,207]
    #LineX3 = [214,300]
    #LineX = [LineX1,LineX2,LineX3]

    # For 2 columns
    LineX1= [28,160] 
    LineX2= [168,314]
    LineX = [LineX1,LineX2]

    LineY = []

    LineY_height = 450 # Or 502
    for year in OverviewList:
        for month in year:
            LineCount = 0
            LineYi = []
            for week in month:
                LineYj = []
                LineYj.append(LineY_height-LineCount*GRID_HEIGHT)
                LineCount += 1
                for day in week:
                    LineYj.append(LineY_height-LineCount*GRID_HEIGHT)  
                    LineCount += 1
                LineYi.append(LineYj)
            LineY.append(LineYi)
    
    
    # Ugly method of extending
    OverviewList_merged = OverviewList[0]
    OverviewList_merged.extend(OverviewList[1])

    GridCount = 0
    PageCount = 0

    MonthCount = 0
    for month in LineY:
        Output.setFillGray(0.90)
        Output.rect(LineX[GridCount][0],month[0][0]+GRID_HEIGHT,GRID_WIDTH,GRID_HEIGHT,
                    stroke=1, fill=1)
        Output.setFillGray(0)
        Output.setFont('CourierBd', 9)
        Output.drawString(LineX[GridCount][0]+3,month[0][0]+GRID_HEIGHT+3,OverviewList_merged[MonthCount][0][0].strftime("%m"))
        Output.setFont('Courier', 9)
        Output.drawString(LineX[GridCount][0]+19.5,month[0][0]+GRID_HEIGHT+3,OverviewList_merged[MonthCount][0][0].strftime("%B"))
        Output.setFont('Courier', 9)
        WeekCount = 0
        for week in month:
            Output.grid(LineX[GridCount],week)
            Output.drawRightString(LineX[GridCount][1],week[0]+Padding,OverviewList_merged[MonthCount][WeekCount][0].strftime("%-W"))
            for i in range(len(week)-1):
                Output.drawString(LineX[GridCount][0]+Padding,week[i+1]+Padding,OverviewList_merged[MonthCount][WeekCount][i].strftime("%d %a"))
            WeekCount += 1
        GridCount += 1
        GridCount %= 2
        if GridCount == 0:
            if PageCount == 0:
                Output.setFont('Courier', 11)
                Output.drawRightString(LineX[1][1],490,OverviewList_merged[MonthCount][0][0].strftime("%Y"))
                LineX[1][1] -= 14
                LineX[0][0] -= 14
            else:
                Output.setFont('Courier', 11)
                Output.drawString(LineX[0][0],490,OverviewList_merged[MonthCount][0][0].strftime("%Y"))
                LineX[1][1] += 14
                LineX[0][0] += 14

            Output.showPage()
            Output.setLineWidth(.6)
            Output.setStrokeGray(0.5)
            Output.setFont('Courier', 9)
            PageCount += 1
            PageCount %= 2

        MonthCount += 1


# Print to Output File
Cover()
Calendar()
Overview()

# Closing Files
Output.save()
