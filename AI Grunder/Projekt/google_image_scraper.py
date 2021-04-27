from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

search = input('Sökord: ')
number = int(input('Antal bilder: '))

driver = webdriver.Chrome('C:\Development\chromedriver.exe')
driver.get('https://www.google.com/')

driver.find_element_by_xpath('//*[@id="zV9nZe"]/div').click()
box = driver.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
box.send_keys(search)
box.send_keys(Keys.ENTER)
driver.find_element_by_xpath('//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()

last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(2)
    new_height = driver.execute_script('return document.body.scrollHeight')
    try:
        driver.find_element_by_xpath(
            '//*[@id="islmp"]/div/div/div/div/div[4]/div[2]/input').click()
        time.sleep(2)
    except:
        pass
    if new_height == last_height:
        break
    last_height = new_height

for i in range(1, number):
    try:
        driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').screenshot(
            './images/'+search+'('+str(i)+').png')
    except:
        pass

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time

# driver = webdriver.Chrome('C:\Development\chromedriver.exe')
# driver.get('https://www.google.com/')

# driver.find_element_by_xpath('//*[@id="zV9nZe"]/div').click()
# box = driver.find_element_by_xpath(
#     '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
# box.send_keys('giraffe')
# box.send_keys(Keys.ENTER)

# driver.find_element_by_xpath('//*[@id="hdtb-msb-vis"]/div[2]/a').click()


# # Will keep scrolling down the webpage until it cannot scroll no more
# last_height = driver.execute_script('return document.body.scrollHeight')
# while True:
#     driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
#     time.sleep(2)
#     new_height = driver.execute_script('return document.body.scrollHeight')
#     try:
#         driver.find_element_by_xpath(
#             '//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
#         time.sleep(2)
#     except:
#         pass
#     if new_height == last_height:
#         break
#     last_height = new_height


# for i in range(1, 10):
#     try:
#         driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(
#             i)+']/a[1]/div[1]/img').screenshot('C:\Development\giraffe ('+str(i)+').png')
#     except:
#         pass
