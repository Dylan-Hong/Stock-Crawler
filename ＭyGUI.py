import tkinter as tk
import tkinter.ttk as ttk
import math

# 建立主視窗，並命名為window
window = tk.Tk()
window.title('Stock Paradise')
window.geometry('800x600')
window.configure(background='white')

# 建立Class，這個Class主要是分頁視窗的class


class Fun_Tab(tk.Frame):
    def __init__(self, Tab_Name, MainWindow):
        super().__init__(MainWindow)
        self.Tab_Name = Tab_Name
        MainWindow.add(self, text=Tab_Name)
        pass


# 建立分頁，需要獨立import tkinter模組中的Notebook功能、Frame功能
# 創建分頁主檔(它包在我們的主視窗window中，width、height用來調整長寬度)
tab_main = ttk.Notebook()
tab_main.place(relx=0.02, rely=0.02, relwidth=0.96,
               relheight=0.96, bordermode='outside')

# 寫一個所有分頁的類別，可以預設定義，並將共用函數寫在裡面
tab_1 = Fun_Tab('參數設定', tab_main)
tab_2 = Fun_Tab('定期定額投資', tab_main)
tab_3 = Fun_Tab('交易紀錄', tab_main)
tab_4 = Fun_Tab('損益圖表', tab_main)

Text = tk.Text(tab_1, width=100, height=37.5)
Text.place(x=0, y=0)


# 要視窗顯示，一定需要這一行
window.mainloop()
