import time
import random
import pandas as pd
import requests
import datetime


# 設定一些通用函數
def GetStockTabel(TargetDate, TargetStock, TargetDataframe):
    # 設定路徑
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=" + \
        str(TargetDate) + "&stockNo=" + str(TargetStock)
    # read_html是一個dataframe的list，目前這個資料撈回來都在第0個index，所以要用[0]，才會存成一個dataframe
    data = pd.read_html(requests.get(url).text)[0]
    # 因為讀進來的Dataframe有兩個columns，index為0的column我們不需要，透過下功能，只讀取第一列的column
    data.columns = data.columns.get_level_values(1)
    # 新建一個dataframe，內容是由我們的參數dataframe垂直併入讀進來的dataframe，並忽略索引值（讓資料可以按照原索引編號繼續下去）
    NewTargetDataframe = pd.concat([TargetDataframe, data], ignore_index=True)
    return NewTargetDataframe

# 這個日期轉換，主要用來產出網址在用的日期，輸入參數為int，輸出為str


def GetStrTargetdate(Year, Month, day):
    # 因為月份會有1~9月，前面沒有0的問題，而在作為網址參數時卻是必要，因此透過str的zfill功能，讓前面補0
    StrTargetdate = str(Year)+str(Month).zfill(2)+str(day).zfill(2)
    return StrTargetdate

# 這個日期轉換，主要用來產出比對下載資料中的日期，輸入參數為date，輸出為str


def GetSearchDate(date):
    newdate = date.strftime('%Y%m%d')
    searchdate = str(int(str(newdate)[0:4])-1911) + \
        '/'+str(newdate)[4:6]+'/'+str(newdate)[6:8]
    return searchdate

# 這個日期轉換，主要將文字日期轉換為Date，輸入參數為str，輸出為date


def GetDateTargetdate(Strdate):
    # 強制將文字日期，轉換為日期格式
    transdate = datetime.date(int(Strdate[0:4]), int(
        Strdate[4:6]), int(Strdate[6:8]))
    return transdate


