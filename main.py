from distutils.command.upload import upload
import json
import os
from turtle import title
import composeVideo
import postScrapper
import extractUrl
import upload_video
url="https://gsmarena.com/allview_viva_1003g_lite-9909.php"

def run():
    extractUrl.checkForNewPost()
    id,url=extractUrl.getNextPostUrlForExtract()
    title,dataDict=postScrapper.run(url)
    composeVideo.run(title,dataDict)

    file=os.path.abspath("output/"+title+".mp4")
    description=json.dumps(dataDict,indent=4)+" for more details visit:https://bit.ly/mobilespeci "
    title=title+" price, ram, rom, camera and battery specifications"
    category="22"
    keywords=", ".join(dataDict.keys())+", "+title
    privacyStatus="public"

    upload_video.run(file,title,description,category,keywords,privacyStatus)
    extractUrl.deletePostedUrlForExtract(id)

if __name__=="__main__":
    run()
    # upload_video.run("./cartAdd.mp4","Summer vacation in California","Had fun surfing in Santa Cruz","surfing,Santa Cruz","22","private")