#coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import configparser
import sys
import os
import subprocess
#启动chrome的debug模式，C:\Program Files (x86)\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\tmp\autofile"


def checkHunter(pages,nums):
    hunter = True
    if pages == 1:
        jobstyle = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[' + str(nums) + ']/img'  # 猎头职位
    else:
        jobstyle = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li[' + str(nums) + ']/img'
    try:
        web.find_element_by_xpath(jobstyle)
        print('第 ' + str(nums) + ' 条数据是猎头职位 ')
    except:
        print('第 ' + str(nums) + ' 条数据不是猎头职位 ')
        hunter = False
    return hunter

def checkFlag(checkTitle,skipList):
    # checkTitleFlag = False
    for skipWrod in skipList:
        if skipWrod.upper() in checkTitle.upper():
            return True
            # checkTitleFlag = True
            # break
    return False

def recommendBosssStatus():
    # statusXpath = '//*[@id="wrap"]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/h2/span'  #打开新的tab页是使用这个，目前已经不支持打开新的tab页
    statusXpath = '//*[@id="wrap"]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/h2/span' #不打开新的tab
    try:
        statusText = web.find_element_by_xpath(statusXpath).text
    except NoSuchElementException:
        statusText = 'no status'
    print('boss活跃状态: ' + statusText)
    if statusText in bossStatusList:
        return True
    return False

def searchBossStatus():
    statusXpath = '//*[@id="main"]/div[3]/div/div[2]/div[1]/div[3]/h2/span'
    try:
        statusText = web.find_element_by_xpath(statusXpath).text
    except NoSuchElementException:
        statusText = 'no status'
    print('boss活跃状态 : ' + statusText)
    if statusText in bossStatusList:
        return True
    return False

def checkChatResultTitle():
    # countPath = '/html/body/div[8]/div[2]/div[1]/h3'
    countPath = '/html/body/div[11]/div[2]/div[2]/p'
    try:
        countText = web.find_element_by_xpath(countPath).text
    except NoSuchElementException:
        countText = '可以继续'
    print(countText)
    if '再试' in countText:
        return True
    return False

def checkLogStatus(web):
    resumeBtnPath = '//*[@id="header"]/div[1]/div[4]/ul/span/li/a'
    try:
        web.find_element_by_xpath(resumeBtnPath)
        print('已有登录状态')
    except NoSuchElementException:
        loginConfim = input('请先登录，登录完后输入Y:')
        if loginConfim.upper() == 'Y':
            print('已手动登录')
            time.sleep(5)
            return True
    return True

