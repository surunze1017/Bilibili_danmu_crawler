import argparse
import datetime

from danmu import Danmu


def main():
    # 使用argparse获取命令行参数
    parser = argparse.ArgumentParser(
        description="Get Danmu info of a Bilibili video by BVID"
    )

    exclusive_group = parser.add_mutually_exclusive_group()

    parser.add_argument(
        "-i",
        "--bvid",
        nargs="?",
        type=str,
        required=True,
        help="BVID of an video, length 12",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        choices=["csv", "mongo"],
        help="Set the output format.Choose [csv] to get the CSV format result, [mongo] to put the result into Mongo DB. Result will only be displayed in terminal by DEFAULT.",
    )

    exclusive_group.add_argument(
        "-n", "--newest", action="store_true", help="Get newest Danmu of the video"
    )
    exclusive_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Get all Danmu of the video. RANGE: [PUB_DATE, TODAY]",
    )
    exclusive_group.add_argument(
        "-d", "--date", nargs="*", help="Get Danmu of the video by date range."
    )
    args = parser.parse_args()

    output_flag_dict = {
        "csv": 1,
        "mongo": 2,
    }

    output_flag = output_flag_dict[args.output]
    # print(f"bvid={args.bvid}; newest={args.newest}; all={args.all}; date={args.date}")

    danmu = Danmu(bvid=args.bvid, output_flag=output_flag)
    danmu.get_video_info()
    danmu.print_video_info()

    if args.newest:
        danmu.get_danmu_proto_newest()
    elif args.all:
        # 列表为全的
        danmu.get_danmu_proto_by_date(
            start_date=danmu.info["pubdate"][:10],
            end_date=datetime.date.today().strftime("%Y-%m-%d"),
        )
    elif len(args.date) == 2:
        # TODO 列表开始和结束日期的大小比较, 和pubdate的大小比较
        danmu.get_danmu_proto_by_date(start_date=args.date[0], end_date=args.date[1])


if __name__ == "__main__":
    main()
