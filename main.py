import requests
import json
from xbet import underSearcher
import time
import schedule
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import cloudscraper
import fake_useragent
# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)

def signals():
  # Open the spreadsheet
  db=[]
  sheet = client.open("bettingscraper").sheet1
  dbold=sheet.get_all_records()
  print(dbold)
  ua = UserAgent()
  headers = {
      'authority': 'games.scoretrend.net',
      'accept': '*/*',
      'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6',
      'cache-control': 'no-cache',
      'origin': 'https://scoretrend.net',
      'pragma': 'no-cache',
      'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': str(ua.random),
  }
  #scraper = cloudscraper.create_scraper()
  #r = scraper.get("MY API").text
  response = requests.get('https://games.scoretrend.net/', headers=headers).text
  print("#######")
  print(response)
  print("#######")
  data= json.loads(response)
  for d in data[0]:
     #pprint(d)
   try:
     
     #d["goalInterceptor"] <= 150
     if (d['score']=='0:0' or d['score']=='1:0' or d['score']=='0:1' or d['score']=='2:0' or d['score']=='0:2'or d['score']=='2:1' or d['score']=='1:1' or d['score']=='1:2' ) and 50 <= d['timer']['tm'] <= 70:
      
        response=requests.get('https://api.scoretrend.net/event/'+d['eventid'],headers=headers).text
        event= json.loads(response)
        #pprint(event)
        print("########################")
        print("League: "+event["data"][1])
        print("Match: "+event["data"][2]+" VS "+event["data"][3])
        print("Score: "+d["score"])
        print("GT: "+str(d["goalInterceptor"]))
        print("time: "+str(d['timer']['tm'])+"'")
        try:
         under,odd= underSearcher(event["data"][2]+" "+event["data"][3],d['score'])
         print("under "+str(under)+" : "+str(odd))
        
         dict={
          "League":event["data"][1],
          "Home" :event["data"][2],
           "Away":event["data"][3],
          "Score":d["score"],
          "GT":str(d["goalInterceptor"]),
          "time":d['timer']['tm'],
          "Under":under,
          "Odd":odd
        }
         db.append(dict)
        except:
          print("odds not found")
        

         #print(link)
         #notifSignal15(event["data"][1],event["data"][2],event["data"][3],d["score"],d["goalInterceptor"],d['timer']['tm'],over15,link) 
               
   except:
      print("error")
      pass
   
  df = pd.DataFrame()
  dbold.extend(db)
  df = df.append(dbold, ignore_index=True) 
  dfi  = df.drop_duplicates(subset=["Home", "Away"], keep='first')
  sheet.update([dfi.columns.values.tolist()] +dfi.values.tolist())


# scheduling steps
schedule.every(30).seconds.do(signals)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
