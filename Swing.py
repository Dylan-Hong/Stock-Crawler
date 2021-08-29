# import GUI
from pandas.core.frame import DataFrame
from requests.sessions import PreparedRequest
import yfinance as yf 
import numpy as np
import matplotlib.pyplot as plt
import talib
import math


# load data
# def Calculation( tab : GUI.cMT_Swing ):
def Calculation():

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
    # ---------------------------------------------------------------------------------------------------
    StartYear = 2020
    StartMonth = 1
    StartDay = 1
    EndYear = 2020
    EndMonth = 3
    EndDay = 10
    # 設定標的
    TargetStockNo = '2330'

    FeeRate = 0.0001425
    TaxRate = 0.0003

    # yfinance上面撈資料

    # 這邊可以撈一些基本面的資料，目前暫時不用
    # Tickerdata = yf.Ticker( '2330.TW' )
    # print( Tickerdata.financials )
    # print( Tickerdata.info )

    # download會回傳dataframe的資料
    df_2330 = yf.download( '%s.TW'%TargetStockNo, \
        start = '%s-%s-%s'%( StartYear, StartMonth, StartDay ), \
        end = '%s-%s-%s'%( EndYear, EndMonth, EndDay ) )
    # print( df_2330 )

    # 用dataframe畫出均線的方法
    # df_2330['MA_7'] = df_2330['Close'].rolling(7).mean()
    # print( df_2330.tail() )

    # 用talib畫出均線
    sma_5 = talib.SMA(np.array(df_2330['Close']), 5)
    sma_20 = talib.SMA(np.array(df_2330['Close']), 20)
    sma_60 = talib.SMA(np.array(df_2330['Close']), 60)
    sma_120 = talib.SMA(np.array(df_2330['Close']), 120)
    df_2330[ 'MA_5' ] = sma_5
    df_2330[ 'MA_20' ] = sma_20
    df_2330[ 'MA_60' ] = sma_60
    df_2330[ 'MA_120' ] = sma_120

    InvestInfo = cInventoryInfo( 100000, TaxRate, FeeRate )

    for i in range( 5, len( df_2330.index ) + 1 ):
        # print( i, '=', df_2330[ 'Close' ][ i - 1 ], ', ma5 = ', df_2330[ 'MA_5' ][ i - 1 ] )
        # 讀取當天價格資訊
        PriceInfo = cPriceInfo( df_2330, i - 1 )
        # 若無持股，判斷是否買進
        if InvestInfo.HoldFlag == 0:
            # 收盤價站上五日線買進
            if PriceInfo.Close > PriceInfo.MA5_value:
                InvestInfo.BuyStock( PriceInfo )
        # 若有持股，判斷是否賣出
        elif InvestInfo.HoldFlag == 1:
            # 收盤價跌破五日線賣出
            if PriceInfo.Close < PriceInfo.MA5_value:
                InvestInfo.SellStock( PriceInfo )
                print( '損益 = ', InvestInfo.NetIncome )
        
        
    # plt.plot( sma_10 )
    # plt.plot( sma_30 )
    # plt.show()

class cPriceInfo():
    def __init__( self, df : DataFrame, index ) -> None:
        self.MA5_value = df[ 'MA_5' ][ index - 1 ]
        self.Close = df[ 'Close' ][ index - 1 ]
        self.date = df.index[ index - 1 ]

class cInventoryInfo():
    def __init__( self, Cash, TaxRate, FeeRate ) -> None:
        # 設定現金總額
        self.Cash = Cash
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
        print( 'Buy  : ', PriceInfo.date, PriceInfo.Close, 'Quantity = ', self.Quantity, 'Cash = ', self.Cash )
        # 持股狀態on
        self.HoldFlag = 1


    def SellStock( self, PriceInfo : cPriceInfo ):
        FeeAmount = PriceInfo.Close * self.Quantity * self.FeeRate
        TaxAmount = PriceInfo.Close * self.Quantity * self.TaxRate
        SellAmount = math.ceil( PriceInfo.Close * self.Quantity - FeeAmount - TaxAmount )
        self.NetIncome += SellAmount - self.CostAmount
        self.Cash += SellAmount
        print( 'Sell : ', PriceInfo.date, PriceInfo.Close, 'Quantity = ', self.Quantity, 'Cash = ', self.Cash )
        self.ClearInfo()
