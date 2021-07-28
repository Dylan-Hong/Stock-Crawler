from tkinter.constants import END
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, filedialog
import SystematicInvest
import Function_def as Func
import threading

class MainWindow( tk.Tk ):
    def __init__( self, title, size ) -> None:
        # 這個可以實作父類別的建構子，要寫這個才能用
        super().__init__()
        # 設定這個window的名稱跟尺寸
        self.title( title )
        self.geometry( size )

        # 建立主選單的notebook
        self.MainNBGroup = ttk.Notebook( self )
        self.MainNBGroup.place( x = 0, y = 0, width = 800, height = 450 )
        
        # 建立tab
        # 基本參數tab
        self.Tab_Parameter = cMT_Parameter( self, self.MainNBGroup, '基本參數' )

        # 定期定額tab
        self.Tab_SysInvest = cMT_SysInvest( self, self.MainNBGroup, '定期定額' )

        # 建立新功能的tab
        self.Tab_Unknow = cMT_Unknown( self, self.MainNBGroup, '新功能' )

        # 預設開啟就選擇在定期定額，方便測試
        self.MainNBGroup.select( self.Tab_SysInvest )


# tab的最基礎class
class cTab( tk.Frame ):
    def __init__( self, MainWindow : MainWindow, NBGroup, TabName ):
        super().__init__( NBGroup )
        self.pMainWindow = MainWindow
        NBGroup.add( self, text = TabName)

class cMT_Parameter( cTab ):
    def __init__( self, MainWindow : MainWindow, NBGroup : ttk.Notebook, TabName ):
        super().__init__( MainWindow, NBGroup, TabName )
        StartX = 0
        width_5 = 80
        width_1 = 20
        height_1 = 20
        width_entry = 100

        # 存檔路徑
        StartY = 10
        # 存檔路徑label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_Path = tk.Label( self, text = '存檔路徑 : ' )
        label_Path.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 存檔路徑entry
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, 200, Hei ]
        self.entry_Path = tk.Entry( self )
        self.entry_Path.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.entry_Path.insert( 0, './' )
        # 存檔路徑button
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_5, Hei ]
        self.Button_SetPath = tk.Button( self, text = '設定', command = self.LoadPath )
        self.Button_SetPath.place( x = PosX, y = PosY, width = Wid, height = Hei )

        # 稅率
        StartY += 20
        # 稅率 label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_TaxRate = tk.Label( self, text = '稅率 : ' )
        label_TaxRate.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 稅率 radio button，設定為0.3%或是0.15%單選
        self.TaxRate1 = tk.DoubleVar()
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_entry, Hei ]
        self.radbutton_TaxRate1 = tk.Radiobutton( self, text = '0.3%', variable = self.TaxRate1, value = 0.003 )
        self.radbutton_TaxRate1.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.radbutton_TaxRate2 = tk.Radiobutton( self, text = '0.15%', variable = self.TaxRate1, value = 0.0015 )
        self.radbutton_TaxRate2.place( x = PosX + Wid, y = PosY, width = Wid, height = Hei )
        # 預設0.3%
        self.radbutton_TaxRate1.select()

        # 手續費
        StartY += 20
        # 手續費label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_FeeRate = tk.Label( self, text = '手續費 : ' )
        label_FeeRate.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 手續費entry
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_entry, Hei ]
        self.entry_FeeRate = tk.Entry( self )
        self.entry_FeeRate.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.entry_FeeRate.insert( 0, 0.1425 )
        # 手續費 % label
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, StartY, width_1, height_1 ]
        label_FeeRate = tk.Label( self, text = '%' )
        label_FeeRate.place( x = PosX, y = PosY, width = Wid, height = Hei )

        # 儲存參數button
        button_SaveParam = tk.Button( self, text = '儲存參數', command = self.SaveParam )
        button_SaveParam.place( x = 200, y = 100, width = width_5, height = height_1 )
        
        # 建立tab的時候，先存下預設的參數
        self.SaveParam()

    def LoadPath( self ):
        self.entry_Path.insert( 0, filedialog.askdirectory() )

    def SaveParam( self ):
        self.Path = self.entry_Path.get()
        self.TaxRate = float( self.TaxRate1.get() )
        self.FeeRate = float( self.entry_FeeRate.get() ) * 0.01

