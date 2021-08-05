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

def Create_NoteBook( InputFrame, iX, iY, iWid, iHei ):
    NoteBook = ttk.Notebook( InputFrame )
    NoteBook.place( x = iX, y = iY, width = iWid, height = iHei )
    return NoteBook

def Create_Label( InputFrame, iText, iRow, iColumn, iSticky, iColspan ):
    Label = ttk.Label( InputFrame, text = iText )
    Label.grid( row = iRow, column = iColumn, sticky = iSticky, columnspan = iColspan, padx = 5, pady = 5 )

def Create_LabelVar( InputFrame, iRow, iColumn, iSticky, iColspan, type ):
    if type == 'Str':
        Var = tk.StringVar()
    elif type == 'Int':
        Var = tk.IntVar()
    elif type == 'Double':
        Var = tk.DoubleVar()
    Label = ttk.Label( InputFrame, textvariable = Var )
    Label.grid( row = iRow, column = iColumn, sticky = iSticky, columnspan = iColspan, padx = 5, pady = 5 )
    return Var

def Create_Entry( InputFrame, iRow, iColumn, iSticky, iColspan ):
    Entry = ttk.Entry( InputFrame )
    Entry.grid( row = iRow, column = iColumn, sticky = iSticky, columnspan = iColspan, padx = 5, pady = 5 )
    return Entry

def Create_Button( InputFrame, iText, iCommand, iRow, iColumn, iSticky, iColspan ):
    Button = ttk.Button( InputFrame, text = iText, command = iCommand )
    Button.grid( row = iRow, column = iColumn, sticky = iSticky, columnspan = iColspan, padx = 5, pady = 5 )

def Create_Radiobutton( InputFrame, iText, iVar, iValue, iRow, iColumn, iSticky, iColspan ):
    Radiobutton = tk.Radiobutton( InputFrame, text = iText, variable = iVar, value = iValue )
    Radiobutton.grid( row = iRow, column = iColumn, sticky = iSticky, columnspan = iColspan, padx = 5, pady = 5 )
    return Radiobutton

def Create_Combobox( InputFrame, StrArr, iRow, iColumn, iSticky, iColspan ):
    Combobox = ttk.Combobox( InputFrame , value = StrArr )
    Combobox.grid( row = iRow, column = iColumn, sticky = iSticky, columnspan = iColspan, padx = 5, pady = 5 )
    return Combobox

def Create_Progressbar( InputFrame, iMode, iRow, iColumn, iSticky, iColspan ):
    Progressbar = ttk.Progressbar( InputFrame, mode = iMode )
    Progressbar.grid( row = iRow, column = iColumn, sticky = iSticky, columnspan = iColspan, padx = 5, pady = 5 )
    return Progressbar
    
def Create_ListBox( InputFrame, iWidth, iRow, iColumn, iSticky, iColspan ):
    ListBox = tk.Listbox( InputFrame, width = iWidth )
    ListBox.grid( row = iRow, column = iColumn, sticky = iSticky, columnspan = iColspan, padx = 5, pady = 5 )
    return ListBox

