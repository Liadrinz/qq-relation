# QQ空间社交网络可视化

## 实现技术

Selenium + Pyecharts

## 使用

### 方法一

1. 安装Firefox浏览器和python3
1. 安装GeckoDriver并添加环境变量
1. 运行`pip install -r requirements.txt`
1. 运行`python start.py` (linux为`python start.py sh`)，输入QQ
1. 浏览器被自动启动，请在浏览器中登录到QQ空间
1. 爬虫开始，最小化即可
1. 爬虫结束后将自动打开可视化结果
1. 若自动打开可视化结果失败，请手动访问`http://localhost:8000`(端口号在config.json中配置)

### 方法二

1. 安装Firefox浏览器
1. 安装GeckoDriver并添加环境变量
1. 运行start.exe，输入QQ
1. 做方法一的5-8步

## 配置

在`config.json`中可以配置:

- port: 可视化服务运行的端口
- encrypt: true/false, 是否加密QQ号
- me: 自身QQ号, 若不配置, 请务必通过命令行输入QQ号
- data_root: 数据存储的根路径
- data_path: 数据存储的子路径

数据最终将存储到data_root + data_path下

## 可视化效果

- Echarts支持滚轮放大缩小，以及鼠标拖拽
- 鼠标指在节点上可以查看详细信息和相关节点
- 节点数量过多时需要迭代一定的时间才能形成稳定的社交网络图
- **新功能**: 可按QQ号过滤查找若干好友，避免节点过多加载过久
![效果](https://github.com/Liadrinz/qq-relation/blob/master/demo.png)
