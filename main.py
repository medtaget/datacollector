import requests
import json
#from pprint import pprint
import time
import schedule
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
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
  
     if 4800<=t and :
      try:
       
       print(l)
       print(match)
       print(s)
       print(round(t/60))
       print("##############")

  
       for dt in data["Value"]["GE"]:
        if dt['G']==8:
         for dc in dt['E']:
           
           if 1.03 <= dc['C'] <= 1.07 :
            print('trade found')
            if dc["T"]==4:
              b="1X"
            elif d["T"]==5:
              b="12"
            elif dc["T"]==6:
              b="X2"
            print(b)
            print(dc['c'])
            

            
            dict={
          "Date":datetime.now(),
          "League":l,
          "Home" :match.split(' vs ')[0],
           "Away":match.split(' vs ')[1] ,
          "Score":s,
          "Time":round(t/60),
          "DC":b,
          "Odd":dc['C']
            }
            db.append(dict)

             
      except Exception as e  :
        pass
  except Exception as e:
  
     pass

# updating sheet
 df = pd.DataFrame()
 dbold.extend(db)
 df = df.append(dbold, ignore_index=True) 
 dfi  = df.drop_duplicates(subset=["Home", "Away"], keep='first')
 sheet.update([dfi.columns.values.tolist()] +dfi.values.tolist())

schedule.every(15).seconds.do(signals)



if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1) 
      
