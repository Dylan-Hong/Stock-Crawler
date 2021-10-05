# import GUI
import pandas as pd
import yfinance as yf 
import numpy as np
import matplotlib.pyplot as plt
import talib
import math
import re
import requests
import twstock

"""
Todo
.漲停、跌停無法買進
.買進後隔天上漲但未站上五日線，會出場
.log的日期格子寬度
.抓平均震盪比例，才能判斷長紅Ｋ
.分批買進、分批賣出
.出場規則改為紅Ｋ底部

Done
1.掃過所有股票
2.站上or跌破只有一天，不列入高低點

"""

class cEnumRow():
    def __init__(self) -> None:
        self.Open = i = 0
        self.High = i = i + 1
        self.Low = i = i + 1
        self.Close = i = i + 1
        self.Adj_Close = i = i + 1
        self.Volumn = i = i + 1
        self.MA_5 = i = i + 1
        self.MA_20 = i = i + 1
        self.MA_60 = i = i + 1
        self.MA_120 = i = i + 1
        self.IsOver5MA = i = i + 1
        self.Trend = i  = i + 1
        self.debugTime = i = i + 1
eRow = cEnumRow()

# load data
# def Calculation( tab : GUI.cMT_Swing ):
def Calculation():
    writer = pd.ExcelWriter( '0905.xlsx', engine='openpyxl' )
    # 讀取所有上市股票的代號與名稱
    [ StockNumList, StockNameList ] = GetStcokList()
    df_profit = pd.DataFrame( columns = [ '股票代號', '股票名稱', '總損益' ] )

    # 搜尋所有股票
    for StockIndex in range( 0, 1 ):
        # 設定標的
        TargetStockNo = StockNumList[ StockIndex ]
        TargetStockName = StockNameList[ StockIndex ]
        # ----------------------------------input : 讀取GUI上輸入的參數---------------------------------------
        # 設定日期
        # StartYear = int( tab.Combobox_StartYear.get() )
        # StartMonth = int( tab.Combobox_StartMonth.get() )
        # EndYear = int( tab.Combobox_EndYear.get() )
        # EndMonth = int( tab.Combobox_EndMonth.get() )
        # # 設定標的
        # TargetStockNo = tab.entry_StockNum.get()

        # FeeRate = tab.pMainWindow.Tab_Parameter.FeeRate
        # TaxRate = tab.pMainWindow.Tab_Parameter.TaxRate
        # --------------------------------------------------------------------------------------------------
        StartYear = 2019
        StartMonth = 4
        StartDay = 1
        EndYear = 2021
        EndMonth = 9
        EndDay = 15
        FeeRate = 0.0001425
        TaxRate = 0.0003

        # yfinance上面撈資料

        # 這邊可以撈一些基本面的資料，目前暫時不用
        # Tickerdata = yf.Ticker( '2330.TW' )
        # print( Tickerdata.financials )
        # print( Tickerdata.info )

        # download會回傳dataframe的資料
        df_data = yf.download( '%s.TW'%TargetStockNo, \
            start = '%s-%s-%s'%( StartYear, StartMonth, StartDay ), \
            end = '%s-%s-%s'%( EndYear, EndMonth, EndDay ) )

        # 用dataframe畫出均線的方法
        # df_data['MA_7'] = df_data['Close'].rolling(7).mean()
        # print( df_data.tail() )

        # 用talib畫出均線
        sma_5 = talib.SMA(np.array(df_data['Close']), 5)
        sma_20 = talib.SMA(np.array(df_data['Close']), 20)
        sma_60 = talib.SMA(np.array(df_data['Close']), 60)
        sma_120 = talib.SMA(np.array(df_data['Close']), 120)
        # 新增均線資料到dataframe中
        df_data[ 'MA_5' ] = sma_5
        df_data[ 'MA_20' ] = sma_20
        df_data[ 'MA_60' ] = sma_60
        df_data[ 'MA_120' ] = sma_120
        # 新增放入dataframe的資訊
        df_data.insert( len(df_data.columns), column = 'IsOver5MA', value = np.nan )
        df_data.insert( len(df_data.columns), column = 'Trend', value = np.nan )
        df_data.insert( len(df_data.columns), column = 'debugTime', value = np.nan )

        # 初始化模組
        InvestInfo = cInventoryInfo( 100000, TaxRate, FeeRate )
        TrendInfo = cTrendInfo()

        # 逐日計算
        for i in range( 0, len( df_data.index ) ):
            # 讀取當天價格資訊
            PriceInfo = cPriceInfo( df_data, i )
            # 更新當天趨勢
            TrendInfo.UpdateTrend( PriceInfo )
            # 輸出資料至dataframe
            PrintToDf( df_data, TrendInfo, i, PriceInfo )
            # 執行買進賣出
            BuySell( PriceInfo, TrendInfo, InvestInfo )

        # 單隻股票結束後輸出結果
        print( PriceInfo.date )
        df_profit.loc[ len( df_profit ) ] = [ TargetStockNo, TargetStockName, '{:.2%}'.format( \
            ( InvestInfo.Cash + InvestInfo.CostAmount ) / InvestInfo.OriginCash - 1 ) ]
        # todo : 這邊可以放判斷當天進出
        # print( TargetStockNo + ' : ' + GetRealtimeData( TargetStockNo, 'Buy' ) )

        # print( df_data.head(10) )
        df_data.to_excel( writer, sheet_name = TargetStockNo + '損益', index = True )
        InvestInfo.df_InventLog.to_excel( writer, sheet_name = TargetStockNo + 'Log', index = False )

    df_profit.to_excel( writer, sheet_name = '所有損益', index = False )
    # print( df_profit[ '總損益' ].mean() ) # 這個必需不能存成字串
    writer.save()

