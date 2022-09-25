from firebase import firebase
import requests
from bs4 import BeautifulSoup

databaseUrl = "https://colabfacebook-default-rtdb.firebaseio.com/YouTube/mobilespeci/"
dataBase = firebase.FirebaseApplication(databaseUrl, None)

# for extract post data  ==================================================
def getLastPostNumberForExtract():
    postNumber = dataBase.get(databaseUrl, "data/lastPostNumberForExtract/")
    if(postNumber == None):
        postNumber = 0
    return postNumber
    pass

# set lastPostNumber


def setLastPostNumberForExtract(postNumber):
    insertData('data', {"lastPostNumberForExtract": postNumber},
               dataBase, format='patch')
    pass

# get next post url

def getNextPostUrlForExtract():
    postUrl = list(dataBase.get(databaseUrl, "toPost/"))[-1]
    no=postUrl.split("-")[1].split(".")[0]
    # print(postUrl)
    # id = list(dataBase.get(databaseUrl, "toPost/").keys())[-1]
    return no,postUrl
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
    dataDict={}
    for i in range(len(mobileLinks)):
        no=mobileLinks[i].split("-")[1].split(".")[0]
        dataDict[no]=mobileLinks[i]
    insertData('toPost', dataDict, dataBase, format='patch')

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
    insertData('data/lastPostInBrand/',{brand: mobileLinks[0]}, dataBase, format='patch')
    return mobileLinks

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
            postLinks=getAllMobilePosts(mobileBrand, mobileBrandUrl, lastPostInBrand)
            print("No of Total post : ",len(postLinks))
            updateToPost(postLinks)
            # print(len(postLinks))
            if(len(postLinks)>maxLen):
                maxLen=len(postLinks)
            insertData('data/crewelData',{mobileBrand: mobileCount}, dataBase, format='patch')
    # updateToPost(allPostLinks)

if __name__=="__main__":
    # id,url=getNextPostUrlForExtract()
    # print(id,url)
    # deletePostedUrlForExtract(id)
    # dataDict={
    #     '1':"a",
    #     '4':"c"
    # }
    print(getNextPostUrlForExtract())