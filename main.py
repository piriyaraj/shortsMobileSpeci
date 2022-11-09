from distutils.command.upload import upload
import json
import os

import composeVideo
import postScrapper
import extractUrl
import upload_video
import tools
url="https://gsmarena.com/allview_viva_1003g_lite-9909.php"

try:os.mkdir("imagesTemp")
except:pass
try:os.mkdir("videoImg")
except:pass
try:os.mkdir("images")
except:pass
try:os.mkdir("output")
except:pass
def deleteFlolderContent(folder):
    for i in os.listdir(folder):
        os.remove(folder+"/"+i)
    pass

def run():
    
    id,soup=extractUrl.getNextPostUrlForExtract()
    if(soup =="Too Many Requests"):
        print(soup)
        return soup
    title,dataDict=postScrapper.run(soup)
    composeVideo.run(title,dataDict)

    file=os.path.abspath("output/"+title+".mp4")
    description=str(tools.jsontotext(dataDict)+" for more details visit:https://bit.ly/mobilespeci ")
    category="22"
    keywords=", ".join(dataDict.keys())+", "+title
    privacyStatus="public"
    tempTitle=title
    title=title+" price, ram, rom, camera and battery specifications"
    # print(description)
    videoId=upload_video.run(file,title,description,category,keywords,privacyStatus)
    if(videoId==False):
        os.remove(file)
        return
    extractUrl.deletePostedUrlForExtract(id)
    tools.pushNoti(tempTitle,videoId)
    os.remove(file)
    deleteFlolderContent("videoImg")
    deleteFlolderContent("imagesTemp")
    deleteFlolderContent("images")




if __name__=="__main__":
    run()
    # upload_video.run("./cartAdd.mp4","Summer vacation in California","Had fun surfing in Santa Cruz","surfing,Santa Cruz","22","private")