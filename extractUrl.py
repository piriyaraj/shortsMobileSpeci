
from firebase import firebase
import requests
from bs4 import BeautifulSoup
databaseUrl = "https://colabfacebook-default-rtdb.firebaseio.com/YouTube/mobilespeci/"
dataBase = firebase.FirebaseApplication(databaseUrl, None)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
# for extract post data  ==================================================
def getLastPostNumberForExtract():
    postNumber = dataBase.get(databaseUrl, "data/lastPostNumberForExtract/")
    if(postNumber == None):
        postNumber = 0
    return postNumber
    pass

# set lastPostNumber
def isPublished(url):
    reqs = requests.get(url, headers=headers)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    table=soup.find("div",id="specs-list")
    if(str(soup.title).find("Too Many")>0):
        return "Too Many Requests"
    print(soup.title.text,end=" :")
    if(table.text.find("soon")<0):
        print("released")
        return soup
    else:
        print("Not released")
        return False
    pass

def setLastPostNumberForExtract(postNumber):
    insertData('data', {"lastPostNumberForExtract": postNumber},
               dataBase, format='patch')
    pass

# get next post url

def getNextPostUrlForExtract():
    postUrl = list(dataBase.get(databaseUrl, "toPost/"))
    postUrl.reverse()
    for i in postUrl:
        if(i==None):
            continue
        result=isPublished(i)
        if(result == "Too Many Requests"):
            return 0,result
        if(result!=False):
            no=i.split("-")[1].split(".")[0]
            return no,result
        else:
            dataDictReleased = {}
            dataDictReleased[no] = postUrl
            dataBase.delete(databaseUrl, 'toPost/'+no)
            insertData('announced', dataDictReleased, dataBase, format='patch')
    
    # print(postUrl)
    # id = list(dataBase.get(databaseUrl, "toPost/").keys())[-1]
    # return no,postUrl
    pass

# detete posted url


def deletePostedUrlForExtract(id):
    dataBase.delete(databaseUrl, 'toPost/'+id)
    pass

# added posted url in posted list


def addPostedUrlForExtract(postNumber, url):
    insertData('postedInFirebase', {postNumber: url}, dataBase, format='patch')

    pass


def insertData(tableName, data, dataBase, format="post"):
    if(format == "patch"):
        result = dataBase.patch(tableName, data)
    else:
        result = dataBase.post(tableName, data)


def readFirebaseDate(tableName):
    dataValueList = []
    ResultSet = dataBase.get(databaseUrl, tableName,)
    try:
        for i in (list(ResultSet.values())):
            dataValueList.append(i['url'])
        return dataValueList
    except:
        return 0


def arrageList(allList,maxlen):
    newList=[]
    for i in range(maxlen):
       for modelList in allList:
        try:
            newList.append(modelList.pop(0))
        except:
            pass
    return newList

# update toPost data
def updateToPost(mobileLinks):
    dataDictReleased = {}
    dataDictAnnounced = {}
    for i in range(len(mobileLinks)):
        # print(mobileLinks[i])
        no = mobileLinks[i].split("-")[1].split(".")[0]
        if (isPublished(mobileLinks[i])==False):
            dataDictAnnounced[no] = mobileLinks[i]
        else:
            dataDictReleased[no] = mobileLinks[i]
    insertData('toPost', dataDictReleased, dataBase, format='patch')
    insertData('announced', dataDictAnnounced, dataBase, format='patch')

def getAllMobilePosts(brand, url, lastPostUrl):
    # print(url)
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    try:
        nextPages = soup.find_all("div", class_="nav-pages")[0].find_all("a")
    except:
        nextPages=[]
    # print(soup.find_all("div", class_="nav-pages"))
    pageLinks = []
    mobileNames = []
    mobileLinks = []
    pageLinks.append(url)
    for i in nextPages:
        pageLink = "https://gsmarena.com/"+i.get_attribute_list("href")[0]
        pageLinks.append(pageLink)

    for i in pageLinks:
        reqs = requests.get(i)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        mobileList = soup.find_all("div", class_="makers")[0]
        mobileListLis = mobileList.find_all("li")
        for i in mobileListLis:
            mobileName = i.text
            postUrl = "https://gsmarena.com/" + i.find("a").get_attribute_list("href")[0]
            if(postUrl == lastPostUrl):
                return mobileNames, mobileLinks
            mobileNames.append(mobileName)
            mobileLinks.append(postUrl)
    
    return mobileNames, mobileLinks

# checking any new post availble using mobile count
def checkForNewPost():
    reqs = requests.get("https://www.gsmarena.com/makers.php3")
    soup = BeautifulSoup(reqs.text, 'html.parser')
    try:
        mobileList = soup.find_all("table")[0]
    except:
        print("too many request")
        return
    mobileListTds = mobileList.find_all("td")
    allPostLinks=[]
    maxLen=0
    for i in mobileListTds:
        mobileCount = i.find("span").text.split(" ")[0]
        mobileBrand = i.find("a").text.split(mobileCount)[0].replace(".", " ")
        # print(i.find("a").get_attribute_list("href"))
        mobileBrandUrl = "https://www.gsmarena.com/" + i.find("a").get_attribute_list("href")[0]
        try:
            noOfPost = dataBase.get(databaseUrl, "data/crewelData/"+mobileBrand).split("|")[0]
        except:
            noOfPost = 0
        if(noOfPost != mobileCount):
            print("new post availabe for", mobileBrand,end=" >> ")
            try:
                lastPostInBrand = dataBase.get(
                    databaseUrl, "data/lastPostInBrand/"+mobileBrand)
            except:
                lastPostInBrand = ""
            mobileNames,postLinks=getAllMobilePosts(mobileBrand, mobileBrandUrl, lastPostInBrand)
            print("No of Total post : ",len(postLinks))
            # print(postLinks)
            # return
            updateToPost(postLinks)
            if(len(postLinks)>0):
               insertData('data/lastPostInBrand/',{mobileBrand: postLinks[0]}, dataBase, format='patch')

            # print(len(postLinks))
            if(len(postLinks)>maxLen):
                maxLen=len(postLinks)
            insertData('data/crewelData',{mobileBrand: mobileCount}, dataBase, format='patch')
            return
    # updateToPost(allPostLinks)

# check urls from firebase wether they are released or not
def getRelasedUrlFromFirebase():
    mobileLinks = list(dataBase.get(databaseUrl, "announced/").values())
    dataDictReleased = {}
    for i in range(len(mobileLinks)):
        # print(mobileLinks[i])
        no = mobileLinks[i].split("-")[1].split(".")[0]
        if (isPublished(mobileLinks[i]) != False):
            dataDictReleased[no] = mobileLinks[i]
            dataBase.delete(databaseUrl, 'announced/'+no)
    insertData('toPost', dataDictReleased, dataBase, format='patch')
if __name__=="__main__":
    # id,url=getNextPostUrlForExtract()
    # print(id,url)
    # deletePostedUrlForExtract(id)
    # dataDict={
    #     '1':"a",
    #     '4':"c"
    # }
    urlNotPublished = "https://www.gsmarena.com/samsung_galaxy_a04e-11945.php"
    urlPublished = "https://www.gsmarena.com/samsung_galaxy_s22_ultra_5g-11251.php"
    url ="https://www.gsmarena.com/vivo_y77e_(t1)-11780.php"
    getRelasedUrlFromFirebase()
