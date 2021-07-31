# -*- coding: utf-8 -*-
from os import path
import tkinter as tk
from tkinter.constants import GROOVE, RIDGE, SUNKEN
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory
import tkinter.messagebox
from tkinter import scrolledtext
import pandas as pd
import threading
import StockCalculate as CAL
# pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 建立主視窗，並命名為window
window = tk.Tk()
window.title('Stock Paradise')
window.geometry('800x600')
window.configure(background='white')

'------------------------------------------------------------------------'
# 參數、輸入選項、以及存取結果、路徑等相關變數先宣告，之後在函數中global存取
Parameters = ['/Users/wuweihsun/Desktop/', 0.03, 0.001425, 0.28]
Input_Word = []
global SD_Show
global TR_Show
global CA_Show
SD_Show = pd.DataFrame()
TR_Show = pd.DataFrame()
CA_Show = pd.DataFrame()
# caldata = {'日期': [1], '持股單位': [1], '均價': [1], '總成本': [1],
#            '總現值': [1], '損益金額': [1], '損益比例': [1], '當天股價': [1]}
# CA = pd.DataFrame(caldata)
# 這個是計算進度條使用
'------------------------------------------------------------------------'


class Fun_Tab(tk.Frame):
    # 建立Class，這個Class主要是分頁視窗的class
    def __init__(self, Tab_Name, MainWindow):
        super().__init__(MainWindow)
        self.Tab_Name = Tab_Name
        MainWindow.add(self, text=Tab_Name)
        pass


class Lable_Display(tk.Label):
    def __init__(self, Text, Frame, inputRow, inputColumn, inputSticky, iPadx=5, iPady=5):
        super().__init__(Frame, text=Text)
        # 定義frame中的grid
        self.grid(row=inputRow, column=inputColumn,
                  sticky=inputSticky, ipadx=iPadx, ipady=iPady)
        pass


class Entry_Display(tk.Entry):
    def __init__(self, Frame, inputRow, inputColumn, inputSticky, Input_Value, Width=8, Cloumnspan=1):
        super().__init__(Frame, textvariable=Input_Value, width=Width)
        self.grid(row=inputRow, column=inputColumn,
                  sticky=inputSticky, columnspan=Cloumnspan)
        pass


def SaveInput():
    global Input_Word
    # 將輸入資料，存成一個Array
    Input_Word = [Input_2_1.get(), Input_2_2.get(),
                  Input_2_3.get(), Input_2_4.get()]
    print(Input_Word)
    pass


def SaveParameter():
    global Parameters
    # 將輸入資料，存成一個Array
    Parameters = [Input_1_1.get(), Input_1_2.get(),
                  Input_1_3.get(), Input_1_4.get()]
    print(Parameters)
    Entry_1_1.delete(0, 'end')
    Entry_1_1.insert(0, Parameters[0])
    Entry_1_2.delete(0, 'end')
    Entry_1_2.insert(0, Parameters[1])
    Entry_1_3.delete(0, 'end')
    Entry_1_3.insert(0, Parameters[2])
    Entry_1_4.delete(0, 'end')
    Entry_1_4.insert(0, Parameters[3])
    pass


def SelectPath():
    # 設定存檔位置
    global Parameters
    Parameters[0] = askdirectory()
    print(Parameters[0])
    Entry_1_1.delete(0, 'end')
    Entry_1_1.insert(0, Parameters[0])
    pass


def SearchAndCalculate():
    # 執行主程式的函數，但我們將會把這函數丟到thread中進行。
    SaveInput()
    # 若不使用global，這些存檔後的dataframe，只會留存在這函式區域內。
    global SD_Show
    global TR_Show
    global CA_Show
    [SD_Show, TR_Show, CA_Show] = CAL.SearchAndCalculate(Input_Word[0], Input_Word[1], Input_Word[3],
                                                         Input_Word[2], Parameters[2], Parameters[3])

    pass