class MainWindow( tk.Tk ):
    def __init__( self, title, size ) -> None:
        # 這個可以實作父類別的建構子，要寫這個才能用
        super().__init__()
        # 設定這個window的名稱跟尺寸
        self.title( title )
        self.geometry( size )

        # 建立主選單的notebook
        self.MainNBGroup = Create_NoteBook( self, 0, 0, 900, 500 )
        
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

        # 存檔路徑label
        label_Path = Create_Label( self, '存檔路徑 : ', 0, 0, 'w', 1 )
        # 存檔路徑entry
        self.entry_Path = Create_Entry( self, 0, 1, 'w', 2 )
        self.entry_Path.insert( 0, './' )
        # 存檔路徑button
        self.Button_SetPath = Create_Button( self, '設定', self.LoadPath, 0, 3, 'w', 1 )

        # 稅率 label
        Create_Label( self, '稅率 : ', 1, 0, 'w', 1 )
        # 稅率 radio button，設定為0.3%或是0.15%單選
        self.TaxRateVar = tk.DoubleVar()
        self.radbutton_TaxRate1 = Create_Radiobutton( self, '0.3%', self.TaxRateVar, 0.003, 1, 1, 'w', 1 )
        self.radbutton_TaxRate2 = Create_Radiobutton( self, '0.15%', self.TaxRateVar, 0.0015, 1, 2, 'w', 1 )
        # 預設0.3%
        self.radbutton_TaxRate1.select()

        # 手續費label
        Create_Label( self, '手續費 : ', 2, 0, 'w', 1 )

        # 手續費entry
        self.entry_FeeRate = Create_Entry( self, 2, 1, 'w', 2 )
        self.entry_FeeRate.insert( 0, 0.1425 )

        # 手續費 % label
        Create_Label( self, '%', 2, 3, 'w', 1 )

        # 儲存參數button
        Create_Button( self, '儲存參數', self.SaveParam, 4, 3, 'w', 1 )
        
        # 建立tab的時候，先存下預設的參數
        self.SaveParam()

    def LoadPath( self ):
        self.entry_Path.insert( 0, filedialog.askdirectory() )

    def SaveParam( self ):
        self.Path = self.entry_Path.get()
        self.TaxRate = float( self.TaxRateVar.get() )
        self.FeeRate = float( self.entry_FeeRate.get() ) * 0.01

class cMT_SysInvest( cTab ):
    def __init__( self, MainWindow : MainWindow,  NBGroup : ttk.Notebook, TabName ):
        super().__init__( MainWindow, NBGroup, TabName )
        # 設定Notebook of subtab
        self.SubNBGroup = Create_NoteBook( self, 0, 0, 850, 480 )
        # 新增subtab : 參數設定
        self.SubTab_InputParam = cST_SysInvest_InputParam( self.pMainWindow, self.SubNBGroup, '參數設定' )
        # 新增subtab試算結果
        self.SubTab_Result = cST_SysInvest_Result( self.pMainWindow, self.SubNBGroup, '試算結果' )
        # 新增subtab圖表輸出
        self.SubTab_Picture = cST_SysInvest_Picture( self.pMainWindow, self.SubNBGroup, '圖表輸出' )

        self.SubNBGroup.select( self.SubTab_InputParam )

class cMT_Unknown( cTab ):
    def __init__( self, MainWindow : MainWindow,  NBGroup : ttk.Notebook, TabName ):
        super().__init__( MainWindow, NBGroup, TabName )
        label = tk.Label( self, text = '新功能放在這邊' )
        label.place( x = 10, y = 10, width = 100, height = 20 )

