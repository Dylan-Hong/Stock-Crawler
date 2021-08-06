import time
import datetime
import requests
import pandas as pd
from io import StringIO
from dateutil.relativedelta import relativedelta

class parser:
    def __init__( self ):
        # 行業類別號 (ex. 1： 水泥工業)
        self.__type_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

        # 爬網頁的時間間隔
        self.__parse_intvl = 5

    # 找個股的行業類別號
    def __stock_No_to_type( self, stock_No ):
        for i in self.__type_list:
            if i < 10:
                select_type = "0" + str( i )
            else:
                select_type = str( i )

            url_chip = "https://www.twse.com.tw/fund/T86?response=csv&date=%s&selectType=%s"%(str( 20210723 ), select_type)

            table_part = pd.read_csv( StringIO( requests.get( url_chip ).text ), header= 1 )

            time.sleep( self.__parse_intvl )

            if table_part.loc[table_part["證券代號"] == str(stock_No)].empty == False:
                break

        return i

    # 爬營收
    def parse_revenue( self, month_start, month_end= None ):
        if month_end is None:
            month_end = month_start

        # 將月份轉成日期(營收是以月來計 但爬蟲網址須輸入日期)
        date = datetime.date.fromisoformat( month_start + "-01" )
        date_end = datetime.date.fromisoformat( month_end + "-01" )

        data_list = []

        while( date <= date_end ):
            # 設定網址
            url = "https://mops.twse.com.tw/nas/t21/sii/t21sc03_%s_%s_0.html"%(str( date.year - 1911 ), str( date.month ))

            # 爬網址資料
            r = requests.get( url )
            
            # 設定資料格式為中文
            r.encoding = 'big5'

            # 讀取資料內容
            table_raw = pd.read_html( StringIO( r.text ), encoding='big-5', header= 1 )

            # 暫停一段時間(避免被網站端視為惡意攻擊)
            time.sleep( self.__parse_intvl )

            # 只保留欄位大於5的列(過濾前述和後述)
            table = pd.concat( [sub for sub in table_raw if sub.shape[1] > 5] )
            
            # 刪除含有合計項的列 並保留特定欄位
            data = table.loc[ table["公司代號"] != "合計" ][["公司代號", "公司名稱", "當月營收"]]

            # 處理後資料加入List
            data_list.append( data )

            # 移至下個月份
            date += relativedelta( months = 1 )

        return data_list

    # 爬個股營收
    def parse_revenue_indiv( self, stock_No, month_start, month_end= None ):
        # 將月份轉成日期(營收是以月來計 但爬蟲網址須輸入日期)
        date = datetime.date.fromisoformat( month_start + "-01" )
        date_end = datetime.date.fromisoformat( month_end + "-01" )

        # 生成輸出的物件
        data_whole = pd.DataFrame()

        while( date <= date_end ):
            # 取出年月(iso格式為 YYYY-MM-DD)
            month = date.isoformat()[0:7]

            # 爬當月營收
            table = self.parse_revenue( month )[0]

            # 從當月營收取出個股營收
            data_part = table.loc[table["公司代號"] == str( stock_No )]

            # 設定列名稱
            data_part = data_part.set_axis( [month], axis= 'index' )

            # 將個股當月營收加入輸出
            data_whole = pd.concat( [data_whole, data_part] )

            # 移至下個月份
            date += relativedelta( months = 1 )

        return data_whole
 
    # 爬技術面
    def parse_tech( self, stock_No, month_start, month_end= None ):
        if month_end is None:
            month_end = month_start

        # 將月份轉成日期(營收是以月來計 但爬蟲網址須輸入日期)
        date = datetime.date.fromisoformat( month_start + "-01" )
        date_end = datetime.date.fromisoformat( month_end + "-01" )

        # 生成輸出的物件
        tech_whole = pd.DataFrame()

        while( date <= date_end ):
            # 分別取出年月日
            date_iso = date.isoformat( date ) 
            year = date_iso[0:4]
            month = date_iso[5:7]
            day = date_iso[8:10]

            # 設定網址
            url_fund = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=%s%s%s&stockNo=%s"%(year, month, day, stock_No)

            # 爬網站資料
            tech_month = pd.read_html( url_fund, header= 1 )[0]

            # 暫停一段時間(避免被網站端視為惡意攻擊)
            time.sleep( self.__parse_intvl )

            # 將資料加入輸出
            tech_whole = pd.concat( [tech_whole, tech_month] )

            # 移至下個月份
            date += relativedelta( months = 1 )

        return tech_whole

    # 爬籌碼面
    def parse_chip( self, date_start, date_end = None, select_type= None ):
        if date_end is None:
            date_end = date_start
        
        if select_type is None:
            type_list = self.__type_list
        else:
            type_list = [select_type]

        # 生成輸出列表
        chip_list = []

        # 計算日期總數
        start = datetime.date.fromisoformat( date_start )
        end = datetime.date.fromisoformat( date_end )
        date_range = (end - start).days

        for delta in range( date_range + 1 ):
            # 生成當日籌碼
            chip = pd.DataFrame()

            for i_type in type_list:
                if i_type < 10:
                    select_type = "0" + str( i_type )
                else:
                    select_type = str( i_type )

                # 計算日期
                date = (datetime.date.fromisoformat( date_start ) + datetime.timedelta( delta )).isoformat()

                # 轉換日期格式(YYYY-MM-DD to YYYYMMDD)
                date = date[0:4] + date[5:7] + date[8:10]

                # 設定網址
                url_chip = "https://www.twse.com.tw/fund/T86?response=csv&date=%s&selectType=%s"%(date, select_type)

                # 爬網址資料
                text = requests.get( url_chip ).text

                # 暫停一段時間(避免被網站端視為惡意攻擊)
                time.sleep( self.__parse_intvl )

                # 略過空的網址(假日沒有資料)
                if text == "\r\n":
                    continue

                # 讀取資料內容
                table_part = pd.read_csv( StringIO( requests.get( url_chip ).text ), header= 1 )

                # 將資料加入當日籌碼
                chip = pd.concat( [chip, table_part] )

            # 將當日籌碼加入輸出
            chip_list.append( chip )

        return chip_list

    # 爬個股籌碼面
    def parse_chip_indiv( self, stock_No, date_start, date_end = None, cols= None ):
        # cols: 0:  證券代號
        #       1:  證券名稱
        #       2:  外陸資買進股數(不含外資自營商)
        #       3:  外陸資賣出股數(不含外資自營商)
        #       4:  外陸資買賣超股數(不含外資自營商)
        #       5:  外資自營商買進股數
        #       6:  外資自營商賣出股數
        #       7:  外資自營商買賣超股數
        #       8:  投信買進股數
        #       9:  投信賣出股數
        #       10: 投信買賣超股數
        #       11: 自營商買賣超股數
        #       12: 自營商買進股數(自行買賣)
        #       13: 自營商賣出股數(自行買賣)
        #       14: 自營商買賣超股數(自行買賣)
        #       15: 自營商買進股數(避險)
        #       16: 自營商賣出股數(避險)
        #       17: 自營商買賣超股數(避險)
        #       18: 三大法人買賣超股數

        if date_end is None:
            date_end = date_start

        # 查找個股對應的行業別
        select_type = self.__stock_No_to_type( stock_No )
        
        # 計算日期總數
        start = datetime.date.fromisoformat( date_start )
        end = datetime.date.fromisoformat( date_end )
        date_range = (end - start).days

        # 生成輸出空間
        chip_whole = pd.DataFrame()

        for i in range( date_range + 1 ):
            # 計算日期
            date = (datetime.date.fromisoformat( date_start ) + datetime.timedelta( i )).isoformat()

            # 爬當日籌碼
            chip_table = self.parse_chip( date, None, select_type )[0]

            # 避免空資料(假日沒有資料)
            if chip_table.empty:
                continue

            # 從當日籌碼中取出個股
            chip_day = chip_table.loc[chip_table["證券代號"] == str(stock_No)]

            # 取出需要的欄位並加入輸出空間
            if cols is None:
                chip_whole = pd.concat([chip_whole, chip_day])
            else:
                chip_whole = pd.concat([chip_whole, chip_day.iloc[:, cols]])

        return chip_whole
