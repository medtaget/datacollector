import requests
import json
#from pprint import pprint
import time
import schedule
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from telegram import notifMsg
# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)

#score=['0:0','0:1','1:0','1:1','1:2','2:1','2:0','0:2']

def signals ():

# Open the spreadsheet
 db=[]
 sheet = client.open("bettingscraper").sheet1
 dbold=sheet.get_all_records()
 print(dbold)
  
 params={
        "sports": 1,
        "country": 1,
        "lng":'en',
        "count": 10000,
        "getEmpty":"true",
        
      
    }

 headers={
        "Accept": "*/*",
        "DNT": "1",
        "Referer": "https://1xbet.com/fr/live/Football/",
        "Sec-Fetch-Mode": "cors",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"


    }
 response =   requests.get("https://1xbet.com/LiveFeed/Get1x2_Zip", headers=headers,params=params).text

 data = json.loads(response)

 #pprint((data["Value"]))

 for dt in data["Value"]:
  #pprint(dt) 
  try:
  
    
     params = {
      'id': dt["ZP"],
      'lng': 'en',
      'cfview': '0',
      'isSubGames': 'true',
      'GroupEvents': 'true',
      'allEventsGroupSubGames': 'true',
      'countevents': '500',
      'partner': '213',
      'marketType': '1',
      'isNewBuilder': 'true',
   }

     response = requests.get("https://1xbet.com/LiveFeed/GetGameZip", headers=headers,params=params).text
#
     data = json.loads(response)
     g=dt['SC']['FS']
     if ('S1' in g.keys()):
      s1=g['S1']
     else:
      s1='0'
     if ('S2' in g.keys()):
      s2=g['S2']
     else:
      s2='0'
     s=str(s1)+':'+str(s2)
     t=dt['SC']["TS"]
     l=dt['LE']
     match=dt["O1"]+' vs '+dt["O2"]
  
     if 5100<=t :
      try:
       
       print(l)
       print(match)
       print(s)
       print(round(t/60))
       print("##############")

  
       for dt in data["Value"]["GE"]:
        if dt['G']==8:
         for dc in dt['E']:
           
           if 1.03 <= dc[0]['C'] <= 1.07 :
            print('trade found')
            if dc[0]["T"]==4:
              b="1X"
            elif dc[0]["T"]==5:
              b="12"
              break
            elif dc[0]["T"]==6:
              b="X2"
            print(b)
            print(dc[0]['C'])
            

            
            dict={
          "League":l,
          "Home" :match.split(' vs ')[0],
           "Away":match.split(' vs ')[1] ,
          "Score":s,
          "Time":round(t/60),
          "DC":b,
          "Odd":dc[0]['C']
            }
            db.append(dict)

             
      except Exception as e  :
        print(e)
        pass
  except Exception as e:
     print(e)
     pass

# updating sheet
 dfold = pd.DataFrame()
 dfold = dfold.append(dbold,ignore_index=True)
 df = pd.DataFrame()
 dbold.extend(db)
 df = df.append(dbold, ignore_index=True) 
 dfi  = df.drop_duplicates(subset=["Home", "Away"], keep='first')
 newdf=pd.concat([dfold,dfi]).drop_duplicates(keep=False)
 msg=newdf.to_dict('records')
 for m in msg:
  notifMsg(m)
  
 sheet.update([dfi.columns.values.tolist()] +dfi.values.tolist())

schedule.every(15).seconds.do(signals)



if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1) 
      
