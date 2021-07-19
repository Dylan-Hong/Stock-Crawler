import tkinter as tk
from tkinter import ttk
import math

""" 
這邊練習用place
 """
# window = tk.Tk()
# window.geometry('800x600')
# window.configure(background='white')
 # http://andrewpythonarduino.blogspot.com/2018/04/python_6.html
# ComboBox

# Radiobutton 
# Checkbutton
# Listbox 


""" 
這邊練習用grid，並且有用函數執行button
 """
# def calculate():
#     btnstr.set( 'hello' )
# window = tk.Tk()
# window.geometry('800x600')
# window.configure(background='white')

# def calculate_bmi_number():
#     height = float(height_entry.get()) / 100
#     weight = float(weight_entry.get())
#     print( height )
#     print( weight )
#     bmi_value = round(weight / math.pow(height, 2), 2)
#     result = '你的 BMI 指數為：{} {}'.format(bmi_value, get_bmi_status_description(bmi_value))
#     # 將計算結果更新到 result_label 文字內容
#     result_label.configure(text=result)

# def get_bmi_status_description(bmi_value):
#     if bmi_value < 18.5:
#         return '體重過輕囉，多吃點！'
#     elif bmi_value >= 18.5 and bmi_value < 24:
#         return '體重剛剛好，繼續保持！'
#     elif bmi_value >= 24 :
#         return '體重有點過重囉，少吃多運動！'

# # font設定字體跟大小
# # bg設定背景顏色
# # fg設定字體顏色
# # row：定義這個部件坐落在哪一列，如row=2
# # column：定義這個部件坐落在哪一欄，如column=2
# # rowspan：定義這個部件跨幾列，如rowspan=2
# # columnspan：定義這個部件跨幾欄，如columnspan=2
# # padx､pady：定義部件與cell邊框的橫縱向的距離，如padx=10
# # ipadx､ipady：定義部件與部件間橫縱向的距離，如ipadx=5
# # label
# label1 = tk.Label( window, text = "帳號", font = ('Arial', 12 ), bg = 'yellow', fg = 'black' )
# label1.grid( row = 0, column = 0 )
# label2 = tk.Label( window, text = "密碼", font = ( '', 12 ), bg = 'gray', fg = 'blue' )
# label2.grid( row = 1, column = 0 )

# # entry
# height_entry = tk.Entry( window )
# height_entry.grid( row = 0, column = 1 )
# weight_entry = tk.Entry( window )
# weight_entry.grid( row = 1, column = 1 )

# # button
# button1 = tk.Button( window, text = '登    入', bg = 'blue',activebackground = 'RED', font = 8, bd = 4, command = calculate_bmi_number )
# button1.grid( row = 2, column = 0, columnspan = 2, sticky = 'we' )
# button2 = tk.Button( window, text = '加入會員', bg = 'blue',activebackground = 'RED', font = 8, bd = 4 )
# button2.grid( row = 2, column = 2, columnspan = 1, sticky = 'we' )
# button3 = tk.Button( window, text = '與我聯繫', bg = 'blue',activebackground = 'RED', font = 8, bd = 4 )
# button3.grid( row = 2, column = 3, columnspan = 1, sticky = 'we' )

# btnstr = tk.StringVar() # 初始化tk的字串變數
# btnstr.set( '按看看' )
# btn = tk.Button( window, bg='violet', fg='black', textvariable=btnstr, font=('微軟正黑體', 20), command = calculate )
# btn.grid( row = 2, column = 4 )

# result_label = tk.Label(window)
# result_label.grid( row = 3, column = 3, columnspan = 1, sticky = 'we' )

# window.mainloop()

""" 
這個看懂了，不過用pack感覺比較不好用
 """
# # 這個步驟建立一個主視窗
# window = tk.Tk()
# # 設定視窗標題、大小和背景顏色
# window.title('BMI App')
# window.geometry('800x600')
# window.configure(background='white')
# window.resizable(False, False) # 如果不想讓使用者能調整視窗大小的話就均設為False

# # window2 = tk.Tk()
# # # 設定視窗標題、大小和背景顏色
# # window2.title('App')
# # window2.geometry('800x600')
# # window2.configure(background='white')
# # window2.resizable(False, False) # 如果不想讓使用者能調整視窗大小的話就均設為False

# # 以下為 height_frame 群組
# # 先建立frame到window裡面
# height_frame = tk.Frame(window)
# # height_frame = tk.Frame(window2)
# # 向上對齊父元件
# # height_frame.pack(side=tk.TOP)
# # height_label = tk.Label(height_frame, text='身高（m）')
# # height_label.pack(side=tk.LEFT)
# # height_entry = tk.Entry(height_frame)
# # height_entry.pack(side=tk.LEFT)

# # 運行主程式
# window.mainloop()
# # window2.mainloop()


""" 
1.繼承tk.frame
2.master不知道幹嘛的
3.標籤使用tk.Label
4.按鈕使用tk.Button
5.mbox.messagebox
網址：https://www.itread01.com/content/1552777204.html
 """
# import tkinter as tk
# import tkinter.messagebox as mbox


# # 定義MainUI類表示應用/視窗，繼承Frame類
# class MainUI(tk.Frame):
#     # Application建構函式，master為視窗的父控制元件
#     def __init__(self, master = None):
#         # 初始化Application的Frame部分 
#         tk.Frame.__init__(self, master)
#         # 顯示視窗，並使用grid佈局
#         self.grid()
#         # 建立控制元件
#         self.createWidgets()


#     # 建立控制元件
#     def createWidgets(self):
#         # 建立一個標籤，輸出要顯示的內容
#         self.firstLabel = tk.Label(self,text="「人人都是Pythonista」專注Python領域，做最專業的Python星球。")
#         # 設定使用grid佈局
#         self.firstLabel.grid()
#         # 建立一個按鈕，用來觸發answer方法
#         self.clickButton = tk.Button(self,text="點一下瞧瞧？",command=self.answer)
#         # 設定使用grid佈局
#         self.clickButton.grid()


#     def answer(self):
#         # 我們通過 messagebox 來顯示一個提示框
#         mbox.showinfo("「人人都是Pythonista」",'''
#         這是一個專注Python的星球，我們提供「從零單排」、「實戰專案」、「大航海」、「技術沙龍」、「技術分享」、「大廠內推」等系列供你選擇及學習，當然也會有周邊技術沿伸。
#         本星球會不定期開展各類實戰專案，階段性組織線上技術沙龍、分享等；對於職業發展路線不明確的，我們會邀請到一些大廠hr及高階開發、經理等給大家解惑。
#         加入我們，和千人一起玩Python，To be a Pythonista！
#         ''')


# # 建立一個MainUI物件
# app = MainUI()
# # 設定視窗標題
# app.master.title('「人人都是Pythonista」')
# # 設定窗體大小
# app.master.geometry('800x450')
# # 主迴圈開始
# app.mainloop()
