import tkinter as tk
from tkinter import ttk
import math
import Function_def as Func
import SystematicInvest as S

class MainWindow( tk.Tk ):
    def __init__(self, title, size) -> None:
        # 這個可以實作父類別的建構子，要寫這個才能用
        super().__init__()
        # 設定這個window的名稱跟尺寸
        self.title( title )
        self.geometry( size )
        self.SetMainNBGroup()

    def SetMainNBGroup( self ):
        # 建立主選單的notebook
        self.MainNBGroup = ttk.Notebook( self )
        self.MainNBGroup.place( x = 0, y = 0, width = 800, height = 450 )
        
        # 建立tab
        # 基本參數tab
        self.Tab_Parameter = MainTab( self, '基本參數' )
        self.Tab_Parameter.SetParameter()

        # 定期定額tab
        self.Tab_SysInvest = MainTab( self, '定期定額' )
        self.Tab_SysInvest.SetSysInvest( self )

        # 建立新功能的tab
        self.Tab_Unknow = MainTab( self, '新功能' )
        self.Tab_Unknow.SetUnknown()

        # 預設開啟就選擇在定期定額，方便測試
        self.MainNBGroup.select( self.Tab_SysInvest )


class MainTab( tk.Frame ):
    def __init__( self, MainWindow, TabName ):
        super().__init__( MainWindow.MainNBGroup )
        self.TabName = TabName
        MainWindow.MainNBGroup.add( self, text = self.TabName )

    def SetParameter( self ):
        label = tk.Label( self, text = '這邊放基本參數設定，例如稅率、手續費' )
        label.place( x = 10, y = 10, width = 300, height = 20 )
        # label = tk.Label( self, text = '存檔路徑 : ' )
        # label.place( x = 10, y = 10, width = 100, height = 20 )
        pass

    def SetSysInvest( self, MainWindow ):
        self.SubNBGroup = ttk.Notebook( self )
        self.SubNBGroup.place( x = 0, y = 0, width = 720, height = 405 )
        self.SubTab_InputParam = SubTab( self, '參數設定' )
        self.SubTab_InputParam.SetSysInvest_InputParam()
        self.SubTab_Result = SubTab( self, '試算結果' )
        self.SubTab_Result.SetSysInvest_Result()
        self.SubTab_Picture = SubTab( self, '圖表輸出' )
        self.SubNBGroup.select( self.SubTab_InputParam )

    def SetUnknown( self ):
        label = tk.Label( self, text = '新功能放在這邊' )
        label.place( x = 10, y = 10, width = 100, height = 20 )


class SubTab( tk.Frame ):
    def __init__( self, MainTab : MainTab, TabName ):
        super().__init__( MainTab.SubNBGroup )
        self.TabName = TabName
        MainTab.SubNBGroup.add( self, text = self.TabName )

    def SetSysInvest_InputParam( self ):
        StartX = 0
        width_5 = 80
        width_1 = 20
        height_1 = 20
        width_entry = 50

        # 起始日期
        StartY = 10
        # 起始日期 label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_StartDate = tk.Label( self, text = '起始日期 : ' )
        label_StartDate.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 起始日期 年entry
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_entry, Hei ]
        self.entry_StartYear = tk.Entry( self )
        self.entry_StartYear.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.entry_StartYear.insert( 0, '2020' )
        # 起始日期 年label
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_1, Hei ]
        label_StartYear = tk.Label( self, text = '年' )
        label_StartYear.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 起始日期 月entry
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_entry, Hei ]
        self.entry_StartMonth = tk.Entry( self )
        self.entry_StartMonth.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.entry_StartMonth.insert( 0, '10' )
        # 起始日期 月label
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_1, Hei ]
        label_StartMonth = tk.Label( self, text = '月' )
        label_StartMonth.place( x = PosX, y = PosY, width = Wid, height = Hei )

        StartY += 20
        # 結束日期label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_EndDate = tk.Label( self, text = '結束日期 : ' )
        label_EndDate.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 起始日期 年entry
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_entry, Hei ]
        self.entry_EndYear = tk.Entry( self )
        self.entry_EndYear.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 起始日期 年label
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_1, Hei ]
        label_EndYear = tk.Label( self, text = '年' )
        label_EndYear.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 起始日期 月entry
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_entry, Hei ]
        self.entry_EndMonth = tk.Entry( self )
        self.entry_EndMonth.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 起始日期 月label
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_1, Hei ]
        label_EndMonth = tk.Label( self, text = '月' )
        label_EndMonth.place( x = PosX, y = PosY, width = Wid, height = Hei )

        # 股票號碼
        StartY += 20
        # 股票號碼label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_StockNum = tk.Label( self, text = '股票號碼 : ' )
        label_StockNum.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 股票號碼entry
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_entry, Hei ]
        self.entry_StockNum = tk.Entry( self )
        self.entry_StockNum.place( x = PosX, y = PosY, width = Wid, height = Hei )

        # 投資金額
        StartY += 20
        # 投資金額label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_InvestAmount = tk.Label( self, text = '投資金額 : ' )
        label_InvestAmount.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 投資金額entry
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_entry, Hei ]
        self.entry_InvestAmount = tk.Entry( self )
        self.entry_InvestAmount.place( x = PosX, y = PosY, width = Wid, height = Hei )
        
        # 開始計算按鈕
        StartX = width_1 * 2 + width_entry * 2
        StartY += 25
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        button_StartCalc = tk.Button( self, text = '開始計算', command = self.Calc_InputParam )
        button_StartCalc.place( x = PosX, y = PosY, width = Wid, height = Hei )
        
    def SetSysInvest_Result( self ):
        label_PLAmount = tk.Label( self, text = '損益金額 : ' )
        label_PLAmount.place( x = 10, y = 10, width = 80, height = 20 )

    
    def Calc_InputParam( self ):
        S.SystematicInvest( self )
        # 這個可以隱藏
        # self.label_InvestAmount.place_forget()

