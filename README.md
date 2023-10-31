# 按日期爬取B站弹幕

可以按照日期爬取，也可以全部爬下来

## 按照日期爬取

填入用户cookie

## 存储到文件/数据库中

## 爬取地址

https://api.bilibili.com/x/v2/dm/wbi/web/seg.so?type=1&oid=250827076&pid=884069371&segment_index=2

cookie，按日期爬取需要
SESSDATA=c89ac743%2C1709102444%2Ca8e72%2A91dJftuTBfm2Lme90-S_HGII91vGgu6ywpvv8j1Pww4t3BcRCwgPyQB3NvsBzIUyxwDRKECAAAJwA;

## 流程

- 根据用户输入的类型，是全的网址还是只有`bvid`
- 根据`bvid`获取视频的简单信息：视频发布日期及视频是否分片
- 根据`bvid`获得`cid`及`aid`
- 用户输入是爬取最新弹幕还是所有弹幕或者是按照日期爬取
- 访问弹幕api，如果只爬取填入用户cookie
- 转存到数据库或者csv
- 数据分析