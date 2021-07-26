import time
import random
import math
import pandas as pd
import requests
import GUI_Dylan as GUI
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

# def SystematicInvest( tab ):
def SystematicInvest( tab : GUI.SubTab ):
    # input
    # -------------------------------------------------------------------------------
    # 設定日期
    StartYear = int( tab.entry_StartYear.get() )
    StartMonth = int( tab.entry_StartMonth.get() )
    EndYear = int( tab.entry_EndYear.get() )
    EndMonth = int( tab.entry_EndMonth.get() )
    # 設定標的
    TargetStockNo = tab.entry_StockNum.get()
    # 投資頻率與金額設定
    InvestFreq = int( tab.entry_InvestFreq.get() )
    InvestAmount = int( tab.entry_InvestAmount.get() )
    FeeRate = tab.pMainWindow.Tab_Parameter.FeeRate
    TaxRate = tab.pMainWindow.Tab_Parameter.TaxRate
    # -------------------------------------------------------------------------------

    # 檔案名稱
    tab.FileName = TargetStockNo +'_'+ Func.SetTimeString( StartYear, StartMonth ) + 'To' + Func.SetTimeString( EndYear, EndMonth )

    # 初始化參數
    tab.pMainWindow.Tab_SysInvest.SubTab_Result.ClearList()
    YearCnt = MonthCnt = 0
    DelayTimeArray = [ 5, 6, 7, 4, 8 ]
    HoldAmount = 0
    HoldQuantity = 0
    HoldCost = 0
    BuyFlag = 0
    # df_log = pd.DataFrame( columns = [ '買進日期', '買進價格', '買進數量(股)', '買進金額', \
    #     '持股數量', '持股均價', '持股成本', '損益金額', '損益比例' ] )
    Index_log = 0
    # df_ProfitAndLoss = pd.DataFrame( columns = [ '計算日期', '損益金額', '損益比例' ] )
    Index_PL = 0
    # df_MaxLoss = pd.DataFrame( columns = [ '項目', '日期', '總投入資金', '虧損金額', '虧損比例' ] )
    Index_MaxLoss = 0
    MaxLoss = 0
    MaxLossRatio = 0

    # 建立dataframe
    oFrame = pd.DataFrame( columns = [ '買進日期', '買進價格', '買進股數', '買進金額', '持股數量', '持股成本', '持股金額', '損益金額', '損益比例' ] )
    oFrameIndex = 0

    # 分為三塊 : (1)設定日期並判斷是否為買進月份，或是是否已經結束 (2)若為買進月更新資訊 (3)計算最大損益
    while( 1 ):
        # 設定這次回圈要執行的日期
        Year = StartYear + YearCnt
        Month = StartMonth + MonthCnt
        # 累加一個月份，並且檢查是否已經到達目標日期，若未到達目標日期，則更新年月的counter
        [ YearCnt, MonthCnt, IsReachEnd ] = Func.AccumulateOneMonth( Year, Month, YearCnt, MonthCnt, EndYear, EndMonth )
        # 檢查是否為買進月份
        BuyFlag = Func.IsBuyMonth( Year, Month, StartYear, StartMonth, InvestFreq )
        # 將日期轉為字串格式
        TargetDate = Func.SetTimeString( Year, Month )
        # 輸出當下計算日期至終端機，確認沒當機
        print( TargetDate )
        
        # 從網頁上讀資料
        # 設定路徑
        url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=" + TargetDate + "&stockNo=" + TargetStockNo
        # read_html是一個dataframe的list，目前這個資料撈回來都在第0個index，所以要用[0]，才會存成一個dataframe
        data = pd.read_html( requests.get( url ).text )[ 0 ]
        
        # 持股資訊更新，若該月要買進，才會進行更新
        if BuyFlag == 1:
            # 買進資訊計算
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

            # 輸出資料：[ 買進日期、買進價格、買進股數、買進金額、持股數量、持股均價、持有金額、損益金額、損益比例 ]
            output = [ data[ data.columns[ 0 ][ 0 ], '日期' ][ 0 ], '{:.2f}'.format( ClosePrice ), BuyQuantity, BuyAmount,\
                HoldQuantity, '{:.2f}'.format( HoldCost ), HoldAmount, '{:.0f}'.format( PLAmount ), '{:.2%}'.format( PLRatio ) ]
            tab.df_log.loc[ Index_log ] = output
            # 存到ListBox
            sStr = str( output[ 0 ] ).ljust( 15 )
            sStr = sStr + str( output[ 1 ] ).ljust( 13 )
            sStr = sStr + str( output[ 2 ] ).ljust( 22 )
            sStr = sStr + str( output[ 3 ] ).ljust( 16 )
            sStr = sStr + str( output[ 4 ] ).ljust( 16 )
            sStr = sStr + str( output[ 5 ] ).ljust( 14 )
            sStr = sStr + str( output[ 6 ] ).ljust( 15 )
            sStr = sStr + str( output[ 7 ] ).ljust( 16 )
            sStr = sStr + str( output[ 8 ] ).ljust( 16 )
            tab.pMainWindow.Tab_SysInvest.SubTab_Result.InsertLogToList( sStr )

        # 最大損益計算
        for i in range( 0, len( data.index ) ):
            # 讀取每日收盤價
            price = data[ data.columns[ 0 ][ 0 ], '收盤價' ][ i ]
            # 計算損益
            PLAmount = price * HoldQuantity * ( 1 - FeeRate - TaxRate ) - HoldAmount
            PLRatio = PLAmount / HoldAmount
            tab.PLRecord.append( PLAmount )
            if PLAmount < MaxLoss:
                # 寫入最大損益的dataframe
                tab.df_MaxLoss.loc[ 0 ] = [ '最大金額', data[ data.columns[ 0 ][ 0 ], '日期' ][ i ], HoldAmount, '{:.0f}'.format( MaxLoss ), '{:.2%}'.format( MaxLossRatio ) ]
                tab.MaxLossDate = data[ data.columns[ 0 ][ 0 ], '日期' ][ i ]
                tab.MaxLoss = '{:.0f}'.format( MaxLoss )
            if PLRatio < MaxLossRatio:
                tab.df_MaxLoss.loc[ 1 ] = [ '最大比例', data[ data.columns[ 0 ][ 0 ], '日期' ][ i ], HoldAmount, '{:.0f}'.format( MaxLoss ), '{:.2%}'.format( MaxLossRatio ) ]
                tab.MaxLossRatioDate = data[ data.columns[ 0 ][ 0 ], '日期' ][ i ]
                tab.MaxLossRatio = '{:.2%}'.format( MaxLossRatio )
            MaxLoss = min( MaxLoss, PLAmount )
            MaxLossRatio = min( MaxLossRatio, PLRatio )

        # 檢查是否已經計算到end date
        if IsReachEnd:
            # 計算最終損益
            tab.df_ProfitAndLoss.loc[ 0 ] = [ data[ data.columns[ 0 ][ 0 ], '日期' ][ len( data.index ) - 1 ], '{:.0f}'.format( PLAmount ), '{:.2%}'.format( PLRatio ) ]
            tab.EndDate = data[ data.columns[ 0 ][ 0 ], '日期' ][ len( data.index ) - 1 ]
            tab.PLAmount = '{:.0f}'.format( PLAmount )
            tab.PLRatio = '{:.2%}'.format( PLRatio )
            break
        else:
            time.sleep( random.choice( DelayTimeArray ) )
        Index_log += 1

def PrintResult( tab : GUI.SubTab ):
    pass


def SaveFile( tab : GUI.SubTab ):
    # 建立writer，設定檔案路徑
    writer = pd.ExcelWriter( tab.pMainWindow.Tab_Parameter.Path + '/' + tab.FileName + '.xlsx', engine='openpyxl' )
    # 依序寫入三個dataframe到同一個
    tab.df_ProfitAndLoss.to_excel( writer, sheet_name = '最終損益', index = False )
    tab.df_log.to_excel( writer, sheet_name = '交易紀錄', index = False )
    tab.df_MaxLoss.to_excel( writer, sheet_name = '最大虧損', index = False )

    writer.save()


""" 
其他紀錄
1.需要擷取的資料來源：股利、當天即時價格、上櫃、籌碼
2.爬資料的方法：目前需要sleep去避免被鎖，考慮用其他方法
 """