class cPriceInfo():
    def __init__( self, df : pd.DataFrame, index ) -> None:
        self.MA20_value = df[ 'MA_20' ][ index ]
        self.MA5_value = df[ 'MA_5' ][ index ]
        self.Close = df[ 'Close' ][ index ]
        self.Open = df[ 'Open' ][ index ]
        self.High = df[ 'High' ][ index ]
        self.Low = df[ 'Low' ][ index ]
        self.date = df.index[ index ]

class cTrendInfo():
    def __init__( self ) -> None:
        self.LastHigh = np.nan
        self.LastLow = np.nan
        self.High = np.nan
        self.Low = np.nan
        self.NewHigh = np.nan
        self.NewLow = np.nan

        self.IsOver5MA = 'Nan'
        self.LastIsOver5MA = 'Nan'
        self.QueIsOver5MA = []
        self.Keep5MADay = np.nan
        self.IsOver20MA = np.nan

        self.IsFirstUpdate = 0
        self.IsHighInc = 0
        self.IsLowInc = 0
        self.Trend = 'Unknown'

    def UpdateTrend( self, PriceInfo : cPriceInfo ):
        # self.LastIsOver5MA = self.IsOver5MA
        # 若已經有三天是否站上五日的資訊了，則pop掉最舊的
        if len( self.QueIsOver5MA ) == 3:
            self.QueIsOver5MA.pop( 0 )
        # 判斷是否在五日線上
        # self.IsOver5MA = self.ChkIsOverMA( PriceInfo.MA5_value, PriceInfo.Close )
        self.QueIsOver5MA.append( self.ChkIsOverMA( PriceInfo.MA5_value, PriceInfo.Close ) )
        # 判斷是否在月線上
        self.IsOver20MA = self.ChkIsOverMA( PriceInfo.MA20_value, PriceInfo.Close )
        # 更新高低點
        self.UpdateHighAndLow( PriceInfo )
        # 更新頭頭高、底底高
        self.UpdateHighLowInc( PriceInfo )
        # 判斷趨勢多、空、盤整
        if self.IsHighInc and self.IsLowInc:
            self.Trend = 'Bull'
        elif not self.IsHighInc and not self.IsLowInc:
            self.Trend = 'Bear'
        else:
            self.Trend = 'Con'
        print( PriceInfo.date, "  ", self.Trend )
        print( "LL = ", self.LastLow, "CL = ", self.Low, "NL = ", self.NewLow )
        print( "LH = ", self.LastHigh, "CH = ", self.High, "NH = ", self.NewHigh )

    # 更新高低點
    def UpdateHighAndLow( self, PriceInfo : cPriceInfo ):
        # 情境
        # 1.尚未切換過五日線，直接不判斷
        # 2.尚無確認的高點與低點
        # 3.尚無確認的前高與前低
        # 4.前高前低，確認高確認低都有
        # 特殊情況需處理
        # 1.站上五日線當天又創低點 ： 會更新到
        # 2.站上五日線當天又創低點，且跌破前低造成底底低 ： 會更新到
        # 3.站上隔天馬上跌破 ： 考慮新增一個維持天數
        # 4.只跌破一點點 ： 考慮在判斷IsOver5MA的時候擋掉

        # 尚未切換兩次五日線
        if len( self.QueIsOver5MA ) < 3:
            self.Keep5MADay = 0

        # 若只有跌破一天，不更新其中低點為確定低點
        elif self.QueIsOver5MA[ 0 ] == 'Y' and self.QueIsOver5MA[ 1 ] == 'Y' and self.QueIsOver5MA[ 2 ] == 'Y' \
          or self.QueIsOver5MA[ 0 ] == 'Y' and self.QueIsOver5MA[ 1 ] == 'N' and self.QueIsOver5MA[ 2 ] == 'Y':
            self.Keep5MADay += 1
            # 若高點有突破則更新NewHigh
            self.UpdateNewHigh( PriceInfo )

        # 第一天跌破五日線，高低點都更新
        elif self.QueIsOver5MA[ 0 ] == 'Y' and self.QueIsOver5MA[ 1 ] == 'Y' and self.QueIsOver5MA[ 2 ] == 'N':
            self.Keep5MADay += 1
            # 若高點有突破則更新NewHigh
            self.UpdateNewHigh( PriceInfo )
            # 跌破第一天更新NewLow，但不當作確認低點
            self.UpdateNewLow( PriceInfo )

        # 兩天沒站上五日線，確認跌破，更新確認高點
        elif self.QueIsOver5MA[ 0 ] == 'Y' and self.QueIsOver5MA[ 1 ] == 'N' and self.QueIsOver5MA[ 2 ] == 'N':
            self.Keep5MADay = 1
            self.UpdateNewHigh( PriceInfo )
            self.UpdateNewLow( PriceInfo )
            self.LastHigh = self.High
            self.High = self.NewHigh
            self.NewHigh = np.nan

        # 維持五日線下or中間有跌破一天
        elif self.QueIsOver5MA[ 0 ] == 'N' and self.QueIsOver5MA[ 1 ] == 'N' and self.QueIsOver5MA[ 2 ] == 'N' \
          or self.QueIsOver5MA[ 0 ] == 'N' and self.QueIsOver5MA[ 1 ] == 'Y' and self.QueIsOver5MA[ 2 ] == 'N':
            self.Keep5MADay += 1
            # 若低點跌破則更新NewLow
            self.UpdateNewLow( PriceInfo )

        # 第一天站上，更新但不作為確認低點
        elif self.QueIsOver5MA[ 0 ] == 'N' and self.QueIsOver5MA[ 1 ] == 'N' and self.QueIsOver5MA[ 2 ] == 'Y':
            self.Keep5MADay += 1
            # 若高點有突破則更新NewHigh
            self.UpdateNewHigh( PriceInfo )
            # 跌破第一天更新NewLow，但不當作確認低點
            self.UpdateNewLow( PriceInfo )

        # 確認站上五日線，更新確認低點
        elif self.QueIsOver5MA[ 0 ] == 'N' and self.QueIsOver5MA[ 1 ] == 'Y' and self.QueIsOver5MA[ 2 ] == 'Y':
            self.Keep5MADay = 1
            self.UpdateNewHigh( PriceInfo )
            self.UpdateNewLow( PriceInfo )
            self.LastLow = self.Low
            self.Low = self.NewLow
            self.NewLow = np.nan
        """
        # 尚未切換過五日線
        if self.LastIsOver5MA == 'Nan':
            self.Keep5MADay = 0

        # 維持五日線上
        elif self.LastIsOver5MA == 'Y' and self.IsOver5MA == 'Y':
            self.Keep5MADay += 1
            # 若高點有突破則更新NewHigh
            self.UpdateNewHigh( PriceInfo )

        # 維持五日線下
        elif self.LastIsOver5MA == 'N' and self.IsOver5MA == 'N':
            self.Keep5MADay += 1
            # 若低點跌破則更新NewLow
            self.UpdateNewLow( PriceInfo )

        # 站上五日線
        elif self.LastIsOver5MA == 'N' and self.IsOver5MA == 'Y':
            self.Keep5MADay = 1
            self.UpdateNewHigh( PriceInfo )
            self.UpdateNewLow( PriceInfo )
            self.LastLow = self.Low
            self.Low = self.NewLow
            self.NewLow = np.nan

        # 跌破五日線
        elif self.LastIsOver5MA == 'Y' and self.IsOver5MA == 'N':
            self.Keep5MADay = 1
            self.UpdateNewHigh( PriceInfo )
            self.UpdateNewLow( PriceInfo )
            self.LastHigh = self.High
            self.High = self.NewHigh
            self.NewHigh = np.nan
        """

    def UpdateNewHigh( self, PriceInfo : cPriceInfo ):
        if PriceInfo.High > self.NewHigh or math.isnan( self.NewHigh ):
            self.NewHigh = PriceInfo.High

    def UpdateNewLow( self, PriceInfo : cPriceInfo ):
        if PriceInfo.Low < self.NewLow or math.isnan( self.NewLow ):
            self.NewLow = PriceInfo.Low

    def UpdateHighLowInc( self, PriceInfo : cPriceInfo ):
        # 頭頭高
        # 確認高點大於前高
        if self.High >= self.LastHigh:
            self.IsHighInc = 1
        # 確認高點低於前高，但新高點已過確認高點；排除未有新高點
        elif not math.isnan( self.NewHigh ) and self.NewHigh > self.High:
            self.IsHighInc = 1
        # 確認高點低於前高、新高點也沒有高過確認高點
        else:
            self.IsHighInc = 0

        # 底底高
        # 確認低點低於前低
        if self.Low < self.LastLow:
            self.IsLowInc = 0
        # 若有新低點，判斷新低點是否跌破
        elif not math.isnan( self.NewLow ) and self.NewLow < self.Low:
            self.IsLowInc = 0
        # 確認低點高於前低，新低點也沒破確認一點
        else:
            self.IsLowInc = 1

    def ChkIsOverMA( self, MA_Value, Close ):
        if math.isnan( MA_Value ):
            return np.nan
        elif Close > MA_Value:
            return 'Y'
        else:
            return 'N'

