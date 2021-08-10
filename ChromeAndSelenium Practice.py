# 需要先pip selenium，並置chromedriver網站下載想對應的driver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# 下載相對應ChromeDriver版本後，放在/Users/local/bin資料夾中，並設定路徑
chromedriver = '/Users/local/bin/chromedriver'
# 啟動ChromeDriver
driver = webdriver.Chrome(chromedriver)
# 指定開啟的網址
driver.get('https://bsr.twse.com.tw/bshtm/')
driver.maximize_window()  # For maximizing window

# import一堆模組，主要是因為WebDriverWait用來確認結構完整載入、By應該是用來簡化尋找物間方法、
# EC則是用來排除特別狀況，比如確認frame是可用並轉換或確認物件是已經可以被按的狀態。
# 證交所每日買賣分點資料，裡面有兩個frame，分別為page1和page2，若沒有先指定他是哪一個frame，這些物件都找不到。
WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.NAME, "page1")))
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="TextBox_Stkno"]'))).send_keys("1216")
