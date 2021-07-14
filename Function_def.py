# function
def SetTimeString( Year, Month ):
    return str( Year ) + str( Month ).zfill( 2 ) + '01'
def AccumulateMonth( Year, Month, YearCnt, MonthCnt, EndYear, EndMonth ):
        # print( "Month = ", Month )
    BreakFlag = 0
    if Year == EndYear:
        # print( "State = 1" )
        if Month == EndMonth:
            # print( "State = 2" )
            BreakFlag = 1
        else:
            # print( "State = 3" )
            MonthCnt += 1
    else:
        # print( "State = 4" )
        if Month == 12:
            # print( "State = 5" )
            MonthCnt -= 11
            YearCnt += 1
        else:
            # print( "State = 6" )
            MonthCnt += 1
    return [ YearCnt, MonthCnt, BreakFlag ]