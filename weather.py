import requests
from pymongo import MongoClient
from pyquery import PyQuery as pq
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Edge()

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s | %(lineno)d")
logger = logging.getLogger("one")

Client = MongoClient('mongodb://localhost:27017/')
db = Client['weather']
collection = db['pages_weather']


def add_delay():
    time.sleep(3)


def add_short_delay():
    time.sleep(1)


def get_weather():
    url = 'https://www.weather.com.cn/weather/101180406.shtml'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0"

    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            doc = pq(response.text)
            weather_week = doc("div#7d.c7d")
            days = weather_week("li.sky.skyid.lv3, li.sky.skyid.lv2, li.sky.skyid.lv1").items()
            for day in days:
                _day = day.find('h1').text()
                weather = day.find('[title].wea').text()
                tem = day.find('.tem').text()
                win = day.find('.win i').text()
                winds = day('.win em span').items()
                wind_ls = []
                for wind in winds:
                    win_dir, win_dir_e = wind.attr('title'), wind.attr('class')
                    wins = {
                        "win_dir": win_dir,
                        "win_dir_e": win_dir_e,
                    }
                    wind_ls.append(wins)
                datas = {
                        "day": _day,
                        "weather": weather,
                        "tem": tem,
                        "win": win,
                        "win_dir": wind_ls,
                    }
                collection.insert_one(datas)
                logger.info(f"保存完成:{_day}")
        else:
            logger.info("未响应")
    except Exception as e:
        logging.info(f"错误：{e}")

# 获取每天各个时段的天气
def get_weather_parts():
    url = "https://www.weather.com.cn/weather/101180406.shtml"
    try:
        driver.get(url)
        add_delay()
        # 查找近七天的节点
        class_name = "li.sky.skyid.lv3, li.sky.skyid.lv2, li.sky.skyid.lv1"
        search_boxs = driver.find_elements(By.CSS_SELECTOR, class_name)
        # 分别查找
        for box in search_boxs:
            box.click()
            add_short_delay()
            tems = driver.find_elements(By.CSS_SELECTOR, '.tem em')
            winfs = driver.find_elements(By.CSS_SELECTOR, '.winf em')
            win_levels = driver.find_elements(By.CSS_SELECTOR, '.winl em')
            hours = driver.find_elements(By.CSS_SELECTOR, '.time em')
            # 时段
            hour_parts_ls = []
            for hour in hours:
                part_time = hour.text
                hour_parts_ls.append(part_time)
            # 时段风向
            winf_hour_ls = []
            for winf in winfs:
                wins_hour_data = winf.text
                winf_hour_ls.append(wins_hour_data)
            # 时段温度
            tem_hour_ls = []
            for tem in tems:
                data_hour = tem.text
                tem_hour_ls.append(data_hour)
            # 时段风速
            winl_hour_ls = []
            for win_level in win_levels:
                win_level_data = win_level.text
                winl_hour_ls.append(win_level_data)

            day = box.find_element(By.CSS_SELECTOR, "h1").text

            day_weather = list(zip(hour_parts_ls, tem_hour_ls, winl_hour_ls, winf_hour_ls))
            # 数据打包
            tem_hour = {
                "day": day,
                "day_hour_weather": day_weather,
            }
            collection.insert_one(tem_hour)

            logger.info(f"时段天气保存完成{day}")
    except Exception as e:
        logger.error(f"错误：{e}")
    finally:
        driver.close()


if __name__ == "__main__":
    get_weather()
    get_weather_parts()
