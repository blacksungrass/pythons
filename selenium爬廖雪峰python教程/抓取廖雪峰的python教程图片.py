from selenium import webdriver
from PIL import Image
import re
import time

def getPicture(driver,url,filename):
    assert filename[-4:]=='.png'
    driver.get(url)
    e = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div[2]/div[2]/div[2]/div[2]')
    left = e.location['x'] 
    top = e.location['y'] 
    elementWidth = e.location['x'] + e.size['width'] 
    elementHeight = e.location['y'] + e.size['height']
    e.screenshot(filename)
    time.sleep(1)
    im = Image.open(filename)
    im = im.crop((left,top,elementWidth,elementHeight))
    im.save(filename)
driver = webdriver.PhantomJS()
driver.maximize_window()
url = 'https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
basepath = 'C:\\Users\\hu\\Desktop\\lalala\\'
baseurl = 'https://www.liaoxuefeng.com'
driver.get(url)
e = driver.find_element_by_xpath('//*[@id="0014316089557264a6b348958f449949df42a6d3a2e542c000"]')
h = e.get_attribute('innerHTML')
r = re.findall(r'<a href="(.+)" class=".+">(.+)</a>',h)
count = 0
for u,t in r:
    t = t.replace('\\',' and ')
    t = t.replace('/',' and ')
    print(u,t)
    getPicture(driver,baseurl+u,basepath+'{:02}'.format(count)+t+'.png')
    #time.sleep(2)
    count += 1
//全部保存为图片格式以后用photoshop-》文件-》自动-》pdf演示文稿 就可以把这些图片汇总成pdf文档