class cInventoryInfo():
    def __init__( self, Cash, TaxRate, FeeRate ) -> None:
        # 設定現金總額
        self.Cash = Cash
        self.OriginCash = Cash
        # 淨損益金額
        self.NetIncome = 0
        # 股票名稱 -> todo:好像沒要幹嘛
        self.StockNum = ''
        # 損益平衡價
        self.UnitCost = 0
        # 買進價格
        self.BuyPrice = 0
        # 持股數量
        self.Quantity = 0
        # 持股成本總額
        self.CostAmount = 0
        # 是否持股狀態變數
        self.HoldFlag = 0

        # 輸出紀錄
        self.df_InventLog = pd.DataFrame( columns = [ '買進日期', '買進價格', '賣出日期', '賣出價格', '單筆淨利', '單筆比例' , '累積損益', '累積比例' ] )
        # 買進日期
        self.BuyDate = 0

        # 交易資訊
        self.TaxRate = TaxRate
        self.FeeRate = FeeRate
    
    def ClearInfo( self ):
        self.UnitCost = 0
        self.BuyPrice = 0
        self.Quantity = 0
        self.CostAmount = 0
        self.HoldFlag = 0

    def BuyStock( self, PriceInfo : cPriceInfo ):
        # 買進價格為收盤價
        self.BuyPrice = PriceInfo.Close
        # 歐印買進，收盤價 * 數量 ＊ ( 1 + 0.001425 ) = 金額，計算可買價格、買進金額
        self.Quantity = math.floor( self.Cash / PriceInfo.Close / ( 1 + self.FeeRate ) )
        self.CostAmount = math.ceil( self.BuyPrice * self.Quantity * ( 1 + self.FeeRate ) )
        # 計算剩餘現金
        self.Cash -= self.CostAmount
        # 計算損益平衡價 : 平衡價 * 數量 * ( 1 - 手續費 - 稅金 ) = 買進金額
        self.UnitCost = self.CostAmount / self.Quantity / ( 1 - self.FeeRate - self.TaxRate )
        # 持股狀態on
        self.HoldFlag = 1
        self.BuyDate = PriceInfo.date

    def SellStock( self, PriceInfo : cPriceInfo ):
        # print( 'Buy  : ', PriceInfo.date, '{:.2f}'.format( PriceInfo.Close ), 'Quantity = ', self.Quantity, 'Cash = ', self.Cash )
        FeeAmount = PriceInfo.Close * self.Quantity * self.FeeRate
        TaxAmount = PriceInfo.Close * self.Quantity * self.TaxRate
        SellAmount = math.ceil( PriceInfo.Close * self.Quantity - FeeAmount - TaxAmount )
        self.NetIncome += SellAmount - self.CostAmount
        self.Cash += SellAmount
        self.df_InventLog.loc[ len(self.df_InventLog) ] = [ self.BuyDate, self.BuyPrice, PriceInfo.date, PriceInfo.Close, \
            SellAmount - self.CostAmount, '{:.2%}'.format( ( SellAmount - self.CostAmount ) / self.CostAmount ), \
            self.NetIncome, '{:.2%}'.format( self.NetIncome / self.OriginCash ) ]
        # print( 'Sell : ', PriceInfo.date, '{:.2f}'.format( PriceInfo.Close ), 'Quantity = ', self.Quantity, 'Cash = ', self.Cash )
        # print( '單筆淨利 = ', SellAmount - self.CostAmount, '   ;百分比 = ', '{:.2f}'.format( ( SellAmount - self.CostAmount ) / self.CostAmount * 100 ) )
        # print( '累積損益 = ', self.NetIncome )
        self.ClearInfo()