class cMT_SysInvest( cTab ):
    def __init__( self, MainWindow : MainWindow,  NBGroup : ttk.Notebook, TabName ):
        super().__init__( MainWindow, NBGroup, TabName )
        # 設定Notebook of subtab
        self.SubNBGroup = ttk.Notebook( self )
        self.SubNBGroup.place( x = 0, y = 0, width = 750, height = 400 )
        # 新增subtab : 參數設定
        self.SubTab_InputParam = cST_SubTab_InputParam( self.pMainWindow, self.SubNBGroup, '參數設定' )
        # 新增subtab試算結果
        self.SubTab_Result = cST_SubTab_Result( self.pMainWindow, self.SubNBGroup, '試算結果' )
        # 新增subtab圖表輸出
        self.SubTab_Picture = cST_SubTab_Picture( self.pMainWindow, self.SubNBGroup, '圖表輸出' )

        self.SubNBGroup.select( self.SubTab_InputParam )

class cMT_Unknown( cTab ):
    def __init__( self, MainWindow : MainWindow,  NBGroup : ttk.Notebook, TabName ):
        super().__init__( MainWindow, NBGroup, TabName )
        label = tk.Label( self, text = '新功能放在這邊' )
        label.place( x = 10, y = 10, width = 100, height = 20 )

class cST_SubTab_InputParam( cTab ):
    def __init__( self, MainWindow : MainWindow,  NBGroup : ttk.Notebook, TabName ):
        super().__init__( MainWindow, NBGroup, TabName )
        StartX = 0
        width_5 = 80
        width_1 = 20
        height_1 = 30
        width_entry = 75
        width_year = 75
        width_month = 50

        # 起始日期
        StartY = 10
        # 起始日期 label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_StartDate = tk.Label( self, text = '起始日期 : ' )
        label_StartDate.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 起始日期 年Combobox
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_year, Hei ]
        self.Combobox_StartYear = ttk.Combobox( self , value = Func.GetYearArrayStr() )
        self.Combobox_StartYear.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.Combobox_StartYear.current( 70 )
        # 起始日期 年label
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_1, Hei ]
        label_StartYear = tk.Label( self, text = '年' )
        label_StartYear.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 起始日期 月Combobox
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_month, Hei ]
        self.Combobox_StartMonth = ttk.Combobox( self , value = Func.GetMonthArrayStr() )
        self.Combobox_StartMonth.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.Combobox_StartMonth.current( 0 )
        # 起始日期 月label
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_1, Hei ]
        label_StartMonth = tk.Label( self, text = '月' )
        label_StartMonth.place( x = PosX, y = PosY, width = Wid, height = Hei )

        # 結束日期
        StartY += Hei
        # 結束日期label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_EndDate = tk.Label( self, text = '結束日期 : ' )
        label_EndDate.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 結束日期 年Combobox
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_year, Hei ]
        self.Combobox_EndYear = ttk.Combobox( self , value = Func.GetYearArrayStr() )
        self.Combobox_EndYear.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.Combobox_EndYear.current( 70 )
        # 結束日期 年label
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_1, Hei ]
        label_EndYear = tk.Label( self, text = '年' )
        label_EndYear.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 結束日期 月Combobox
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_month, Hei ]
        self.Combobox_EndMonth = ttk.Combobox( self , value = Func.GetMonthArrayStr() )
        self.Combobox_EndMonth.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.Combobox_EndMonth.current( 0 )
        # 結束日期 月label
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_1, Hei ]
        label_EndMonth = tk.Label( self, text = '月' )
        label_EndMonth.place( x = PosX, y = PosY, width = Wid, height = Hei )

        # 股票號碼
        StartY += Hei
        # 股票號碼label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_StockNum = tk.Label( self, text = '股票號碼 : ' )
        label_StockNum.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 股票號碼entry
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_entry, Hei ]
        self.entry_StockNum = tk.Entry( self )
        self.entry_StockNum.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.entry_StockNum.insert( 0, '2330' )

        # 投資金額
        StartY += Hei
        # 投資金額label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_InvestAmount = tk.Label( self, text = '投資金額 : ' )
        label_InvestAmount.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 投資金額entry
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_entry, Hei ]
        self.entry_InvestAmount = tk.Entry( self )
        self.entry_InvestAmount.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.entry_InvestAmount.insert( 0, '10000' )
        # 投資金額單位label
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_5, Hei ]
        label_InvestFreq = tk.Label( self, text = 'NTD' )
        label_InvestFreq.place( x = PosX, y = PosY, width = Wid, height = Hei )

        # 投資頻率
        StartY += Hei
        # 投資金額label
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_InvestFreq = tk.Label( self, text = '投資頻率 : ' )
        label_InvestFreq.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 投資金額entry
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_entry, Hei ]
        self.entry_InvestFreq = tk.Entry( self )
        self.entry_InvestFreq.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.entry_InvestFreq.insert( 0, '1' )
        # 投資金額單位label
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, PosY, width_5, Hei ]
        label_InvestFreq = tk.Label( self, text = '月 / 次' )
        label_InvestFreq.place( x = PosX, y = PosY, width = Wid, height = Hei )
        
        # 開始計算按鈕
        StartX = width_1 + width_entry * 2
        StartY += Hei
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        self.button_StartCalc = tk.Button( self, text = '開始計算', command = self.Thread_Calc_InputParam )
        self.button_StartCalc.place( x = PosX, y = PosY, width = Wid, height = Hei )
        
        # 進度條
        StartY += Hei
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        # indeterminate就是會一直跑
        self.Progressbar = ttk.Progressbar( self, mode="indeterminate" )
        self.Progressbar.place( x = PosX, y = PosY, width = Wid, height = Hei )

    def Thread_Calc_InputParam( self ):
        # 因為設定成thread後，只能執行一次，因此要另外call 一個funtcion每次按下按鈕，就設定一次thread
        t = threading.Thread( target = self.Calc_InputParam )
        t.start()

    def Calc_InputParam( self ):
        # 初始化模組需要資料
        self.df_log = pd.DataFrame( columns = [ '買進日期', '買進價格', '買進數量(股)', '買進金額', \
        '持股數量', '持股均價', '持股成本', '損益金額', '損益比例' ] )
        self.df_ProfitAndLoss = pd.DataFrame( columns = [ '計算日期', '損益金額', '損益比例' ] )
        self.df_MaxLoss = pd.DataFrame( columns = [ '項目', '日期', '總投入資金', '虧損金額', '虧損比例' ] )
        self.FileName = ''
        self.EndDate = ''
        self.MaxLossDate = ''
        self.MaxLoss = 0
        self.MaxLossRatioDate = ''
        self.PLAmount = 0
        self.PLRatio = 0
        self.MaxLossRatio = 0
        self.PLRecord = []

        # 清除Listbox
        self.pMainWindow.Tab_SysInvest.SubTab_Result.ClearList()
        # 執行計算
        SystematicInvest.Calc( self )
        # 印出結果
        self.pMainWindow.Tab_SysInvest.SubTab_Result.Calc_PrintResult()