def Show_Result(SD_Show, TR_Show, CA_Show):
    show_title = ["期間最大損失金額為：", "出現日期為：", "期間最大損失比率：", "出現日期為：",
                  "期間最大利益金額為：", "出現日期為：", "期間最大利益比率：", "出現日期為："]
    show_result = [CA_Show['損益金額'].min(),
                   CA_Show.iat[list(CA_Show['損益金額']).index(
                       CA_Show['損益金額'].min()), 0],
                   CA_Show["損益比例"].min(),
                   CA_Show.iat[list(CA_Show["損益比例"]).index(
                       CA_Show["損益比例"].min()), 0],
                   CA_Show["損益金額"].max(),
                   CA_Show.iat[list(CA_Show["損益金額"]).index(
                       CA_Show["損益金額"].max()), 0],
                   CA_Show["損益比例"].max(),
                   CA_Show.iat[list(CA_Show["損益比例"]).index(CA_Show["損益比例"].max()), 0]]
    # 因直接調整Dataframe格式，會將數值直接變成文字，而無法以數字方式比較，因此專門創一個dataframe來改格式之後，回傳到list。
    CA1 = pd.DataFrame(show_result)
    CA1 = CA1.T
    CA1[0] = CA1[0].apply(lambda x: format(x, ','))
    CA1[2] = CA1[2].apply(lambda x: format(x, '.2%'))
    CA1[4] = CA1[4].apply(lambda x: format(x, ','))
    CA1[6] = CA1[6].apply(lambda x: format(x, '.2%'))
    show_result[0] = CA1.iat[0, 0]
    show_result[2] = CA1.iat[0, 2]
    show_result[4] = CA1.iat[0, 4]
    show_result[6] = CA1.iat[0, 6]
    # 因為CA資料不需要以數值方式比較了，直接調整格式。
    CA_Show[u'損益比例'] = CA_Show[u'損益比例'].apply(lambda x: format(x, '.2%'))
    CA_Show[u'持股單位'] = CA_Show[u'持股單位'].apply(lambda x: format(x, ','))
    CA_Show[u'總成本'] = CA_Show[u'總成本'].apply(lambda x: format(x, ','))
    CA_Show[u'總現值'] = CA_Show[u'總現值'].apply(lambda x: format(x, ','))
    CA_Show[u'損益金額'] = CA_Show[u'損益金額'].apply(lambda x: format(x, ','))
    CA_Show[u'均價'] = CA_Show[u'均價'].apply(lambda x: format(x, '.2f'))
    show_lable = []
    for i in range(0, 8):
        show_lable.append(str('Lable_2_'+str((i+5))))
    for i in range(0, 8):
        show_lable[i] = Lable_Display(
            show_title[i]+str(show_result[i]), frame_t2_2, i, 0, 'w', iPadx=0, iPady=0)

    Text_2_1.insert("insert", CA_Show)
    Text_3_1.insert("insert", TR_Show)
    pass


def Thread_SearchAndCalculate():
    # 使用thread來執行主程式，這樣子進度條就可以跑。
    thread1 = threading.Thread(target=SearchAndCalculate, args=())
    thread1.start()
    ProgressBar = ttk.Progressbar(
        frame_t2_1, orient=tk.HORIZONTAL, length=180, mode='indeterminate')
    ProgressBar.grid(row=6, column=1, columnspan=2)
    ProgressBar.start()
    while thread1.is_alive():
        tab_main.update()
        pass
    ProgressBar.destroy()
    Show_Result(SD_Show, TR_Show, CA_Show)
    Click_Request_2_2 = tk.Button(
        frame_t2_2, text="另存新檔", fg="black", command=Save_Excel, bd=0)
    Click_Request_2_2.grid(row=9, column=0, sticky='w', pady=15)
    pass


def Save_Excel():
    CAL.Save_Excel(TR_Show, CA_Show, SD_Show, Parameters[0])
    tkinter.messagebox.showinfo("Pop up", "已儲存在："+Parameters[0])
    pass

# def Show_Result():
#     #運算結果後，顯示在窗口
#     Lable_2_5 = Lable_Display(Input_Word[0],frame_t2_2,0,0,'w')
#     Lable_2_6 = Lable_Display(Input_Word[1],frame_t2_2,1,0,'w')
#     Lable_2_7 = Lable_Display(Input_Word[2],frame_t2_2,2,0,'w')
#     Lable_2_8 = Lable_Display(Input_Word[3],frame_t2_2,3,0,'w')
#     pass


'------------------------------------------------------------------------'
# 建立分頁，需要獨立import tkinter模組中的Notebook功能、Frame功能
# 創建分頁主檔(它包在我們的主視窗window中，width、height用來調整長寬度)
tab_main = ttk.Notebook()
tab_main.place(relx=0.02, rely=0.02, relwidth=0.96,
               relheight=0.96, bordermode='outside')

# 寫一個所有分頁的類別，可以預設定義，並將共用函數寫在裡面
tab_2 = Fun_Tab('定期定額投資', tab_main)
tab_3 = Fun_Tab('交易當日股票資訊', tab_main)
tab_4 = Fun_Tab('損益圖表', tab_main)
tab_1 = Fun_Tab('參數設定', tab_main)


'------------------------------------------------------------------------'
# 建立tab_1中的Frame
frame_t1_1 = tk.Frame(tab_1, width=400, height=250)
# 想讓Frame在左上方，因此我使用anchor定義方位
frame_t1_1.pack(side='left', anchor='nw')
Lable_1_1 = Lable_Display('儲存路徑：', frame_t1_1, 0, 0, 'w')
Input_1_1 = tk.StringVar()
Input_1_1.set(Parameters[0])
Entry_1_1 = Entry_Display(frame_t1_1, 0, 1, 'w', Input_1_1, 30, 3)

