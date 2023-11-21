from selenium import webdriver
import time
import random
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
    checkTitleFlag = False
    for skipWrod in skipList:
        if skipWrod.upper() in checkTitle.upper():
            checkTitleFlag = True
            break
    return checkTitleFlag

def searchJob(jobName,cludeHunter=False,pages=6):
    for i in range(1,pages):   #页数，建议1-6，前5页
        print('现在开始第' + str(i) + '页的查询')
        if i > 1:
            url_page =   base_url + '&query=' + jobName + '&page=' + str(i)
        else:
            url_page = base_url + '&query=' + jobName
        web.get(url_page)
        time.sleep(random.randint(2,4))
        for j in range(1,31): # 每页的数据，一页有30条，可以全部遍历。
            print('---------------------------------')
            print('现在开始第' + str(i) + '页第' + str(j) + '条数据')
            if j % 4 == 0:
                web.execute_script('window.scrollBy(0,500)')
            if i == 1:
                jobpath = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[' + str(j) + ']/div[1]/a/div[1]/span[1]'
                companypath = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[' + str(j) + ']/div[1]/div/div[2]/h3/a'
            else:
                jobpath = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li[' + str(j) + ']/div[1]/a/div[1]/span[1]'
                companypath = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li[' + str(j) + ']/div[1]/div/div[2]/h3/a'
            if cludeHunter:
                hunterFlag = False
            else:
                hunterFlag = checkHunter(i, j)
            jobTitle = web.find_element_by_xpath(jobpath).text
            jobFlag = checkFlag(jobTitle,jobTitleKeyWords)
            if not jobFlag:
                print(jobTitle + ' 不符合，忽略')
            companyName = web.find_element_by_xpath(companypath).text
            companyFlag = checkFlag(companyName,skipCompays)
            if companyFlag:
                print(companyName + ' 需要忽略')
            if  not hunterFlag  and jobFlag and not companyFlag:
                print(companyName + ' 公司的 ' + jobTitle + ' 职位可以继续')
                web.find_element_by_xpath(jobpath).click()
                web.switch_to.window(web.window_handles[1])
                time.sleep(random.randint(2,3))
                chatStatus = web.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[2]').text
                print('沟通状态' + chatStatus)
                if '立即沟通' in chatStatus:
                    web.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[2]').click()
                    print('没有沟通过，已发起沟通')
                    time.sleep(1)
                web.close()
                web.switch_to.window(web.window_handles[0])

def commandJob(typePath,searchNum):
    web.find_element_by_xpath(typePath).click()
    time.sleep(2)
    for i in range(1,searchNum):
        print('---------------------------')
        if i % 4 == 0:
            web.execute_script('window.scrollBy(0,700)')
            time.sleep(2)
        jobPath = '//*[@id="wrap"]/div[2]/div[2]/div/div/div[1]/ul/li[' + str(i) + ']/div[1]/div/a'
        jobTitle = web.find_element_by_xpath(jobPath).text
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
        if not companyFlag and jobFlag:
            print(companyName + ' 公司的' + jobTitle + ' 职位可以继续')
            herf = web.find_element_by_xpath(jobPath).get_attribute('href')
            web.execute_script(f'window.open("{herf}","_blank");')
            web.switch_to.window(web.window_handles[1])
            time.sleep(4)
            chatstatus = web.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[2]').text
            print('沟通状态 ' + chatstatus)
            if '立即沟通' in chatstatus:
                web.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[2]').click()
                print('没有沟通过，已发起沟通')
                time.sleep(1)
            web.close()
            web.switch_to.window(web.window_handles[0])
            time.sleep(2)

def runJobRecommend(searchNum):
    url = 'https://www.zhipin.com/web/geek/job-recommend?salary=406'
    web.get(url)
    time.sleep(2)
    i = 3  #tab页是从3开始编号
    commandFlag = True
    while commandFlag:
        jobtypePath = '//*[@id="wrap"]/div[2]/div[1]/div/div[1]/a[' + str(i) + ']/span'
        try:
            # web.find_element_by_xpath(jobtypePath)
            commandJob(jobtypePath, searchNum)
        except:
            commandFlag = False
        # if commandFlag:
        #     commandJob(jobtypePath,searchNum)
        i += 1

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
web = webdriver.Chrome(executable_path='D:\chrome\chromedriver.exe',chrome_options=options)

skipCompays = ['某','平安','得物']
jobTitleKeyWords = ['测试','TEST','QA']
# searchJobTitles = ['资深测试','自动化测试','测试专家','测试开发','软件测试','高级测试','中级测试','测试工程师']
searchJobTitles = ['自动化测试','测试开发']   #需要搜索的职位名，遍历所有职位名，每页会有30条
hunterJob = False   #查询职位时,True 投递猎头职位，False 忽略猎头职位
pages = 6    # 查询职位时，查询最大页数，小于10
searchNum = 40  #推荐职位，查看最大条数
base_url = 'https://www.zhipin.com/web/geek/job?salary=406&city=101020100'
#&industry=100206' 互金 city=101020100 上海  salary=406 薪资20-50k

#执行页面查询及投递
# for jobTitle in searchJobTitles:
#     searchJob(jobTitle,hunterJob,pages)

#推荐职位  推荐职位会根据保存的求职期望职位，有几个期望职位会有几个tab页，遍历所有的期望职位
runJobRecommend(searchNum)
#
#回到主页
web.get('https://www.zhipin.com/shanghai/?ka=header-home')