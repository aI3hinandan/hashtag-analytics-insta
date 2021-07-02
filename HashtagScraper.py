def getHashtagTuple(link,driver):
    driver.get(link)
    try:
        hashtagName = str(driver.find_element_by_xpath('/html/body/div[1]/section/main/header/div[2]/div[1]/div[1]/h1').text)
    except:
        hashtagName = "Not Found"
    hashtagPosts = '0'
    try:
        hashtagPosts = driver.find_element_by_class_name('g47SY ').text
    except:
        print('not found')
    hashtagPosts = int(hashtagPosts.replace(',', ''))
    return (hashtagName,hashtagPosts)

