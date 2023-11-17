# 主要目的: 
## -- 学习selenium功能
# 主要功能：
## -- 在BOSS上，主动发起沟通，可以搜索职位后发起沟通，或者是根据推荐职位发起沟通
# 使用方法：
## -- 根据注释，修改文件中一些参数
## -- 电脑需安装chrome及chromedriver，python及selenium库
# 使用步骤
1. chrome debug模式，如chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\tmp\autofile"
2. 登录
3. 修改脚本中的参数，
   -- 如果是搜索职位，执行方法 searchJob(jobTitle,hunterJob,pages)
   -- 如果是执行推荐职位，执行方法 runJobRecommend(searchNum)
4. 执行脚本