def GetBuyDateInfo(date, freq, SDseries, TRdataframe):
    # 要把外部變數拉進來用，要用global
    global CalStartIndex
    global x1
    global x2
    global x3
    global x4
    global x5
    global x6
    newdate = (date + datetime.timedelta(days=freq))
    count = 0
    while count < 1:
        if GetSearchDate(newdate) in list(SDseries):
            index = list(SDseries).index(GetSearchDate(newdate))
            TRdataframe = pd.concat(
                [TRdataframe, SD.iloc[[index]]], ignore_index=True)
            benchmark = CalStartIndex
            for i in range(benchmark, index-1, 1):
                CalStartIndex = CalStartIndex + 1
                print('-----------')
                print(CalStartIndex)
                print(len(SD.index))
                # 持股總現值
                x3 = int(x1*SD.iat[CalStartIndex, 6])
                # 損益金額
                x4 = x3-x2
                # 損益比例
                x5 = x4/x2
                # 存進CA中
                CA.loc[len(CA.index)] = [
                    SD.iat[CalStartIndex, 0], x1, x6, x2, x3, x4, x5, SD.iat[CalStartIndex, 6]]

            # 將交易日資料也寫進CA
            CalStartIndex = CalStartIndex + 1

            # 持股總股數，ox1代表交易前股數
            ox1 = x1
            x1 = x1+int(Payment//(SD.iat[index, 6]+((SD.iat[index, 6])*c1*c2)))
            # 持股總成本
            x2 = x2+int(((x1-ox1)*SD.iat[index, 6]) +
                        ((x1-ox1)*SD.iat[index, 6]*c1*c2))
            # 持股總現值
            x3 = int(x1*SD.iat[index, 6])
            # 損益金額
            x4 = x3-x2
            # 損益比例
            x5 = x4/x2
            # 持股平均成本單價
            x6 = x2/x1
            # 存進CA中
            CA.loc[len(CA.index)] = [
                SD.iat[CalStartIndex, 0], x1, x6, x2, x3, x4, x5, SD.iat[CalStartIndex, 6]]
            count = 1
        else:
            # 若輸入的日期沒找到，則日期再加一日來重跑迴圈
            newdate = newdate + datetime.timedelta(days=1)
            if newdate > datetime.date(YearNow, MonthNow, DayNow):
                count = 1
    return newdate, TRdataframe


    # 設定輸入選項
TargetStock = input("請輸入投資項目股票代號，範例：2330。")
InitialTime = input("請輸入投資開始年月日，範例：20210701。")
Payment = int(input("請輸入定期定額投入金額，範例：10000。"))
Freq = int(input("請輸入幾天定期投入一次，範例：30。"))

# TargetStock = '2330'
# InitialTime = '20210601'的
# Payment = '10000'
# Freq = '30'

# 拆解輸入選項，以作為URL參數
InitialYear = int(InitialTime[0:4])
# 在讀取月份時，可能會有1~9月以01的方式出現，因此利用zfill功能，讓前面為0的自動消失
InitialMonth = int(InitialTime[4:6].zfill(1))
InitialDay = int(InitialTime[6:8].zfill(1))
TimeNow = time.localtime()
YearNow = TimeNow.tm_year
# 在讀取月份時，會有1~9月前面沒有0情況，因此利用zfill功能讓前面補0
MonthNow = TimeNow.tm_mon
DayNow = TimeNow.tm_mday
# 稅費相關參數
c1 = 0.001425
c2 = 0.28

# debug
# print(InitialYear)
# print(InitialMonth)
# print(YearNow)
# print(MonthNow)

# 創造收取資料的dataframe
SD = pd.DataFrame()
# 設定請求的delaytime，以這個網站為例，5秒內存取3次會被鎖IP
DelayTime = [2.5, 2.6, 2.55, 2.65]
# 完成進度比率，a代表以下載的次數，b代表總共需要下載的次數
a = 0
b = 0
for year in range(InitialYear, YearNow + 1, 1):
    if InitialYear != YearNow:
        if year == InitialYear:
            for month_1 in range(InitialMonth, 13, 1):
                b = b+1
        elif year == YearNow:
            for month_2 in range(1, MonthNow+1, 1):
                b = b+1
        else:
            for month_3 in range(1, 12, 1):
                b = b+1
    else:
        for month_4 in range(InitialMonth, MonthNow + 1, 1):
            b = b+1

# print(b)

# 開始查詢迴圈
for year in range(InitialYear, YearNow + 1, 1):
    if InitialYear != YearNow:
        if year == InitialYear:
            for month_1 in range(InitialMonth, 13, 1):
                d1 = GetStrTargetdate(year, month_1, 1)
                SD = GetStockTabel(d1, TargetStock, SD)
                time.sleep(random.choice(DelayTime))
                a = a+1
                print('進度: {:.0%}'.format(a/b))
        elif year == YearNow:
            for month_2 in range(1, MonthNow+1, 1):
                d2 = GetStrTargetdate(year, month_2, 1)
                SD = GetStockTabel(d2, TargetStock, SD)
                time.sleep(random.choice(DelayTime))
                a = a+1
                print('進度: {:.0%}'.format(a/b))
        else:
            for month_3 in range(1, 12, 1):
                d3 = GetStrTargetdate(year, month_3, 1)
                SD = GetStockTabel(d3, TargetStock, SD)
                time.sleep(random.choice(DelayTime))
                a = a+1
                print('進度: {:.0%}'.format(a/b))
    else:
        for month_4 in range(InitialMonth, MonthNow + 1, 1):
            d4 = GetStrTargetdate(year, month_4, 1)
            SD = GetStockTabel(d4, TargetStock, SD)
            time.sleep(random.choice(DelayTime))
            a = a+1
            print('進度: {:.0%}'.format(a/b))

# print(SD)
# print(SD.iat[0, 0])
# print(type(SD.iat[0, 0]))

# 撰寫執行交易，並將交易日相關資訊存到dataframe中。
# TR代表Transaction Record
TR = pd.DataFrame()
# CA代表Calculation，先用一個caldata建立起CA dataframe架構，但因為如果只有column沒有值，我不會把後續檔案併入，因此index 0 的值先個賦予1。
caldata = {'日期': [1], '持股單位': [1], '均價': [1], '總成本': [
    1], '總現值': [1], '損益金額': [1], '損益比例': [1], '當天股價': [1]}
CA = pd.DataFrame(caldata)
# CalStartIndex代表計算資料的第一筆，是在SD的第幾個index
CalStartIndex = 0
# 將交易資料變數宣告在迴圈外，這樣可以一直被更改迭代
x1 = 0
x2 = 0
x3 = 0
x4 = 0
x5 = 0
x6 = 0
x7 = 0

firstdate = GetDateTargetdate(str(InitialTime))
breakpoint1 = 0
while breakpoint1 < 1:
    if GetSearchDate(firstdate) in list(SD['日期']):
        index = list(SD['日期']).index(GetSearchDate(firstdate))
        CalStartIndex = index
        TR = pd.concat([TR, SD.iloc[[index]]], ignore_index=True)
        # 持股單位
        x1 = int(Payment//(SD.iat[index, 6]+((SD.iat[index, 6])*c1*c2)))
        # 持股總成本
        x2 = int((x1*SD.iat[index, 6]) + (x1*SD.iat[index, 6]*c1*c2))
        # 持股總現值
        x3 = int(x1*SD.iat[index, 6])
        # 損益金額
        x4 = x3-x2
        # 損益比例
        x5 = x4/x2
        # 持股平均成本單價
        x6 = x2/x1
        # 當天股價
        x7 = SD.iat[index, 6]

        # 修改儲存計算數據的Dataframe
        CA.iat[0, 0] = GetSearchDate(firstdate)
        CA.iat[0, 1] = x1
        CA.iat[0, 2] = x6
        CA.iat[0, 3] = x2
        CA.iat[0, 4] = x3
        CA.iat[0, 5] = x4
        CA.iat[0, 6] = x5
        CA.iat[0, 7] = x7

        # print(len(CA.index))
        # print(CA)
        # CA.loc[1] = [GetSearchDate(firstdate), x1, x6, x2, x3, x4, x5]
        # print(len(CA.index))

        # print(CA)
        # print(x1)
        # print(x2)
        # print(x3)
        # print(x4)
        # print(x5)
        # print(x6)
        breakpoint1 = 1
    else:
        # 若輸入的日期沒找到，則日期再加一日來重跑迴圈
        firstdate = firstdate + datetime.timedelta(days=1)
        if firstdate > datetime.date(YearNow, MonthNow, DayNow):
            breakpoint = 1

print(CalStartIndex)
print(x1)
print(x2)

# 此時得到儲存第一筆資料的TR
# 接下來完成後續所有交易，並儲存至TR dataframe
while firstdate <= datetime.date(YearNow, MonthNow, DayNow):
    firstdate, TR = GetBuyDateInfo(firstdate, Freq, SD['日期'], TR)

# CA交易紀錄，只會補足到最後一天交易日，這邊把他補足到有資料的最後一天
# 待寫

print(SD)
print(TR)
print(CA)
