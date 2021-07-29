# -*- coding: utf-8 -*-
from os import path
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory
import pandas as pd
import StockCalculate as CAL

# 建立主視窗，並命名為window
window = tk.Tk()
window.title('Stock Paradise')
window.geometry('800x600')
window.configure(background='white')

'------------------------------------------------------------------------'
# 參數、輸入選項、以及存取結果、路徑等相關變數先宣告，之後在函數中global存取
Parameters = ['/Users/wuweihsun/Desktop/', 0.03, 0.001425, 0.28]
Input_Word = []
SD = pd.DataFrame()
TR = pd.DataFrame()
caldata = {'日期': [1], '持股單位': [1], '均價': [1], '總成本': [1],
           '總現值': [1], '損益金額': [1], '損益比例': [1], '當天股價': [1]}
CA = pd.DataFrame(caldata)
'------------------------------------------------------------------------'


class Fun_Tab(tk.Frame):
    # 建立Class，這個Class主要是分頁視窗的class
    def __init__(self, Tab_Name, MainWindow):
        super().__init__(MainWindow)
        self.Tab_Name = Tab_Name
        MainWindow.add(self, text=Tab_Name)
        pass


class Lable_Display(tk.Label):
    def __init__(self, Text, Frame, inputRow, inputColumn, inputSticky):
        super().__init__(Frame, text=Text)
        # 定義frame中的grid
        self.grid(row=inputRow, column=inputColumn,
                  sticky=inputSticky, ipadx=5, ipady=5)
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
    Lable_2_5 = Lable_Display(Input_Word[0], frame_t2_2, 0, 0, 'w')
    Lable_2_6 = Lable_Display(Input_Word[1], frame_t2_2, 1, 0, 'w')
    Lable_2_7 = Lable_Display(Input_Word[2], frame_t2_2, 2, 0, 'w')
    Lable_2_8 = Lable_Display(Input_Word[3], frame_t2_2, 3, 0, 'w')
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
    SaveInput()
    CAL.SearchAndCalculate(Input_Word[0], Input_Word[1], Input_Word[3],
                           Input_Word[2], Parameters[2], Parameters[3], SD, TR, CA, Parameters[0])
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
tab_3 = Fun_Tab('交易紀錄', tab_main)
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
    frame_t2_1, text="開始查詢", fg="black", command=SearchAndCalculate)
Click_Request_2_1.grid(row=5, column=1, sticky='w')

# 建立frame_t2_2的顯示選項
# 暫時設定用Label，並用函數生成


# 建立frame_t2_3的顯示選項
# 暫時設定用Text
Text_2_1 = tk.Text(frame_t2_3, width=92, height=18)
Text_2_1.grid(row=0, column=0)
'------------------------------------------------------------------------'
'------------------------------------------------------------------------'
# 建立tab_3中的Frame
frame_t3_1 = tk.Frame(tab_3, width=400, height=250, borderwidth=10)
# 想讓Frame在左上方，因此我使用anchor定義方位
frame_t3_1.pack()
Text_3_1 = tk.Text(frame_t3_1, width=92, height=34)
Text_3_1.grid(row=0, column=0)
'------------------------------------------------------------------------'
'------------------------------------------------------------------------'
# 要視窗顯示，一定需要這一行
window.mainloop()

print('----------------')
print(Input_Word)
print('----------------')
