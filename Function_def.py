# function
import pandas as pd
def SetTimeString( Year, Month ):
    return str( Year ) + str( Month ).zfill( 2 ) + '01'

def IsBuyMonth( Year, Month, StartYear, StartMonth, Freq ):
    # 月份差異 / 頻率為0則買進
    if ( ( Year - StartYear ) * 12 + ( Month - StartMonth ) ) % Freq == 0:
        return True
    else:
        return False

def AccumulateOneMonth( Year, Month, YearCnt, MonthCnt, EndYear, EndMonth ):
    BreakFlag = 0
    if Year == EndYear:
        if Month == EndMonth:
            BreakFlag = 1
        else:
            MonthCnt += 1
    else:
        if Month == 12:
            MonthCnt -= 11
            YearCnt += 1
        else:
            MonthCnt += 1
    return [ YearCnt, MonthCnt, BreakFlag ]

def GetYearArrayStr():
    YearArr = []
    for i in range( 1950, 2021 ):
        YearArr.append( i )
    return YearArr

def GetMonthArrayStr():
    MonthArr = []
    for i in range( 1, 13 ):
        MonthArr.append( i )
    return MonthArr