def searchJob(jobName,cludeHunter=False,pages=6):
    for i in range(1,pages):   #页数，建议1-6，前5页
        print('现在开始第' + str(i) + '页的查询')
        if i > 1:
            url_page =   base_url + '&query=' + jobName + '&page=' + str(i)
            web.get(url_page)
        else:
            # url_page = base_url + '&query=' + jobName
            # web.find_element_by_xpath('//*[@id="header"]/div[1]/div[2]/ul/ul[1]/li[1]/a').click()
            # time.sleep(5)
            web.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[1]/div[1]/div[1]/div/div[1]/input').clear()
            time.sleep(1)
            web.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[1]/div[1]/div[1]/div/div[1]/input').send_keys(jobName)
            time.sleep(2)
            web.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[1]/div[1]/div[1]/a').click()
        time.sleep(random.randint(8,10))
        for j in range(1,30): # 每页的数据，一页有30条，可以全部遍历。
            print('---------------------------------')
            print('现在开始第' + str(i) + '页第' + str(j) + '条数据')
            if j % 4 == 0:
                web.execute_script('window.scrollBy(0,500)')
                time.sleep(2)
            if i == 1:
                jobdiv = '1'
                try:
                    jobpath = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[' + jobdiv + ']/ul/li[' + str(
                        j) + ']/div[1]/a/div[1]/span[1]'
                    web.find_element_by_xpath(jobpath)
                except NoSuchElementException:
                    jobdiv = '2'
                jobpath = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[' + jobdiv + ']/ul/li[' + str(
                    j) + ']/div[1]/a/div[1]/span[1]'
                companypath = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[' + jobdiv + ']/ul/li[' + str(
                    j) + ']/div[1]/div/div[2]/h3/a'
                chatPath = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div['+ jobdiv +']/ul/li[' + str(j) + ']/div[1]/a/div[2]/a'
            else:
                jobpath = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li[' + str(j) + ']/div[1]/a/div[1]/span[1]'
                companypath = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li[' + str(j) + ']/div[1]/div/div[2]/h3/a'
                chatPath = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li[' + str(j) + ']/div[1]/a/div[2]/a'
            if cludeHunter:
                hunterFlag = False
            else:
                hunterFlag = checkHunter(i, j)
            ActionChains(web).move_to_element(web.find_element_by_xpath(jobpath)).perform()
            chatStat = web.find_element_by_xpath(chatPath).text
            print('沟通选项：' + chatStat)
            chatFlag = checkFlag(chatStat,['立即沟通'])
            # if chatFlag:
            #     print('未沟通')
            jobTitle = web.find_element_by_xpath(jobpath).text
            jobFlag = checkFlag(jobTitle,jobTitleKeyWords)
            if not jobFlag:
                print(jobTitle + ' 不符合，忽略')
            companyName = web.find_element_by_xpath(companypath).text
            companyFlag = checkFlag(companyName,skipCompays)
            if companyFlag:
                print(companyName + ' 需要忽略')
            if  not hunterFlag  and jobFlag and not companyFlag and chatFlag:
                print(companyName + ' 公司的 ' + jobTitle + ' 职位没有沟通过')
                web.find_element_by_xpath(jobpath).click()
                time.sleep(random.randint(1, 3))
                web.switch_to.window(web.window_handles[1])
                time.sleep(random.randint(2,4))
                # chatStatus = web.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[2]').text
                # print('沟通状态: ' + chatStatus)
                bossStatus = searchBossStatus()
                if bossStatus:
                    web.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[2]').click()
                    print('已发起沟通')
                    time.sleep(1)
                    chatResultTitle = checkChatResultTitle()
                    if chatResultTitle:
                        print('不能沟通，退出')
                        sys.exit(0)
                web.close()
                web.switch_to.window(web.window_handles[0])

def recommendJob(searchNum):
    for i in range(1,searchNum):
        print('-----------第' + str(i) + '条数据----------------')
        if i % 4 == 0:
            web.execute_script('window.scrollBy(0,700)')
            time.sleep(2)
        # if i % 16 == 0:
        #     web.execute_script('window.scrollBy(0,500)')
        #     time.sleep(2)
        jobPath = '//*[@id="wrap"]/div[2]/div[2]/div/div/div[1]/ul/li[' + str(i) + ']/div[1]/div/a'
        try:
            web.find_element_by_xpath(jobPath)
        except:
            web.execute_script('window.scrollBy(0,800)')
            time.sleep(2)
        jobTitle = web.find_element_by_xpath(jobPath).text
        print(jobTitle)
        jobFlag = checkFlag(jobTitle,jobTitleKeyWords)
        companyName = ''
        if jobFlag:
            web.find_element_by_xpath(jobPath).click()
            time.sleep(2)
            companypath = '//*[@id="wrap"]/div[2]/div[2]/div/div/div[1]/ul/li[' + str(i) + ']/div[2]/a/span'
            companyName = web.find_element_by_xpath(companypath).text
        else:
            print(jobTitle + '，职位不符合')
        companyFlag = checkFlag(companyName,skipCompays)
        if companyFlag:
            print(companyName + '需要忽略的公司')
        bossStatus = recommendBosssStatus()
        if not companyFlag and jobFlag and bossStatus:
            print(companyName + ' 公司的' + jobTitle + ' 职位可以继续')
            # herf = web.find_element_by_xpath(jobPath).get_attribute('href')
            # web.execute_script(f'window.open("{herf}","_blank");')
            # web.switch_to.window(web.window_handles[1])
            # time.sleep(5)
            # chatstatus = web.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[2]').text
            chatstatus = web.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/a[2]').text
            print('沟通状态: ' + chatstatus)
            if '立即沟通' in chatstatus:
                web.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/a[2]').click()
                print('没有沟通过，已发起沟通')
                time.sleep(2)
                web.find_element_by_xpath('/html/body/div[8]/div[2]/div[3]/a[1]').click()
                time.sleep(1)
                chatResultTitle = checkChatResultTitle()
                if chatResultTitle:
                    print('不能沟通，退出')
                    sys.exit(0)
            # web.close()
            # web.switch_to.window(web.window_handles[0])
            time.sleep(2)