class cST_SubTab_Result( cTab ):
    def __init__( self, MainWindow : MainWindow,  NBGroup : ttk.Notebook, TabName ):
        super().__init__( MainWindow, NBGroup, TabName )
        StartX = 0
        width_5 = 80
        height_1 = 20
        StartY = 10

        # 結算日期
        # 標題
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_SettleDate = tk.Label( self, text = '結算日期 : ' )
        label_SettleDate.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 結果
        self.EndDate = tk.StringVar()
        [ PosX, PosY, Wid, Hei ] = [ StartX + Wid, StartY, width_5, height_1 ]
        label_oEndDate = tk.Label( self, textvariable = self.EndDate )
        label_oEndDate.place( x = PosX, y = PosY, width = Wid, height = Hei )

        StartY += height_1
        # 損益金額
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_PLAmount = tk.Label( self, text = '損益金額 : ' )
        label_PLAmount.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.PLAmount = tk.IntVar()
        [ PosX, PosY, Wid, Hei ] = [ StartX + Wid, StartY, width_5, height_1 ]
        label_oPLAmount = tk.Label( self, textvariable = self.PLAmount )
        label_oPLAmount.place( x = PosX, y = PosY, width = Wid, height = Hei )

        StartY += height_1
        # 損益比例
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_PLRatio = tk.Label( self, text = '損益比例 : ' )
        label_PLRatio.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.PLRatio = tk.DoubleVar()
        [ PosX, PosY, Wid, Hei ] = [ StartX + Wid, StartY, width_5, height_1 ]
        label_oPLRatio = tk.Label( self, textvariable = self.PLRatio )
        label_oPLRatio.place( x = PosX, y = PosY, width = Wid, height = Hei )

        # 最高虧損比例
        StartY += height_1
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_MaxLossRatio = tk.Label( self, text = '最高虧損比例 : ', anchor = 'w' )
        label_MaxLossRatio.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 日期
        self.MaxLossRatioDate = tk.StringVar()
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, StartY, width_5, height_1 ]
        label_oMaxLossRatioDate = tk.Label( self, textvariable = self.MaxLossRatioDate )
        label_oMaxLossRatioDate.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.MaxLossRatioDate.set( '---/--/--' )
        # 比例
        self.MaxLossRatio = tk.DoubleVar()
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, StartY, width_5, height_1 ]
        label_oMaxLossRatio = tk.Label( self, textvariable = self.MaxLossRatio )
        label_oMaxLossRatio.place( x = PosX, y = PosY, width = Wid, height = Hei )
 
        # 最高損益金額
        StartY += height_1
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        label_MaxLoss = tk.Label( self, text = '最高虧損金額 : ', anchor = 'w' )
        label_MaxLoss.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 日期
        self.MaxLossDate = tk.StringVar()
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, StartY, width_5, height_1 ]
        label_oMaxLossDate = tk.Label( self, textvariable = self.MaxLossDate )
        label_oMaxLossDate.place( x = PosX, y = PosY, width = Wid, height = Hei )
        self.MaxLossDate.set( '---/--/--' )
        # 比例
        self.MaxLoss = tk.IntVar()
        [ PosX, PosY, Wid, Hei ] = [ PosX + Wid, StartY, width_5, height_1 ]
        label_oMaxLoss = tk.Label( self, textvariable = self.MaxLoss )
        label_oMaxLoss.place( x = PosX, y = PosY, width = Wid, height = Hei )

        # 輸出excel button
        StartY += 25
        [ PosX, PosY, Wid, Hei ] = [ width_5 * 3, StartY, width_5, height_1 ]
        button_StartCalc = tk.Button( self, text = '輸出excel', command = self.ExportLog )
        button_StartCalc.place( x = PosX, y = PosY, width = Wid, height = Hei )

        # 交易紀錄ListBox
        StartY += height_1
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5 * 8, height_1 * 8 ]
        self.List_Log = tk.Listbox( self, width = 380 )
        self.List_Log.place( x = PosX, y = PosY, width = Wid, height = Hei )
        # 生成的時候先寫入第一欄標題
        str = '買進日期'.ljust( 13 )
        str = str +'買進價格'.ljust( 8 )
        str = str +'買進數量(股)'.ljust( 10 )
        str = str +'買進金額'.ljust( 8 )
        str = str +'持股數量'.ljust( 8 )
        str = str +'持股均價'.ljust( 8 )
        str = str +'持股成本'.ljust( 8 )
        str = str +'損益金額'.ljust( 8 )
        str = str +'損益比例'.ljust( 8 )
        self.List_Log.insert( 0, str )
    
    def Calc_PrintResult( self ):
        InputParam = self.pMainWindow.Tab_SysInvest.SubTab_InputParam
        self.EndDate.set( InputParam.EndDate )
        self.PLAmount.set( '{:.0f}'.format( InputParam.PLAmount ) )
        self.PLRatio.set( '{:.2%}'.format( InputParam.PLRatio ) )
        self.MaxLossRatioDate.set( InputParam.MaxLossRatioDate )
        self.MaxLossRatio.set( InputParam.MaxLossRatio )
        self.MaxLossDate.set( InputParam.MaxLossDate )
        self.MaxLoss.set( InputParam.MaxLoss )

    def ExportLog( self ):
        SystematicInvest.SaveFile( self.pMainWindow.Tab_SysInvest.SubTab_InputParam )

    def InsertLogToList( self, Content ):
        # 寫入在最後一欄
        self.List_Log.insert( END, Content )

    def ClearList( self ):
        # 除了標題以外都清掉
        self.List_Log.delete( 1, END )

