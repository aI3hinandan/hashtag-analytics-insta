from Initialization import *
from HashtagScraper import *
import pandas as pd

########################################################################################################################

def getRelatedTags(link, driver, hashData):
    driver.get(link)
    driver.implicitly_wait(5)
    relatedHashtagsElements = driver.find_elements_by_class_name('LFGs8.xil3i')
    hashName = driver.find_element_by_xpath('/html/body/div[1]/section/main/header/div[2]/div[1]/div[1]/h1').text
    hashPosts = 0

    hashLinks = []
    relatedHashtags = []
    for i in relatedHashtagsElements:
        hashLinks.append( i.get_attribute('href'))
    for link in hashLinks:
        hd = getHashtagTuple(link,driver)
        hashData['hashtag'].append(hd[0])
        hashData['no of posts'].append(hd[1])
    print(relatedHashtags, hashLinks, hashName, hashPosts)
    return relatedHashtags, hashLinks, hashName, hashPosts





########################################################################################################################
hashData = {
    'hashtag': [],
    'no of posts':[]
}
print("\nEnter Hashtag without Hash: ")
hashtag = input()
print("\nEnter No Of Related Hastags You want\n: ")
nofHashtags = int(input())
print("processing....")
driver = getFirefoxDriver()
relatedHashtags = []
inputLink = f'https://www.instagram.com/explore/tags/{hashtag}/'
hashOutput = getRelatedTags(inputLink, driver,hashData)
hashLinks = hashOutput[1]
if len(hashLinks) == 0:
    print("invalid hashtag. please rerun with another hashtag")
    exit()



relatedHashtags= relatedHashtags + hashOutput[0]

for link in hashLinks:
    hashOutput = getRelatedTags(inputLink, driver, hashData)
    if len(hashData['hashtag']) > nofHashtags: break
    hashLinks = hashLinks + hashOutput[1]

print(relatedHashtags)
path = r'D:\RelatedData.xlsx'
writer = pd.ExcelWriter(path)
fdf = pd.DataFrame(hashData)
fdf.to_excel(writer)
writer.save()