def runJobRecommend(searchNum):
    url = 'https://www.zhipin.com/web/geek/job-recommend?city=101020100&salary=406'
    web.get(url)
    time.sleep(2)
    i = 3  #tab页是从3开始编号,每个订阅职位一个,每订阅一个+1
    # commandFlag = True
    while i < 6:
        jobtypePath = '//*[@id="wrap"]/div[2]/div[1]/div/div[1]/a[' + str(i) + ']/span'
        web.find_element_by_xpath(jobtypePath).click()
        time.sleep(2)
        recommendJob(searchNum)
        i += 1

#启动浏览器
def startChromeDebugger():
    chromeProcessCheckCmd = 'netstat -ano | findstr "9222" | findstr "LISTENING"'
    checkChromeResult = subprocess.getoutput(chromeProcessCheckCmd)
    # print(checkChromeResult)
    if not checkChromeResult:
        chromePath = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  #chrome安装目录
        tmpPath = r"D:\tmp\autofile"    #debugger模式，临时文件存放目录
        startChromCmd = chromePath + ' --disable-background-networking --remote-debugging-port=9222 --user-data-dir=' + tmpPath
        subprocess.Popen(startChromCmd)
        time.sleep(5)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    web = webdriver.Chrome(executable_path='D:\chrome\chromedriver.exe', chrome_options=options)   #chromedriver目录
    # web.get('https://www.zhipin.com/shanghai/?ka=header-home')
    # time.sleep(5)
    # logStatus = checkLogStatus(web)
    logStatus = True
    if not logStatus:
        sys.exit(1)
    return web

web = startChromeDebugger()
base_url = 'https://www.zhipin.com/web/geek/job?salary=406&city=101020100'
cf = configparser.ConfigParser()
cf.read('config.cfg',encoding='utf-8')
bossStatusList = cf['BOSS']['bossStatusList'].split(',')
skipCompays = cf['BOSS']['skipCompays'].split(',')
jobTitleKeyWords = cf['BOSS']['jobTitleKeyWords'].split(',')
# searchJobTitles = ['资深测试','自动化测试','测试专家','测试开发','软件测试','高级测试','中级测试','测试工程师']
searchJobTitles = cf['BOSS']['searchJobTitles'].split(',')   #需要搜索的职位名，遍历所有职位名，每页会有30条
hunterJob = False   #查询职位时,True 投递猎头职位，False 忽略猎头职位
pages = 6    # 查询职位时，查询最大页数，小于10
searchNum = 20  #推荐职位，查看最大条数
#&industry=100206' 互金 city=101020100 上海  salary=406 薪资20-50k

# web.get('https://www.zhipin.com/web/geek/chat?ka=header-message')
# time.sleep(3)
#执行页面查询及投递
# for jobName in searchJobTitles:
#     searchJob(jobName,hunterJob,pages)

#推荐职位  推荐职位会根据保存的求职期望职位，有几个期望职位会有几个tab页，遍历所有的期望职位
runJobRecommend(searchNum)
#
#回到主页
web.get('https://www.zhipin.com/shanghai/?ka=header-home')

