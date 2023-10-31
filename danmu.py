import re
import requests

import dm_small_pb2 as dm
import google.protobuf.text_format as text_format

from prettytable import PrettyTable
from config import COOKIES, DANMU_URL, DANMU_URL_DATE, HEADERS, ORI_URL
from utils import (
    date_format,
    generate_dic,
    output,
    time_format,
    create_date_list,
)


class Danmu:
    def __init__(self, bvid: str, output_flag=0) -> None:
        """
        Args:
            bvid (str): bvid
            output_flag (int, optional): Decide the output format, 1 for CSV, 2 for MONGO. Defaults to 0.
        """
        self.bvid = bvid
        # self.date_list = date_list
        # self.danmu_count = 0
        self.info = {}
        # self.session = requests.session()
        self.output_flag = output_flag

    def get_video_info(self) -> None:
        """获取视频详细信息"""
        url = ORI_URL + self.bvid
        html = requests.get(url, headers=HEADERS)
        html.encoding = 'utf-8'
        aid_regx = f'"aid":(.*?),"bvid":"{self.bvid}"'
        cid_regx = '{"cid":(.*?),"page":1'
        pubdate_regx = ',"pubdate":(.*?),"'
        title_regx = ',"title":"(.*?)","'
        duration_regx = ',"duration":(.*?),"'
        views_regx = '"view":(.*?),"danmaku"'
        danmu_num_regx = '"danmaku":(.*?),"reply"'
        favorite_regx = '"favorite":(.*?),"coin"'
        likes_regx = '"like":(.*?),"dislike"'
        dislikes_regx = '"dislike":(.*?),"evaluation"'
        coin_regx = '"coin":(.*?),"share"'
        share_regx = '"share":(.*?),"now_rank'
        description_regx = '"desc":"(.*?)","desc_v2"'

        self.info["aid"] = re.findall(aid_regx, html.text)[0]
        self.info["cid"] = re.findall(cid_regx, html.text)[0]

        pubdate = re.findall(pubdate_regx, html.text)[0]
        self.info["pubdate"] = date_format(int(pubdate))

        self.info["title"] = re.findall(title_regx, html.text)[0]

        duration = re.findall(duration_regx, html.text)[0]
        self.info["duration"] = time_format(int(duration) * 1000)

        self.info["views"] = re.findall(views_regx, html.text)[0]
        self.info["danmu_num"] = re.findall(danmu_num_regx, html.text)[0]
        self.info["favorite"] = re.findall(favorite_regx, html.text)[0]
        self.info["likes"] = re.findall(likes_regx, html.text)[0]
        self.info["dislikes"] = re.findall(dislikes_regx, html.text)[0]
        self.info["coin"] = re.findall(coin_regx, html.text)[0]
        self.info["share"] = re.findall(share_regx, html.text)[0]
        self.info["description"] = re.findall(description_regx, html.text)[0]

    def print_video_info(self):
        table = PrettyTable()
        table.add_column("Title", [self.info["title"]])
        table.add_column("Pubdate", [self.info["pubdate"]])
        table.add_column("Views", [self.info["views"]])
        table.add_column("Danmu_Count", [self.info["danmu_num"]])
        table.add_column("Likes", [self.info["likes"]])
        table.add_column("Coins", [self.info["coin"]])
        table.add_column("Favorites", [self.info["favorite"]])
        table.add_column("Dislikes", [self.info["dislikes"]])
        table.add_column("Shares", [self.info["share"]])
        print(table)

    def get_danmu_proto_newest(self) -> None:
        """获取最新的弹幕, 不需要登录cookie"""
        # 用来更改弹幕segment的页数，若status code不为200，则break
        segment_number = 1

        # 获取的弹幕总数
        total_counts = 0

        while True:
            print(f"第{segment_number}页")
            url = DANMU_URL
            params = {
                'type': 1,  # 弹幕类型
                'oid': self.info["cid"],  # oid is cid
                'pid': self.info["aid"],  # pid is aid
                'segment_index': segment_number,  # 弹幕分段
                "web_location": 1315873,
                "w_rid": "267252d487b55bf3f6abea113715cb98",
                "wts": 169357660,
            }
            resp = requests.get(url, params, headers=HEADERS)
            if resp.status_code != 200:
                # print(f"检索完成，共{segment_number}页弹幕")
                break
            segment_number += 1
            danmu_proto = resp.content
            total_counts += self.proto2dict(danmu_proto)
        print(f"共解析{total_counts}条弹幕")

    def get_danmu_proto_by_date(self, start_date, end_date) -> None:
        """根据输入的日期范围来获取弹幕, 使用日期获取弹幕的接口不存在翻页选项, 可能b站觉得不需要?

        Args:
            start_date(str): 起始日期, 不得小于视频发布日期
            end_date(str): 结束日期, 不得大于today
        """

        # TODO 优化: 使用生成器来生成日期, 不形成一整个列表, 优化内存空间
        date_list = create_date_list(start_date, end_date)

        # 获取的弹幕总数
        total_counts = 0

        for date in date_list:
            print(date)
            url = DANMU_URL_DATE
            params = {
                'type': 1,  # 弹幕类型
                'oid': self.info["cid"],  # cid
                'date': date,
            }
            resp = requests.get(url, params, headers=HEADERS, cookies=COOKIES)

            danmu_proto = resp.content
            total_counts += self.proto2dict(danmu_proto, date=date)

        print(f"共解析{total_counts}条弹幕")

    def proto2dict(self, proto, date=None):
        """解析返回页面的弹幕

        Args:
            proto (resp.content): 返回页面的字节数据
            date: 选定的日期, 用以判断某条弹幕是否为用户输入的日期

        Returns:
            int: 返回该页弹幕总数
        """
        # 获取每页的弹幕量计数
        count = 0

        danmaku_seg = dm.DmSegMobileReply()  # type: ignore
        danmaku_seg.ParseFromString(proto)

        # 读取elem内的键值，对时间进行格式化操作后赋值给字典
        for elem in danmaku_seg.elems:
            # 弹幕发送的视频位置
            progress_formatted = time_format(elem.progress)
            # 弹幕发送的utc时间
            ctime_formatted = date_format(elem.ctime)

            if date is not None:
                if ctime_formatted[:10] != date:
                    break

            count += 1

            output_dic = generate_dic(
                elem.id, progress_formatted, elem.content, ctime_formatted, elem.weight
            )
            # print(json.dumps(output_dic, ensure_ascii=False))
            print(output_dic)
            # 文件写入
            output(output_dic, f"{self.bvid}_{self.info['title']}", self.output_flag)
        return count


if __name__ == "__main__":
    danmu = Danmu("BV1aW41187Qw")
    danmu.get_video_info()
    danmu.get_danmu_proto_by_date(start_date="2020-12-12", end_date="2020-12-12")