class cST_SubTab_Picture( cTab ):
    def __init__( self, MainWindow : MainWindow,  NBGroup : ttk.Notebook, TabName ):
        super().__init__( MainWindow, NBGroup, TabName )
        StartX = 0
        width_5 = 80
        height_1 = 20
        # 視窗內畫圖 button
        StartY = 10
        [ PosX, PosY, Wid, Hei ] = [ StartX, StartY, width_5, height_1 ]
        button_StartCalc = tk.Button( self, text = '視窗內畫圖', command = self.PlotDiagramInTk )
        button_StartCalc.place( x = PosX, y = PosY, width = Wid, height = Hei )

        [ PosX, PosY, Wid, Hei ] = [ StartX + Wid, StartY, width_5, height_1 ]
        button_StartCalc = tk.Button( self, text = '新視窗畫圖', command = self.PlotNewWindow )
        button_StartCalc.place( x = PosX, y = PosY, width = Wid, height = Hei )

    def PlotDiagramInTk( self ):
        # 圖表輸出到tab，這部分其他設定也不會用
        fig = Figure()
        a = fig.add_subplot(111)
        a.plot( self.pMainWindow.Tab_SysInvest.SubTab_InputParam.PLRecord )
        canvas = FigureCanvasTkAgg( fig, self )
        canvas.get_tk_widget().place( x = 30, y = 30, width = 700, height = 300 )
    
    def PlotNewWindow( self ):
        PLRecord = self.pMainWindow.Tab_SysInvest.SubTab_InputParam.PLRecord
        plt.figure( figsize = ( 8, 4.5 ) )
        plt.plot( PLRecord )
        plt.title( "Change of Profit and Loss" )
        plt.xlabel( 'Trade day' )
        plt.ylabel( 'Profit and Loss' )
        plt.grid()
        plt.xlim( [ 0, len( PLRecord )])
        plt.show()
