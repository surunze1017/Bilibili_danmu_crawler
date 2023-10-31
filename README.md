# B站视频弹幕爬虫

## 使用方法

### 安装项目依赖

- `pip install -r requirements.txt`

### 运行及帮助

- `python3 main.py -h`

```bash
python3 main.py -h

usage: main.py [-h] -i [BVID] [-o {csv,mongo}] [-n | -a | -d [DATE ...]]

Get Danmu info of a Bilibili video by BVID

options:
  -h, --help            show this help message and exit
  -i [BVID], --bvid [BVID]
                        BVID of an video, length 12
  -o {csv,mongo}, --output {csv,mongo}
                        Set the output format.Choose [csv] to get the CSV format result, [mongo] to put the result into Mongo DB. Result will only
                        be displayed in terminal by DEFAULT.
  -n, --newest          Get newest Danmu of the video
  -a, --all             Get all Danmu of the video. RANGE: [PUB_DATE, TODAY]
  -d [DATE ...], --date [DATE ...]
                        Get Danmu of the video by date range.
```

### 爬取

#### 爬取系统默认最新弹幕

- 示例:`python3 main.py -i BV1aW41187Qw -n`

#### 爬取视频发布以来的全部弹幕

- 示例: `python3 main.py -i BV1aW41187Qw -a`
- 爬取所有弹幕以及根据日期爬取需要填入个人登录后的cookie, 位置: `config.py SESSDATA`

#### 爬取视频发布以来指定日期范围内的全部弹幕

- 示例: `python3 main.py -i BV1aW41187Qw -d 2020-10-11 2020-10-22`
- 爬取所有弹幕以及根据日期爬取需要填入个人登录后的cookie, 位置: `config.py SESSDATA`

### 输出

- 提供三种输出模式:
  1. 命令行输出(默认)
  2. 输出到csv文件
  3. 输出到Mongo DB

#### 输出到csv文件

- 示例: `python3 main.py -i BV1aW41187Qw -d 2020-10-11 2020-10-22 -o csv`
- 默认存储在`项目/result`下

#### 输出到Mongo DB

- 示例: `python3 main.py -i BV1aW41187Qw -d 2020-10-11 2020-10-22 -o mongo`
- Mongo DB配置:
  - `config.py`中修改`MONGO_URL`参数