# GitTest
import time
import random
import math
import pandas as pd
import requests
import Function_def as Func

# 建立一個class儲存當天的資訊
class PriceInDay:
    # 建構子包含日期、收盤價
    def __init__( self, date, ClosePrice ):
        self.date = date
        self.ClosePrice = ClosePrice
    def func():
        ClosePrice = 0

# input
# -------------------------------------------------------------------------------
# 設定日期
StartYear = 2020
StartMonth = 5
EndYear = 2020
EndMonth = 6
# 設定標的
TargetStockNo = '0050'
# 投資頻率與金額設定
InvestFreq = 1
InvestAmount = 10000

# 固定參數
FeeRate = 0.001425
TaxRate = 0.003
# -------------------------------------------------------------------------------

# 檔案名稱
FileName = TargetStockNo +'_'+ Func.SetTimeString( StartYear, StartMonth ) + 'To' + Func.SetTimeString( EndYear, EndMonth )

stop = 1
YearCnt = MonthCnt = 0
DelayTimeArray = [ 5, 6, 7, 4, 8 ]

# 初始化參數
HoldAmount = 0
HoldQuantity = 0
HoldCost = 0

# 計算流程：讀每個月第一個交易日收盤價 -> 計算可買入股數 -> 設定平均成本 -> 設定資金大小 -> 設定目前損益
while( 1 ):

    # 設定這次回圈要執行的日期
    Year = StartYear + YearCnt
    Month = StartMonth + MonthCnt
    # 累加一個月份
    [ YearCnt, MonthCnt, IsReachEnd ] = Func.AccumulateMonth( Year, Month, YearCnt, MonthCnt, EndYear, EndMonth )
    # 將日期轉為字串格式
    TargetDate = Func.SetTimeString( Year, Month )
    
    # 從網頁上讀資料
    # 設定路徑
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=" + TargetDate + "&stockNo=" + TargetStockNo
    # read_html是一個dataframe的list，目前這個資料撈回來都在第0個index，所以要用[0]，才會存成一個dataframe
    data = pd.read_html( requests.get( url ).text )[ 0 ]
    
    # 讀取收盤價、計算買進數量
    # 買進價格
    ClosePrice = data[ data.columns[ 0 ][ 0 ],  '收盤價' ][ 0 ]
    # 計算買進股數
    BuyQuantity = math.floor( InvestAmount / ClosePrice )
    # 計算買進金額
    BuyAmount = math.ceil( ClosePrice * BuyQuantity * ( 1 + FeeRate ) )
    
    # 更新持股成本、數量
    # 持股數量
    HoldQuantity += BuyQuantity
    # 持股金額
    HoldAmount += BuyAmount
    # 持股均價
    HoldCost = HoldAmount / HoldQuantity



    # # 輸出資料：[ 買進日期、買進價格、買進股數、買進金額、持有成本、持有股數、損益金額、損益比例 ]
    # print( '買進日期 : ', data[ data.columns[ 0 ][ 0 ],  '日期' ][ 0 ] )
    # print( '買進價格 : ', ClosePrice )
    # print( '買進股數 : ', BuyQuantity )
    # print( '買進金額 : ', BuyAmount )
    # print( '持股數量 : ', HoldQuantity )
    # print( '持股均價 : ', HoldCost )
    # print( '持有金額 : ', HoldAmount )
    print( '損益金額 : ', ClosePrice * HoldQuantity * ( 1 + FeeRate + TaxRate ) - HoldAmount )
    # print( '損益比例 : ', '{:.2%}'.format( ClosePrice / HoldCost - 1 ) )
    # print()

    time.sleep( random.choice( DelayTimeArray ) )

    # 檢查是否已經計算到end date
    if IsReachEnd:
        break


# 存入PriceInDay的物件陣列中
# Price0701 = PriceInDay( data.iat[ 0, 0 ], data.iat[ 0, 6 ] )

# writer = pd.ExcelWriter( './practice/xlsfile/' + FileName + '.xlsx', engine='openpyxl' )

# data.to_excel( writer, sheet_name = '2330' )
# writer.save()

""" 
其他紀錄
1.需要擷取的資料來源：股利、當天即時價格、上櫃、籌碼
2.爬資料的方法：目前需要sleep去避免被鎖，考慮用其他方法

 """