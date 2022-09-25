from email.mime import image
import os
from re import template
from turtle import title
from moviepy.editor import *
from PIL import *
from PIL import ImageFont
from PIL import ImageDraw
import textwrap

def arrage(allList,maxlen):
    newList=[]
    for i in range(maxlen):
       for modelList in allList:
        try:
            newList.append(modelList.pop(0))
        except:
            pass
    return newList
    
def createTemps(noOfImg)->None:
    preImages=os.listdir("images")
    

    for i in range(noOfImg):
        downImg=Image.open(os.path.abspath("images/"+preImages[i%len(preImages)]))
        template=Image.open(os.path.abspath("shorts template.jpg"))

        downSize=downImg.size
        if(downSize[0]<downSize[1]):
            downImg=downImg.resize((int(downSize[0]*800/downSize[1]),800))
        elif(downSize[0]>downSize[1]):
            downImg=downImg.resize((800,int(downSize[1]*800/downSize[0])))
        downSize=downImg.size
        tempSize=template.size

        startX=int((tempSize[0]-downSize[0])/2)

        startY=int((tempSize[1]/2-downSize[1])/2-20)
        template.paste(downImg,(startX,startY))
        template.save("imagesTemp/"+str(i)+".jpg")

def addTexts(title,data)->None:
    tempImages=os.listdir("imagesTemp")
    keys=list(data.keys())[:9]
    for i in range(len(keys)): 
        templateTemp=Image.open(os.path.abspath("imagesTemp/"+str(i)+".jpg"))

        # Title setup
        titleFont = ImageFont.truetype(os.path.abspath("fonts/sans-serif/SansSerifBookFLF.otf"), 56)
        mobileNameFont = ImageFont.truetype(os.path.abspath("fonts/sans-serif/SansSerifBldFLF-Italic.otf"), 56)

        draw = ImageDraw.Draw(templateTemp)
        titleSize=titleFont.getsize(keys[i])
        imageSize=templateTemp.size
        titlePosition=(int((imageSize[0]-titleSize[0])/2),1080)
        draw.text(titlePosition,keys[i],(255,0,0),font=mobileNameFont)

        # model name update
        modelSize=titleFont.getsize(title)
        titlePosition=(int((imageSize[0]-modelSize[0])/2),0)
        draw.text(titlePosition,title,(255,0,0),font=mobileNameFont)

        # content setup
        y_text = 1150
        keyFont = ImageFont.truetype(os.path.abspath("fonts/sans-serif/SansSerifBldFLF-Italic.otf"), 40)
        valFont = ImageFont.truetype(os.path.abspath("fonts/sans-serif/SansSerifExbFLF.otf"), 40)

        for key,value in data.get(keys[i]).items():
            contentText=key+" : "+value+"\n"
            draw = ImageDraw.Draw(templateTemp)
            widthKey, heightKey = keyFont.getsize(key)



            lines = textwrap.wrap(value, width=35)
            widthValue, heightValue = valFont.getsize(value)
            draw.text((40, y_text), "->"+key+" : ",(31,206,203),font=keyFont)
            x_text=80
            if(widthKey+widthValue<1000):
                x_text=widthKey+100
            else:
                y_text += heightKey+10

            for line in lines:

                draw.text((x_text, y_text), line,(255,255,0),font=valFont)
                y_text += heightValue+10
            

        templateTemp.save(os.path.abspath("videoImg/"+str(i)+".jpg"))
        pass

    # for i in range(9):
    #     pass

def makeVideo(title,noOfSlides)->None:
    postClips=[]
    size = (1080,1920)
    tempImages=os.listdir("videoImg")
    for i in tempImages:
        absdir=os.path.abspath("videoImg/"+i)
        postClips.append(ImageClip(absdir).set_duration(int(59/noOfSlides)).resize(size))

    audioclip = AudioFileClip(os.path.abspath("music/backgroundmusicshort.mp3"))
    video_clip = concatenate_videoclips(postClips, method='compose')
    video_clip.audio=audioclip
    video_clip.write_videofile("output/"+title+".mp4", fps=24, remove_temp=True, codec="libx264", audio_codec="aac")

def run(title,data):
    if(title==""):
        data={
            "BODY":{
                "Dimenstions":"163.3 x 75.5 x 8.2 mm (6.43 x 2.97 x 0.32 in)",
                "Weight":"186 g (6.56 oz)",
                "Build":"Glass front (Gorilla Glass 5), plastic frame, plastic back",
                "Sim":"Dual SIM (Nano-SIM, dual stand-by)"
            },
            "DISPLAY":{
                "Type":	"Fluid AMOLED, 1B colors, 120Hz, HDR10+",
                "Size":	"6.7 inches, 108.0 cm2 (~87.6% screen-to-body ratio)",
                "Resolution":	"1080 x 2412 pixels, 20:9 ratio (~394 ppi density)",
                "Protection":	"Corning Gorilla Glass 5"
            },
            "MEMORY":{
                "card slot":"NO",
                "Internal":"128GB 8GB RAM, 256GB 8GB RAM, 256GB 12GB RAM UFS 3.1"
            },
            "MAIN CAMERA":{
                "Triple":	"50 MP, f/1.8, 24mm (wide), 1/1.56', 1.0µm, PDAF, OIS8 MP, f/2.2, 15mm, 120˚ (ultrawide), 1/4.0', 1.12µm 2 MP, f/2.4, (macro)",
                "Features":	"LED flash, HDR, panorama",
                "Video":	"4K@30fps, 1080p@30/60/120fps, gyro-EIS"
            },
            "SELFIE CAMERA":{
                "Single":	"16 MP, f/2.4, 26mm (wide), 1/3.09', 1.0µm",
                "Features":	"HDR",
                "Video":	"1080p@30fps, gyro-EIS"
            },
            "BATTERY":{
                "Type":	"Li-Po 5000 mAh, non-removable",
                "Charging":	"Fast charging 80W, 1-100% in 32 min"
            },
            "COMMS":{
                "WLAN":	"Wi-Fi 802.11 a/b/g/n/ac/6, dual-band, Wi-Fi Direct, hotspot",
                "Bluetooth":	"5.2, A2DP, LE",
                "GPS":	"Yes, with dual-band A-GPS, GLONASS, GALILEO, BDS",
                "NFC":	"Yes",
                "Radio":	"No",
                "USB":	"USB Type-C 2.0"
            },
            "FEATURES":{
                "Sensors":	"Fingerprint (under display, optical), accelerometer, gyro, proximity, compass, color spectrum"
            },
            "MISC":{
                "Colors":	"Sierra Black, Forest Green, Prime Blue",
                "Models":	"CPH2411",
                "Price":	"₹ 31,999"
            }
        }
        title="OnePlus 10R"
    createTemps(len(data.keys()))
    addTexts(title,data)
    makeVideo(title,len(data.keys()))
    pass

if __name__=="__main__":
    run("","")