def PrintToDf( df : pd.DataFrame, TrendInfo : cTrendInfo, index, PriceInfo : cPriceInfo ):
    # Todo : 這邊寫數值到df需要一個enum比較好
    df.iloc[ index, eRow.IsOver5MA ] = TrendInfo.IsOver5MA
    df.iloc[ index, eRow.Trend ] = TrendInfo.Trend
    df.iloc[ index, eRow.debugTime ] = PriceInfo.date

def BuySell( PriceInfo : cPriceInfo, TrendInfo : cTrendInfo, InvestInfo : cInventoryInfo ):
    # 多頭趨勢判斷是否為買點
    # 若無持股，判斷是否買進
    if InvestInfo.HoldFlag == 0:
        # print( PriceInfo.date, ':', ( PriceInfo.Close - PriceInfo.Open ) / PriceInfo.Close * 100 )
        # 收盤價站上五日線買進
        if TrendInfo.Trend == 'Bull' and PriceInfo.Close > PriceInfo.Open:
            InvestInfo.BuyStock( PriceInfo )
    # 若有持股，判斷是否賣出
    elif InvestInfo.HoldFlag == 1:
        # 收盤價跌破五日線賣出
        if PriceInfo.Close < PriceInfo.MA5_value:
            InvestInfo.SellStock( PriceInfo )

