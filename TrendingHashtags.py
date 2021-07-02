from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Initialization import *
from HashtagScraper import *
import pandas as pd
from varname import nameof

SheetName = ""

#INITIALIZATION
driver = getFirefoxDriver()
driver.get('http://instagram.com/explore/')
SCROLL_PAUSE_TIME = 5
EXPLORE_TABS_CSS_PATH = 'html.js.logged-in.client-root.js-focus-visible.sDN5V body div#react-root section._9eogI.E3X2T main.SCxLW.o64aR div.mJ2Qv._2Z_Zl.YrkqH div.K6yM_ div div.QzzMF.Igw0E.IwRSH.eGOV_._4EzTm div.pKKVh div.QzzMF.Igw0E.IwRSH.eGOV_._4EzTm.NUiEW'
#sfv
exploreThumbs = []
exploreLinks = []
hashtagsUnsorted = {}
hashtagLinks = []
WAIT_TIME = 2
driver.implicitly_wait(8)

#DEFINING DICTIONARIES
p20K = {'hashtag': [], 'Posts': []}
p50K = {'hashtag': [], 'Posts': []}
p100K = {'hashtag': [], 'Posts': []}
p500K = {'hashtag': [], 'Posts': []}
p1M = {'hashtag': [], 'Posts': []}
pM1M = {'hashtag': [], 'Posts': []}
dictList = [p20K,p50K,p100K,p500K,p1M,pM1M]

while (len(exploreThumbs)<=25):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME)
    exploreThumbs = [None]
    exploreThumbs =  driver.find_elements_by_css_selector(EXPLORE_TABS_CSS_PATH )

    newHeight = driver.execute_script("return document.body.scrollHeight")
    print('number of explore links: ' + str(len(exploreThumbs)))

#Get Links From Thumbs
for i in exploreThumbs:
    exploreLinks.append(i.find_element_by_tag_name('a').get_attribute('href'))
#Get Hashtags from Links
for link in exploreLinks:
    driver.get(link)
    elements = driver.find_elements_by_class_name('xil3i')
    for i in elements :
        hashtagLinks.append(i.get_attribute('href'))

frequencySet = []
frequencyDict = {'hashtag': [],'Posts': [], 'Times Used': []}
for link in hashtagLinks:
    hd = getHashtagTuple(link, driver)
    if hd[1] != 0:
        hashtagsUnsorted.update({hd[0]: hd[1]})
        frequencySet.append(hd)

#handing the frequency of hashtag use
for i in frequencySet:
    n = 0
    for j in frequencySet:
        if j[0] == i[0]:
            n += 1
    if n != 1:
        frequencyDict['hashtag'].append(i[0])
        frequencyDict['Posts'].append(i[1])
        frequencyDict['Times Used'].append(n)



#handling the hastags Dictionary
hashtags = {k: v for k, v in sorted(hashtagsUnsorted.items(), key=lambda item: item[1])}
for hashtag in hashtags:
    if hashtags[hashtag] > 5000 and hashtags[hashtag] <= 20000:
        p20K['hashtag'].append(hashtag)
        p20K['Posts'].append(hashtags[hashtag])
        continue
    if hashtags[hashtag] > 50000 and hashtags[hashtag] <= 100000:
        p50K['hashtag'].append(hashtag)
        p50K['Posts'].append(hashtags[hashtag])
        continue
    if hashtags[hashtag] > 100000 and hashtags[hashtag] <= 500000:
        p100K['hashtag'].append(hashtag)
        p100K['Posts'].append(hashtags[hashtag])
        continue
    if hashtags[hashtag] > 500000 and hashtags[hashtag] <= 1000000:
        p500K['hashtag'].append(hashtag)
        p500K['Posts'].append(hashtags[hashtag])
        continue
    if hashtags[hashtag] > 1000000:
        pM1M['hashtag'].append(hashtag)
        pM1M['Posts'].append(hashtags[hashtag])
        continue


path = r'D:\HashtagData.xlsx'
writer = pd.ExcelWriter(path)
sheetNo = 1
#add sheets for the hastags filtered by no of posts
if dictList != []:
    for i in dictList:
        print(i)
        df = pd.DataFrame(i)
        df.to_excel(writer, f"Sheet-{str(sheetNo)}")
        sheetNo += 1

#add sheet based on times used
fdf = pd.DataFrame(frequencyDict)
fdf.to_excel(writer,'Most Used Hashtags')

writer.save()














