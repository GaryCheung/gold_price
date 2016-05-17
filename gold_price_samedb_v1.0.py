from bs4 import BeautifulSoup
import requests
import pymysql
import time

# 格式化成2016-03-20 11:45:39形式
present_time =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(present_time)

url = ['http://gold.hexun.com/hjxh/']

def get_gold_price(url):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')
    #print(soup)
    price = soup.select('table.nsc04 > tbody > tr:nth-of-type(6) > td:nth-of-type(4)')
    gold_price = []
    for prices in price:
        gold_price.append(prices.get_text())
    return gold_price

config = {
    'host':'127.0.0.1',
    'port':8889,
    'user':'root',
    'password':'root',
    'db':'gold_price',
    'charset':'gb2312',
    'unix_socket':'/Applications/MAMP/tmp/mysql/mysql.sock'
}

def mysql_insert(source,price):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = 'INSERT INTO gold_price (date, price, source) VALUES (%s, %s, %s)'
            cursor.execute(sql, (present_time, price, source))
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()

print('Execute on---------',present_time)
source = ['hexun']
price = get_gold_price(url[0])
#print(price)
mysql_insert(source[0],price)