def GetStcokList():
    res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
    df = pd.read_html(res.text)[0]
    df.columns = ['有價證券代號及名稱', '國際證券辨識號碼(ISIN Code)', '上市日', '市場別', '產業別', 'CFICode', '備註']

    stackCodeDict = {}
    StockNumList = []
    StockNameList = []
    for code in df['有價證券代號及名稱']:
        pattern = "[0-9]"
        stackCode = code.split('　')
        if stackCode[0] and re.search(pattern, stackCode[0]) and len(stackCode[0]) == 4:
            StockNumList.append( str( stackCode[0] ) )
            StockNameList.append( str( stackCode[1] ))
            stackCodeDict[stackCode[0]] = stackCode[1]
    return [ StockNumList, StockNameList ]

def GetRealtimeData( StockNum, BuyOrSell ):
    stock = twstock.realtime.get( StockNum )
    # print( stock[ 'success' ] )
    # print( stock[ 'realtime' ][ 'best_ask_price' ][ 0 ] )
    high = stock[ 'realtime' ][ 'high' ]
    print( 'high = ', high )
    if BuyOrSell == 'Buy':
        return stock[ 'realtime' ][ 'best_ask_price' ][ 0 ]
    if BuyOrSell == 'Sell':
        return stock[ 'realtime' ][ 'best_bid_price' ][ 0 ]


Calculation()