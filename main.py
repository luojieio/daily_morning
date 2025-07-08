from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import sxtwl


# ------------------定义变量------------------

# 当前时间
today = datetime.now()

# 日期
start_date = {
  "photo":"09-01",
  "ceremory":"10-19",
  "love":"2018-01-21",
  "love_day":"01-21",
}

# 微信配置（使用环境变量）
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
template_id = os.environ["TEMPLATE_ID"]
user_id=["oxWV56ooCAoSKwx44Y1J1HPiPm80","oxWV56jh_osIxSaq5JMVVGRj_LO8"]


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

# 距离生日天数（10-01）
def get_birthday(birthday):
  next=datetime.strptime(birthday,"%Y-%m-%d")
  print(next)
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

# 计算累计天数
def get_count(start_date):
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

# 计算距离天数
def get_day_left(day):
  next = datetime.strptime(str(date.today().year) + "-" + day, "%Y-%m-%d")
  
  print(next)
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

# 发送微信消息
def call_wx():
  # 初始化微信客户端
  client = WeChatClient(app_id, app_secret)
  # 初始化微信消息实例
  wm = WeChatMessage(client)

  # 定义模板数据
  data = {
    "love_days":{"value":get_count(start_date.get('love'))},
    "love_days_left":{"value":get_day_left(start_date.get('love_day'))},
    "jie_birthday_left":{"value":get_birthday(get_solar('jie'))},
    "chen_birthday_left":{"value":get_birthday(get_solar('chen'))},
    "ceremony_days_left":{"value":get_day_left(start_date.get('ceremory'))},
    "photo_days_left":{"value":get_day_left(start_date.get('photo'))},
  }

  # 发送模板消息
  for j in user_id:
    res = wm.send_template(j, template_id, data)
    print(data)
    print(res)


# 主程序
if __name__ == "__main__":
  call_wx()