window = MainWindow( 'Stock Crawler', '800x450' )
window.mainloop()









# ------------------以下為練習留存-------------------




"""
Notebook分頁功能
window底下建立Notebook
在Notebook底下建立建立frame
在用notebook.add
 """

# window =tk.Tk()  # 創建窗口對象
# window.title(string = 'ttk.Notebook')  #設置窗口標題
# window.geometry('800x600')

# Notebook1 = ttk.Notebook(window)  #創建Notebook
# tab1 = tk.Frame(Notebook1, bg = 'white') 
# Notebook1.add(tab1, text='第一個分頁')

# tab2 = tk.Frame(Notebook1,bg='white')
# Notebook1.add(tab2, text='第二個分頁')

# label1 = tk.Label( tab2, text='test' )
# label1.place( x = 0, y = 0, width = 100, height = 20 )

# Notebook1.place( x = 10, y = 10, width = 500, height = 500 )

# Notebook1.select(tab1) #選擇tab1

# window.mainloop()     # 進入消息循環


""" 
這邊練習用place
 """
# window = tk.Tk()
# window.geometry( '800x600' )
# window.configure( background='white' )
# window.title( 'place測試' )

# def updateAfterCombo():
#     output1.set( int( comGrade.get() ) )
#     print( type(comGrade.get()) )

# # http://andrewpythonarduino.blogspot.com/2018/04/python_6.html
# # label用法補充
# # wraplength可以指定多少寬度之後要換行
# # justify指定換行要對其左邊還是中間還是右邊(left, right, center)
# # anchor指定要放到哪邊(w, e, n, s, c)
# # 這邊的width都重複設定了，感覺可以place設定就好，不過跟著label也很方便，不過這兩個width單位不同
# label1 = tk.Label(window, text = '要是打很長會出現到第二行:', wraplength = 100, justify='left', width=50)
# label1.place(x=10, y=100, width=100, height=80)
# label2 = tk.Label(window, text = '選擇數字:', anchor = 'e', justify='left', width=50)
# label2.place(x=10, y=10, width=100, height=20)
# output1 = tk.IntVar()
# output1.set( 1 )
# label3 = tk.Label( window, textvariable = output1, anchor = 'c', width=20 )
# # label3.place( x=10, y = 60, height = 20 )
# label3.place( x=10, y = 200, width = 100, height = 20 )


# # ComboBox
# stdGrade = ['1', '2', '3']

# comGrade = ttk.Combobox(window, width=50, values=stdGrade)
# comGrade.place(x=110, y=10, width=50, height=20 )
# print( comGrade.get() )

# button1 = tk.Button( window, text = '更新', anchor = 'c', command = updateAfterCombo )
# button1.place( x = 10, y = 220, width = 100, height = 20 )

# # Radiobutton
# # 透過設定variable為相同的變數，就可以變成同一個群組
# RadiobutLabel1 = tk.Label(window, text = '單選按鈕', justify=tk.RIGHT, width=50)
# RadiobutLabel1.place(x=10, y=70, width=100, height=20)

# RadioVar = tk.IntVar()
# RadioVar.set(1)       # 預設值1
# rad1 = tk.Radiobutton(window, variable=RadioVar, value=1,text='1')
# rad1.place(x=110, y=70, width=60, height=20)
# rad2 = tk.Radiobutton(window, variable=RadioVar, value=0,text='2')
# rad2.place(x=190, y=70, width=60, height=20)

# # Checkbutton
# signin = tk.StringVar()
# signin.set('abc')       # 預設值0=未報到
# chkSignin = tk.Checkbutton(window, text='CheckButton', variable=signin, onvalue='aaa', offvalue='bbb')
# chkSignin.place(x=300, y=100, width=100, height=20)
# label3 = tk.Label( window, textvariable = signin, anchor = 'c', width=20 )
# label3.place( x=400, y = 100, width = 100, height = 20 )

# # Listbox
# # 建立一個框框，利用listbox.insert可以輸入東西，第一個引數是要從第幾行開始新增的意思
# def addInfo():
#     result = '年級:' + comGrade.get()
#     result += ';性別:' + ('1' if RadioVar.get() else '0')
#     result += ';報到:' + ('是' if signin.get() else '否')
#     lstStudent.insert( 0, result)
   
# btnAdd = tk.Button(window, text='加入', width=40, command=addInfo)
# btnAdd.place(x=200, y=210, width=100, height=20)

# btnDel = tk.Button(window, text='刪除', width=40, command=addInfo)
# btnDel.place(x=300, y=210, width=100, height=20)

# lstStudent = tk.Listbox(window, width=380)
# lstStudent.place(x=200, y=230, width=380, height=180)
# window.mainloop()


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