class cST_SysInvest_InputParam( cTab ):
    def __init__( self, MainWindow : MainWindow,  NBGroup : ttk.Notebook, TabName ):
        super().__init__( MainWindow, NBGroup, TabName )

        # 起始日期 label
        Create_Label( self, '起始日期 : ', 0, 0, 'w', 1 )
        # 起始日期 年Combobox
        self.Combobox_StartYear = Create_Combobox( self, Func.GetYearArrayStr(), 0, 1, 'w', 1 )
        self.Combobox_StartYear.current( 70 )
        # 起始日期 年label
        Create_Label( self, '年', 0, 2, 'w', 1 )
        # 起始日期 月Combobox
        self.Combobox_StartMonth = Create_Combobox( self, Func.GetMonthArrayStr(), 0, 3, 'w', 1 )
        self.Combobox_StartMonth.current( 0 )
        # 起始日期 月label
        Create_Label( self, '月', 0, 4, 'w', 1 )

        # 結束日期label
        Create_Label( self, '結束日期 : ', 1, 0, 'w', 1 )
        # 結束日期 年Combobox
        self.Combobox_EndYear = Create_Combobox( self, Func.GetYearArrayStr(), 1, 1, 'w', 1 )
        self.Combobox_EndYear.current( 70 )
        # 結束日期 年label
        Create_Label( self, '年', 1, 2, 'w', 1 )
        # 結束日期 月Combobox
        self.Combobox_EndMonth = Create_Combobox( self, Func.GetMonthArrayStr(), 1, 3, 'w', 1 )
        self.Combobox_EndMonth.current( 0 )
        # 結束日期 月label
        Create_Label( self, '月', 1, 4, 'w', 1 )

        # 股票號碼label
        Create_Label( self, '股票號碼 : ', 2, 0, 'w', 1 )
        # 股票號碼entry
        self.entry_StockNum = Create_Entry( self, 2, 1, 'w', 1 )
        self.entry_StockNum.insert( 0, '2330' )

        # 投資金額label
        Create_Label( self, '投資金額 : ', 3, 0, 'w', 1 )
        # 投資金額entry
        self.entry_InvestAmount = Create_Entry( self, 3, 1, 'w', 1 )
        self.entry_InvestAmount.insert( 0, '10000' )
        # 投資金額單位label
        Create_Label( self, 'NTD', 3, 2, 'w', 1 )

        # 投資頻率label
        Create_Label( self, '投資頻率 : ', 4, 0, 'w', 1 )
        # 投資頻率entry
        self.entry_InvestFreq = Create_Entry( self, 4, 1, 'w', 1 )
        self.entry_InvestFreq.insert( 0, '1' )
        # 投資頻率單位label
        Create_Label( self, '月 / 次', 4, 2, 'w', 1 )
        
        # 開始計算按鈕
        self.button_StartCalc = Create_Button( self, '開始計算', self.Thread_Calc_InputParam, 5, 5, 'w', 1 )
        
        # 進度條
        self.Progressbar = Create_Progressbar( self, "indeterminate", 6, 5, 'w', 1 )

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

class cST_SysInvest_Result( cTab ):
    def __init__( self, MainWindow : MainWindow,  NBGroup : ttk.Notebook, TabName ):
        super().__init__( MainWindow, NBGroup, TabName )

        # 結算日期標題
        Create_Label( self, '結算日期 : ', 0, 0, 'w', 1 )
        # 結算日期結果
        self.EndDate = Create_LabelVar( self, 0, 1, 'w', 1, 'Str' )

        # 損益金額
        Create_Label( self, '損益金額 : ', 1, 0, 'w', 1 )
        self.PLAmount = Create_LabelVar( self, 1, 1, 'w', 1, 'Str' )

        # 損益比例
        Create_Label( self, '損益比例 : ', 2, 0, 'w', 1 )
        self.PLRatio = Create_LabelVar( self, 2, 1, 'w', 1, 'Double' )

        # 最高虧損比例
        Create_Label( self, '最高虧損比例 : ', 3, 0, 'w', 1 )
        # 日期
        self.MaxLossRatioDate = Create_LabelVar( self, 3, 1, 'w', 1, 'Str' )
        self.MaxLossRatioDate.set( '---/--/--' )
        # 比例
        self.MaxLossRatio = Create_LabelVar( self, 3, 2, 'w', 1, 'Double' )
 
        # 最高損益金額
        Create_Label( self, '最高虧損金額 : ', 4, 0, 'w', 1 )
        # 日期
        self.MaxLossDate = Create_LabelVar( self, 4, 1, 'w', 1, 'Str' )
        self.MaxLossDate.set( '---/--/--' )
        # 比例
        self.MaxLoss = Create_LabelVar( self, 4, 2, 'w', 1, 'Int' )

        # 輸出excel button
        Create_Button( self, '輸出excel', self.ExportLog, 5, 3, 'w', 1 )

        # 交易紀錄ListBox
        self.List_Log = Create_ListBox( self, 80, 6, 0, 'w', 10 )
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

class cST_SysInvest_Picture( cTab ):
    def __init__( self, MainWindow : MainWindow,  NBGroup : ttk.Notebook, TabName ):
        super().__init__( MainWindow, NBGroup, TabName )

        Create_Button( self, '視窗內畫圖', self.PlotDiagramInTk , 0, 0, 'w', 1 )
        Create_Button( self, '新視窗畫圖', self.PlotNewWindow , 0, 1, 'w', 1 )

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
