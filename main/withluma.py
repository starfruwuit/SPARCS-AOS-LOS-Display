# once more with luma
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text
from luma.core.legacy.font import proportional, SINCLAIR_FONT
import time
import datetime
import asyncio

serial = spi(port = 0, device = 0, gpio=noop())
device = max7219(serial, cascaded = 8, block_orientation = 90, contrast = 0x2f)

hold = 0.1 - 0.005  # refresh rate in seconds
verbose = False  # toggles verbose output. selected by user
firstEntry = ""
secondEntry = ""
halfwayFlag = False  # True IF the first entry has alreay been completed
completeFlag = False # True IF both entries have been completed
zeroes = "00000000"

def timeMath(entry): # takes in a string in the provided format and subtracts the current date, returns a list with 4 entries: days, hours, minutes, seconds
    Syear = int(entry[3:7]) #Syear short for "signal year," the year in which the signal will be acquired/lost
    Smonth = int(entry[8:10])
    Sday = int(entry[11:13])
    Shour = int(entry[14:16])
    Smin = int(entry[17:19])
    Ssec = int(entry[20:22])
    if verbose:
        print(f"in the entry, year is {Syear}, month is {Smonth}, day is {Sday}, hour is {Shour}, minute is {Smin}, second is {Ssec}")
    Sdate = datetime.datetime(year = Syear, month = Smonth, day = Sday, hour = Shour, minute = Smin, second = Ssec)
    currentTime = datetime.datetime.utcnow()
    if verbose:
        print(f"the current time is {currentTime} and the time of signal is {Sdate}")
    Dtime = Sdate - currentTime # D is short for delta
    if verbose:
        print(f"the time between now and signal is {Dtime}")
    # if time has "days" >9, input is invalid and cannot be displayed
    if Dtime.days >9:
        raise ValueError("the number of days between now and signal is greater than nine, and unable to be displayed.")
    Ddays = Dtime.days
    Dsec = Dtime.seconds % 60
    Dminutes = int(Dtime.seconds / 60)
    Dhours = int(Dminutes / 60)
    Dminutes = Dminutes % 60
    if verbose:
        print(f"there are {Ddays} days, {Dhours} hours, {Dminutes} minutes, and {Dsec} seconds until signal")
    delta = [Ddays, Dhours, Dminutes, Dsec]
    return delta
    
def validate(rawString): #takes in a "raw" string and makes sure it's in the specified format
    global firstEntry
    global secondEntry
    validationFlag = False
    if len(rawString) ==46:
        lenFlag = True
    else:
        lenFlag = False
    firstEntry = rawString[0:21]
    secondEntry = rawString[24:45]
    if (rawString[0:3] == "AOS" or rawString[0:3] == "LOS") and (rawString[24:27] =="AOS" or rawString[24:27] == "LOS"):
        markersFlag = True
    else:
        markersFlag = False
    timeMath(firstEntry) #testimg the timeMath function
    # more validation here
    numericalFlag = True #true by default for now!! EDIT LATER
    
    if lenFlag and markersFlag and numericalFlag:
        validationFlag = True
    return validationFlag
    
def countdown(deltaTime): #takes a list in the style of [days, hours, minutes, seconds] and counts down to zero
    global halfwayFlag
    global completeFlag
    global zeroes
    global hold
    days = deltaTime[0]
    hours = deltaTime[1]
    minutes = deltaTime[2]
    secondsAnd = deltaTime[3] * 10 #seconds and deciseconds as one number
    countdownDoneFlag = False
    while not countdownDoneFlag:
        # iterate:
        if secondsAnd > 0:
            secondsAnd -= 1
            time.sleep(hold)
            count = str(days) + zeroes[0:(2-len(str(hours)))] + str(hours) + zeroes[0:(2-len(str(minutes)))] + str(minutes) + zeroes[0:(3-len(str(secondsAnd)))] + str(secondsAnd)
        elif minutes > 0:
            minutes -= 1
            secondsAnd += 599
            time.sleep(hold)
            count = str(days) + zeroes[0:(2-len(str(hours)))] + str(hours) + zeroes[0:(2-len(str(minutes)))] + str(minutes) + zeroes[0:(3-len(str(secondsAnd)))] + str(secondsAnd)
        elif hours > 0:
            hours -= 1
            minutes += 59
            secondsAnd += 599
            time.sleep(hold)
            count = str(days) + zeroes[0:(2-len(str(hours)))] + str(hours) + zeroes[0:(2-len(str(minutes)))] + str(minutes) + zeroes[0:(3-len(str(secondsAnd)))] + str(secondsAnd)
        elif days > 0:
            days -= 1
            hours += 23
            minutes += 59
            secondsAnd += 599 
            time.sleep(hold)
            count = str(days) + zeroes[0:(2-len(str(hours)))] + str(hours) + zeroes[0:(2-len(str(minutes)))] + str(minutes) + zeroes[0:(3-len(str(secondsAnd)))] + str(secondsAnd)
        else:
            countdownDoneFlag = True
            count = "00000000"
        # display active countdown
        with canvas(device) as draw:
            text(draw, (1,0), count, fill="white", font = SINCLAIR_FONT)
    if halfwayFlag:
        completeFlag = True
    else:
        halfwayFlag = True

def GrabData():
    global firstEntry
    global secondEntry
    global halfwayFlag
    # CODE TO RETREIVE DATA GOES HERE
    dataValid = False
    while not dataValid and not halfwayFlag:
        raw = input("please enter your AOS/LOS timestamps in UTC time, in exactly the format 'AOSyyyy/mm/dd/hh:mm:ss; LOSyyyy/mm/dd/hh:mm:ss'--> ")
        # do format validation here
        formatValid = validate(raw)
        if formatValid and verbose:
            print(f"you have entered {raw}.")
            confirm = input("is this correct? [y/n] ")
            if confirm == "y":
                dataValid = True
        else:
            dataValid = True
    # data has now been entered. now to parse
    if not halfwayFlag:
        delta = timeMath(firstEntry)
    else:
        delta = timeMath(secondEntry)
    return delta

def main():
    global verbose
    global halfwayFlag
    global completeFlag
    verboseAsk = input("would you like verbose output in your terminal? [y/n] ")
    if verboseAsk == "y":
        verbose = True # enables verbose output
    while not completeFlag:
        if not halfwayFlag:
            delta1 = GrabData()
            countdown(delta1)
        elif not completeFlag:
            delta2 = GrabData()
            countdown(delta2)
    with canvas(device) as draw:
        text(draw, (1,0), "__DONE__", fill="white", font = SINCLAIR_FONT)

main()