import requests
import json
#from pprint import pprint
import time
import schedule
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)

score=['0:0','0:1','1:0','1:1','1:2','2:1','2:0','0:2']

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
  
     if 4200<=t:
      try:
       
       print(l)
       print(match)
       print(s)
       print(round(t/60))
       print("##############")

  
       for dt in data["Value"]["GE"]:
        if dt['G']==99:
         for under in dt['E'][1]:
           sc=int(s.split(":")[0])+int(s.split(":")[1])+2.5
           if 1.05<= under['C'] <= 1.8 and under['P']>sc:
            print('trade found')
            print(under['P'])
            print(under['C'])
            
            dict={
           "League":l,
          "Home" :match.split(' vs ')[0],
           "Away":match.split(' vs ')[1] ,
          "Score":s,
          "Time":round(t/60),
          "Under":under['P'],
          "Odd":under['C']
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
