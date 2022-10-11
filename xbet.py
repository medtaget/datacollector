import requests
import json


def underSearcher(match,score):
  headers = {
      'authority': 'tn.1xbet.com',
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6',
      'cache-control': 'no-cache',
      # Requests sorts cookies= alphabetically
      # 'cookie': 'che_r=104; pushfree_status=canceled; sh.session_be98639c=6df12127-1316-424e-91c6-5cb4a775e4c1; SESSION=00c0338bce3413331a4d6d02a96010bd; lng=fr; flaglng=fr; is_rtl=1; tzo=3; visit=1-3b94d279bdb6c639f49022cf4634d4eb; fast_coupon=true; v3fr=1; typeBetNames=full; coefview=0; auid=LYd5RWMYqsqvf73xA0PqAg==; completed_user_settings=true; _ga=GA1.2.363828188.1662560990; _gid=GA1.2.1640397653.1662560990; che_g=fb2f64c1-3d7a-1b16-8f8e-5e9c045a9865; right_side=right; dnb=1; _glhf=1662580358; ggru=174; _gat_gtag_UA_131019888_1=1',
      'pragma': 'no-cache',
      'referer': 'https://tn.1xbet.com/fr',
      'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
      'x-requested-with': 'XMLHttpRequest',
  }
  try:
   params = {
      'text': match,
      'limit': '50',
      'lng': 'fr',
      'mode': '4',
      'strict': 'True',
      'partner': '213',
  }
   #print("scraping link")
   response = requests.get('https://tn.1xbet.com/LiveFeed/Web_SearchZip', params=params, headers=headers).text
   data=json.loads(response)
   x=data["Value"][0]["ZP"]
  except:
    params = {
      'text': match,
      'limit': '50',
      'lng': 'fr',
      'mode': '4',
      'strict': 'false',
      'partner': '213',
  }
  
    response = requests.get('https://tn.1xbet.com/LiveFeed/Web_SearchZip', params=params, headers=headers).text
    data=json.loads(response)
    x=data["Value"][0]["ZP"]
    

  
    
    
  
  params = {
      'id': x,
      'lng': 'fr',
      'cfview': '0',
      'isSubGames': 'true',
      'GroupEvents': 'true',
      'allEventsGroupSubGames': 'true',
      'countevents': '500',
      'partner': '213',
      'marketType': '1',
      'isNewBuilder': 'true',
  }
  #print("scrape odds")
  response = requests.get('https://tn.1xbet.com/LiveFeed/GetGameZip', params=params, headers=headers).text
  cotas=json.loads(response)
  #pprint(cotas["Value"]['GE'])
  total={}
  for cota in cotas["Value"]['GE']:
    if cota["G"]==99:
      total=cota
      #pprint(total["E"][1])
  s=int(score.split(":")[0])+int(score.split(":")[1])+3.5
  for under in total["E"][1]:
    if 1.05<= under['C'] <= 1.2 and under['P']>s:
      #print(under['P'])
      #print(under['C'])
      return under['P'],under['C']
