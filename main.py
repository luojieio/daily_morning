from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import sxtwl


today = datetime.now()

# ------------------定义变量------------------
# 日期
start_date = {
  "love":"2018-01-21",
  "love_day":"01-21",
}

# 城市
city = ['武汉', '广州', '绵阳', '乐昌']

breakfirst=["美式","鸡蛋","豆浆","酸奶","包子","纯牛奶","玉米","红薯","花卷","三明治","云吞"]
lunch=["正常吃"]
dinner=["玉米","鸡蛋","纤体瓶","贝果","黄瓜","鸡翅","豆腐汤","小番茄","虾","火龙果","饺子","香蕉","番茄","三明治","牛奶","骨架","包子"]


# 微信配置（使用环境变量）
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
# user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]
user_id=["oxWV56ooCAoSKwx44Y1J1HPiPm80"]


# ------------------定义函数------------------
# 获取农历（阴历）对应公历（阳历）时间
def get_solar(user):
  if user=="jie":
    day=sxtwl.fromLunar(date.today().year+1, 2, 19)
    birthday="{}-{}-{}".format(day.getSolarYear(),day.getSolarMonth(),day.getSolarDay())
    # print(birthday)
    return birthday
  else:
    day=sxtwl.fromLunar(date.today().year+1, 2, 14)
    birthday="{}-{}-{}".format(day.getSolarYear(),day.getSolarMonth(),day.getSolarDay())
    # print(birthday)
    return birthday

# 获取天气
def get_weather(city):
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

# 计算距离天数（2018-01-21）
def get_count(start_date):
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

# 距离生日天数（10-01）
def get_birthday(birthday):
  # next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  next=datetime.strptime(birthday,"%Y-%m-%d")
  print(next)
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_day_left(day):
  next = datetime.strptime(str(date.today().year) + "-" + day, "%Y-%m-%d")
  
  print(next)
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

# 获取随机一句
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

# 获取随机颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

# 发送微信消息
def call_wx():
  # 初始化微信客户端
  client = WeChatClient(app_id, app_secret)
  # 初始化微信消息实例
  wm = WeChatMessage(client)
  # 获取天气
  city_dir={}
  for i in city:
    i_weather,i_temp=get_weather(i)
    city_dir[i]={
      "weather":i_weather,
      "temperature":i_temp
    }
  
  # 定义模板数据
  data = {
  "wuhan_weather":{"value":city_dir.get('武汉').get('weather')},
  "wuhan_temperature":{"value":city_dir.get('武汉').get('temperature')},
  "guangzhou_weather":{"value":city_dir.get('广州').get('weather')},
  "guangzhou_temperature":{"value":city_dir.get('广州').get('temperature')},
  "mianYang_weather":{"value":city_dir.get('绵阳').get('weather')},
  "mianYang_temperature":{"value":city_dir.get('绵阳').get('temperature')},
  "leChang_weather":{"value":city_dir.get('乐昌').get('weather')},
  "leChang_temperature":{"value":city_dir.get('乐昌').get('temperature')},

  "breakfirst_menu":{"value":random.choice(breakfirst)},
  "lunch_menu":{"value":random.choice(lunch)},
  "dinner_menu":{"value":random.choice(dinner)},

  "love_days":{"value":get_count(start_date.get('love'))},
  "love_days_left":{"value":get_day_left(start_date.get('love_day'))},
  "jie_birthday_left":{"value":get_birthday(get_solar('jie'))},
  "chen_birthday_left":{"value":get_birthday(get_solar('chen'))},

  # "words":{"value":get_words(), "color":get_random_color()}
  }

  # 发送模板消息
  for j in user_id:
    res = wm.send_template(j, template_id, data)
    print(data)
    print(res)


# 主程序
if __name__ == "__main__":
  call_wx()