Lable_1_2 = Lable_Display('證交率率：', frame_t1_1, 1, 0, 'w')
Input_1_2 = tk.DoubleVar()
Input_1_2.set(Parameters[1])
Entry_1_2 = Entry_Display(frame_t1_1, 1, 1, 'w', Input_1_2)

Lable_1_3 = Lable_Display('券商手續費：', frame_t1_1, 2, 0, 'w')
Input_1_3 = tk.DoubleVar()
Input_1_3.set(Parameters[2])
Entry_1_3 = Entry_Display(frame_t1_1, 2, 1, 'w', Input_1_3)

Lable_1_4 = Lable_Display('券商折扣：', frame_t1_1, 3, 0, 'w')
Input_1_4 = tk.DoubleVar()
Input_1_4.set(Parameters[3])
Entry_1_4 = Entry_Display(frame_t1_1, 3, 1, 'w', Input_1_4)


Click_Request_1_1 = tk.Button(
    frame_t1_1, text="存檔路徑", fg="black", command=SelectPath)
Click_Request_1_1.grid(row=0, column=5, sticky='w')

Click_Request_1_2 = tk.Button(
    frame_t1_1, text="儲存參數", fg="black", command=SaveParameter)
Click_Request_1_2.grid(row=4, column=1, sticky='w')
'------------------------------------------------------------------------'
'------------------------------------------------------------------------'
# 建立tab_2中的Frame
# t2_1為輸入區、t2_2為結果區、t2_3為交易損益區
frame_t2_1 = tk.Frame(tab_2, width=382, height=250, borderwidth=20)
frame_t2_1.grid(row=0, column=0)
# 告訴Frame不要resize，不然放入元件後，將會根據元件大小重新塑形
frame_t2_1.grid_propagate(0)
frame_t2_2 = tk.Frame(tab_2, bg='LightYellow3',
                      width=382, height=250, borderwidth=10)
frame_t2_2.grid(row=0, column=1)
frame_t2_2.grid_propagate(0)
frame_t2_3 = tk.Frame(tab_2, bg='LightYellow3',
                      width=764, height=300, borderwidth=10)
frame_t2_3.grid(row=1, column=0, columnspan=2)
frame_t2_3.grid_propagate(0)

# 建立frame_t2_1的輸入選項
Lable_2_1 = Lable_Display('請輸入起始交易日：', frame_t2_1, 0, 0, 'w')
Lable_2_1_1 = Lable_Display('西元年月日(如: 20210630)', frame_t2_1, 1, 1, 'nw')
Input_2_1 = tk.StringVar()
Input_2_1.set('20210630')
Entry_2_1 = Entry_Display(frame_t2_1, 0, 1, 'w', Input_2_1, 20, 1)

Lable_2_2 = Lable_Display('請輸入股票代號：：', frame_t2_1, 2, 0, 'w')
Input_2_2 = tk.StringVar()
Input_2_2.set('2330')
Entry_2_2 = Entry_Display(frame_t2_1, 2, 1, 'w', Input_2_2, 20, 1)

Lable_2_3 = Lable_Display('請輸入幾天買一次：', frame_t2_1, 3, 0, 'w')
Input_2_3 = tk.IntVar()
Input_2_3.set(30)
Entry_2_3 = Entry_Display(frame_t2_1, 3, 1, 'w', Input_2_3, 20, 1)

Lable_2_4 = Lable_Display('請輸入每次投資金額：', frame_t2_1, 4, 0, 'w')
Input_2_4 = tk.IntVar()
Input_2_4.set(10000)
Entry_2_4 = Entry_Display(frame_t2_1, 4, 1, 'w', Input_2_4, 20, 1)

Click_Request_2_1 = tk.Button(
    frame_t2_1, text="開始查詢", fg="black", command=Thread_SearchAndCalculate, relief=GROOVE)
Click_Request_2_1.grid(row=5, column=1, sticky='w')

# 建立frame_t2_2的顯示選項
# 暫時設定用Label，並用函數生成


# 建立frame_t2_3的顯示選項
# 暫時設定用Text
Text_2_1 = scrolledtext.ScrolledText(frame_t2_3, width=92, height=18)
Text_2_1.grid(row=0, column=0)
'------------------------------------------------------------------------'
'------------------------------------------------------------------------'
# 建立tab_3中的Frame
frame_t3_1 = tk.Frame(tab_3, width=400, height=250, borderwidth=10)
# 想讓Frame在左上方，因此我使用anchor定義方位
frame_t3_1.pack()
Text_3_1 = scrolledtext.ScrolledText(frame_t3_1, width=92, height=34)
Text_3_1.grid(row=0, column=0)
'------------------------------------------------------------------------'
'------------------------------------------------------------------------'
# 要視窗顯示，一定需要這一行
window.mainloop()

print('----------------')
print(Input_Word)
print('----------------')
