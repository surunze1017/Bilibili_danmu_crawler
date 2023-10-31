import csv
import re
import time
import os
import pymongo

from datetime import datetime, timedelta

from config import MONGO_URL, DATABASE_NAME


def get_bvid(bvid_raw: str) -> str:
    """从用户输入中获取视频的BVID号，如果输入的是链接，链接当中必须含有“bilibili”

    Args:
        bvid_raw (str): 用户输入的值，可以是视频完整链接或者含有bvid号的部分链接，也可以是bvid号

    Returns:
        str: 可以检索到bvid则返回bvid |
        None: 输入错误则返回None值
    """
    # 检测是否为链接形式
    if "bilibili" in bvid_raw:
        pattern = re.compile("com/video/(.{12})", re.S)
        bvid = re.findall(pattern, bvid_raw)[0]
        # print(bvid[:1])
    elif len(bvid_raw.strip()) == 12 and bvid_raw[:2].lower() == "bv":
        bvid = bvid_raw[:12]
        # print(bvid)
    else:
        # 输入错误，返回空值
        return ""
    return bvid


def create_date_list(start_date: str, end_date: str) -> list:
    """将输入的字符串格式的起始时间和结束时间转化为时间区间列表

    Args:
        start_date (str): 起始时间
        end_date (str): 结束时间

    Returns:
        list: 时间列表，以字符串形式存储
    """

    time_str_type = "%Y-%m-%d"
    start_date_datetime = datetime.strptime(start_date, time_str_type)
    end_date_datetime = datetime.strptime(end_date, time_str_type)

    interval = timedelta(days=1)
    tmp_time = start_date_datetime

    date_list = []

    while tmp_time <= end_date_datetime:
        tmp_time_str = tmp_time.strftime("%Y-%m-%d")
        date_list.append(tmp_time_str)
        tmp_time += interval
    # print(date_list)
    return date_list


def generate_dic(id, progress, content, ctime, weight) -> dict:
    output_dic = {
        "弹幕编号": id,
        "视频时间": progress,
        "弹幕内容": content,
        "弹幕发送日期": ctime,
        "权重": weight,
    }
    return output_dic


def time_format(progress_millis: int) -> str:
    """将毫秒制的时间转换为x时x分x妙的格式

    Args:
        progress_millis (int): 整型毫秒时间

    Returns:
        str: x时x分x妙
    """
    seconds = (progress_millis / 1000) % 60
    seconds = int(seconds)
    minutes = (progress_millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (progress_millis / (1000 * 60 * 60)) % 24
    hours = int(hours)
    lay = (
        progress_millis - hours * 1000 * 60 * 60 - minutes * 1000 * 60 - seconds * 1000
    )

    return f"{hours}时{minutes}分{seconds}秒{lay}"


def date_format(ctime_millis: int) -> str:
    """将毫秒制时间改为年-月-日 XX:XX:XX

    Args:
        ctime_millis (int): _description_

    Returns:
        str: _description_
    """
    tmp_time = time.localtime(ctime_millis)
    ctime_formatted = time.strftime("%Y-%m-%d %H:%M:%S", tmp_time)
    return ctime_formatted


def output(output_dic, filename, output_flag):
    # 创建result文件夹
    if not os.path.exists("./result"):
        os.mkdir("./result")

    def out_terminal():
        print(output_dic)

    def out_csv():
        if not os.path.exists(f"./result/{filename}.csv"):
            with open(
                f'./result/{filename}.csv', 'a', newline='', encoding='utf-8'
            ) as f:
                writer = csv.DictWriter(f, fieldnames=output_dic.keys())
                writer.writeheader()
                writer.writerow(output_dic)
        else:
            with open(
                f'./result/{filename}.csv', 'a', newline='', encoding='utf-8'
            ) as f:
                writer = csv.DictWriter(f, fieldnames=output_dic.keys())
                writer.writerow(output_dic)

    def out_mongo():
        myclient = pymongo.MongoClient(MONGO_URL)
        mydb = myclient[DATABASE_NAME]

        mycol = mydb[filename]

        mycol.insert_one(output_dic)

    format_dic = {0: out_terminal, 1: out_csv, 2: out_mongo}

    output_fun = format_dic.get(output_flag)
    output_fun()


if __name__ == "__main__":
    # create_date_list("2013-11-01", "2023-12-11")
    test_dic = {
        "弹幕编号": "id",
        "视频时间": "progress",
        "弹幕内容": "content",
        "弹幕发送日期": "ctime",
        "权重": "weight",
    }
    output(test_dic, "xxxxx", 2)
