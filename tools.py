import requests
def pushNoti(postTitle,id):
    if(id!=False):
        params={
            'k':"k-6e9372687b0b",
            't':'Mobilespeci Short',
            'c':postTitle +" posted on youtube",
            'u':"https://www.youtube.com/shorts/"+str(id)
        }
        # URL="http://xdroid.net/api/message?k=k-6e9372687b0b&t=Mobilespeci Short&c=from+HUAWEI+POT-LX1&u=http%3A%2F%2Fgoogle.com"
        result=requests.get(url='http://xdroid.net/api/message',params=params)
        print(result.json())

if __name__=="__main__":
    pushNoti("new video uploaded","Ax1k05AvJgk")