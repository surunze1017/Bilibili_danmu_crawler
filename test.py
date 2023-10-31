import argparse
import datetime
import os
import pymongo


def test(*args, **aa):
    print(args)
    print(aa)


def mongo(dic):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Bilibili-Danmu"]
    dblist = myclient.list_database_names()
    mycol = mydb.create_collection("bvid")
    print(dblist)

if __name__ == '__main__':
    # test(*[1,2,3])
    # test(1, 2, 3)

    # dict = {
    #     "b": 2,
    #     "c": 3
    # }

    # test(1, 2, 3, a=1, **dict)

    # parser = argparse.ArgumentParser(description="test of argparse")
    # parser.add_argument("--range", nargs="*", type=str, help="help of range")
    # parser.add_argument("-a", help="aaa", required=False)

    # args = parser.parse_args()
    # print(args)
    # ctime = "2022-01-21 21:11:18"
    # print(ctime[:10])
    # print(ctime[:10] == "2022-01-21")

    # print(datetime.date.today().strftime("%Y-%m-%d"))

    # os.chdir("pyspider/project/Bilibili/")
    # if not os.path.exists("./reult"):
    #     os.mkdir("./result")
    
    mongo(dic)
