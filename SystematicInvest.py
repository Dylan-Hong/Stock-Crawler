import time
import random
import math
import pandas as pd
import requests
import Function_def as Func

""" 程式使用說明
輸入
1.起始定期定額年月，為int型態
2.結束定期定額年月，為int型態
3.投資標的，字串型態
4.投資頻率，單位為月
5.投資金額

輸出
1.第一個sheet : 最終損益狀況(結束月份的最後一個交易日比較)
2.第二個sheet : 提供買進的交易紀錄以及買進後損益狀況
3.第三個sheet : 過程中最大虧損金額與比例
 """

# input
# -------------------------------------------------------------------------------
# 設定日期
StartYear = 2019
StartMonth = 1
EndYear = 2020
EndMonth = 12
# 設定標的
TargetStockNo = '0050'
# 投資頻率與金額設定
InvestFreq = 2
InvestAmount = 10000

# 固定參數
FeeRate = 0.001425
TaxRate = 0.003
# -------------------------------------------------------------------------------

# 檔案名稱
FileName = TargetStockNo +'_'+ Func.SetTimeString( StartYear, StartMonth ) + 'To' + Func.SetTimeString( EndYear, EndMonth )

# 初始化參數
YearCnt = MonthCnt = 0
DelayTimeArray = [ 5, 6, 7, 4, 8 ]
HoldAmount = 0
HoldQuantity = 0
HoldCost = 0
BuyFlag = 0
df_log = pd.DataFrame( columns = [ '買進日期', '買進價格', '買進數量(股)', '買進金額', \
     '持股數量', '持股均價', '持股成本', '損益金額', '損益比例' ] )
Index_log = 0
df_ProfitAndLoss = pd.DataFrame( columns = [ '計算日期', '損益金額', '損益比例' ] )
Index_PL = 0
df_MaxLoss = pd.DataFrame( columns = [ '項目', '日期', '總投入資金', '虧損金額', '虧損比例' ] )
Index_MaxLoss = 0
MaxLoss = 0
MaxLossRatio = 0

# 計算流程：讀每個月第一個交易日收盤價 -> 計算可買入股數 -> 設定平均成本 -> 設定資金大小 -> 設定目前損益
while( 1 ):
    # 設定這次回圈要執行的日期
    Year = StartYear + YearCnt
    Month = StartMonth + MonthCnt
    # 累加一個月份
    [ YearCnt, MonthCnt, IsReachEnd ] = Func.AccumulateOneMonth( Year, Month, YearCnt, MonthCnt, EndYear, EndMonth )
    # 檢查是否為買進月份
    BuyFlag = Func.IsBuyMonth( Year, Month, StartYear, StartMonth, InvestFreq )
    # 將日期轉為字串格式
    TargetDate = Func.SetTimeString( Year, Month )
    print(TargetDate)
    
    # 從網頁上讀資料
    # 設定路徑
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=" + TargetDate + "&stockNo=" + TargetStockNo
    # read_html是一個dataframe的list，目前這個資料撈回來都在第0個index，所以要用[0]，才會存成一個dataframe
    data = pd.read_html( requests.get( url ).text )[ 0 ]
    
    # 若該月要買進，才更新持股資訊
    if BuyFlag == 1:
        # ----交易計算----
        # 買進價格
        ClosePrice = data[ data.columns[ 0 ][ 0 ],  '收盤價' ][ 0 ]
        # 計算買進股數
        BuyQuantity = math.floor( InvestAmount / ClosePrice )
        # 計算買進金額
        BuyAmount = math.ceil( ClosePrice * BuyQuantity * ( 1 + FeeRate ) )
        
        # 更新持股成本、數量
        # 持股數量
        HoldQuantity += BuyQuantity
        # 持股成本，包含買進的手續費
        HoldAmount += BuyAmount
        # 持股均價，包含買進的手續費
        HoldCost = HoldAmount / HoldQuantity
        # 未實現損益，包含賣出的手續費+稅
        PLAmount = ClosePrice * HoldQuantity * ( 1 - FeeRate - TaxRate ) - HoldAmount
        # 未實現損益比例，未實現損益 / 投入資金
        PLRatio = PLAmount / HoldAmount
        df_log.loc[ Index_log ] = [ data[ data.columns[ 0 ][ 0 ], '日期' ][ 0 ], '{:.2f}'.format( ClosePrice ), BuyQuantity, BuyAmount,\
            HoldQuantity, '{:.2f}'.format( HoldCost ), HoldAmount, '{:.0f}'.format( PLAmount ), '{:.2%}'.format( PLRatio ) ]

    # ----最大損益計算----
    for i in range( 0, len( data.index ) ):
        # 讀取每日收盤價
        price = data[ data.columns[ 0 ][ 0 ], '收盤價' ][ i ]
        # 計算損益
        PLAmount = price * HoldQuantity * ( 1 - FeeRate - TaxRate ) - HoldAmount
        PLRatio = PLAmount / HoldAmount
        if PLAmount < MaxLoss:
            # 寫入最大損益的dataframe
            df_MaxLoss.loc[ 0 ] = [ '最大金額', data[ data.columns[ 0 ][ 0 ], '日期' ][ i ], HoldAmount, '{:.0f}'.format( MaxLoss ), '{:.2%}'.format( MaxLossRatio ) ]
        if PLRatio < MaxLossRatio:
            df_MaxLoss.loc[ 1 ] = [ '最大比例', data[ data.columns[ 0 ][ 0 ], '日期' ][ i ], HoldAmount, '{:.0f}'.format( MaxLoss ), '{:.2%}'.format( MaxLossRatio ) ]
        # 判斷有沒有超過最大損益，if簡寫方法[ False, True ][ 條件 ]
        MaxLoss = min( MaxLoss, PLAmount )
        MaxLossRatio = min( MaxLossRatio, PLRatio )


    # 檢查是否已經計算到end date
    if IsReachEnd:
        # 計算最終損益
        df_ProfitAndLoss.loc[ 0 ] = [ data[ data.columns[ 0 ][ 0 ], '日期' ][ len( data.index ) - 1 ], '{:.0f}'.format( PLAmount ), '{:.2%}'.format( PLRatio ) ]
        break
    else:
        time.sleep( random.choice( DelayTimeArray ) )
    Index_log += 1
    # # 存入PriceInDay的物件陣列中
    # Price0701 = PriceInDay( data.iat[ 0, 0 ], data.iat[ 0, 6 ] )

# 建立writer，設定檔案路徑
writer = pd.ExcelWriter( './' + FileName + '.xlsx', engine='openpyxl' )
Func.PrintToXlsx_MultiSheet( writer, df_ProfitAndLoss, '最終損益' )
Func.PrintToXlsx_MultiSheet( writer, df_log, '交易紀錄' )
Func.PrintToXlsx_MultiSheet( writer, df_MaxLoss, '最大損益' )
writer.save()


""" 
其他紀錄
1.需要擷取的資料來源：股利、當天即時價格、上櫃、籌碼
2.爬資料的方法：目前需要sleep去避免被鎖，考慮用其他方法
 """