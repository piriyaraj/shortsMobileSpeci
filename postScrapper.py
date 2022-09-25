


import os
import requests
from bs4 import BeautifulSoup

def findimgurl(soup):
    imgUrls = []
    # firstImg = soup.find("div", class_="specs-photo-main").find("img").get_attribute_list("src")[0]
    # imgUrls.append(firstImg)
    try:
        imgclass = soup.find_all('div', class_="specs-photo-main")[0]
        a_tag = imgclass.find_all('a')[0]
        imglink = "https://www.gsmarena.com/" +a_tag.get_attribute_list('href')[0]
    except:
        imgclass = soup.find_all('div', class_="specs-photo-main")[0]
        imglink = imgclass.find_all('img')[0].get_attribute_list('src')[0]
    reqs = requests.get(imglink)
    soupImg = BeautifulSoup(reqs.text, 'html.parser')

    try:
        picclass = soupImg.findAll("div", id="pictures-list")[0]
        imgtags = picclass.findAll("img")
        for i in imgtags:
            if(i.get_attribute_list("border")[0]==None):
                continue
            img_url = i.get_attribute_list("src")[0]
            if(img_url == None):
                img_url = i.get_attribute_list("data-src")[0]
            imgUrls.append(img_url)
    except Exception as e:
        print(e)
        imgUrls.append(imglink)
    return imgUrls
    
def downloadImages(imgUrlList)->None:
    for i in os.listdir(os.path.abspath("images/")):
        os.remove(os.path.abspath("images/"+i))

    for i in range(len(imgUrlList)):
        reqs = requests.get(imgUrlList[i])
        try:
            soup = BeautifulSoup(reqs.text, 'html.parser')
            picclass=soup.findAll("div",id="pictures-list")[0]
            imgtag=picclass.findAll("img")[0]
            img_url=imgtag.get_attribute_list("src")[0]
            res=requests.get(img_url)
        except:
            res=reqs
        img_title=os.path.abspath("images/"+str(i)+".jpg")
        file = open(img_title,'wb')
        for chunk in res.iter_content(10000):
            file.write(chunk)
        file.close()

def maketable(soup):
    tables=soup.findAll("table")
    dataDict={}
    for i in tables:
        tempDict={}

        for j in i.findAll("tr"):
            if(i.findAll("tr").index(j)==0):
                try:
                    th=j.findAll('th')[0].text
                except:
                    th="PRICE"
            tds = j.findAll("td")
            try:
                key=tds[0].text
                value=tds[1].text.replace("\n","").split("/")
                listvalue=tds[1].text.replace("\n","")
                value.reverse()
                value=" ||".join(value)
                value=value.split(",")
                value.reverse()
                value=", ".join(value)
                value=value.split(":")
                value.reverse()
                value=" ||".join(value)
                tempDict[key]=value
            except:
                break


        dataDict[th]=tempDict
        
    return dataDict


def run(link):
    # link="https://www.gsmarena.com/oneplus_10_pro-11234.php"
    reqs = requests.get(link)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    downloadImages(findimgurl(soup))
    dataDict=maketable(soup)
    phoneName = soup.title.text.split(" -")[0]
    return phoneName,dataDict

if __name__=="__main__":
    link="https://www.gsmarena.com/oneplus_10_pro-11234.php"
    reqs = requests.get(link)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    downloadImages(findimgurl(soup))
    dataDict=maketable(soup)
