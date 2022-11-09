import configparser
import telepot


config = configparser.ConfigParser()
config.read("config.ini")

bot_token = str(config["Telegram"]["bot_token"])
channel_id = str(config["Telegram"]["channel_id"])
bot = telepot.Bot(bot_token)



def notifMsg(d):
  msg=d["League"]+"\n"+d["Home"]+' vs '+d["Away"]+"\n"+d["Score"]+"\n"+str(d["Time"])+"'"+"\n"+str(d["DC"])+" || "+str(d["Odd"])
  bot.sendMessage(channel_id, msg )
