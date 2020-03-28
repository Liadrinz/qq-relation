# QQ空间社交网络可视化

## 实现技术

Selenium + Pyecharts

## 使用

### 方法一

1. 安装Firefox浏览器和python3
1. 运行`pip install -r requirements.txt`
1. 运行`python start.py` (linux为`python start.py sh`)，输入QQ
1. 浏览器被自动启动，请在浏览器中登录到QQ空间
1. 爬虫开始，最小化即可
1. 爬虫结束后将在项目根目录生成可视化结果，并自动打开
1. 若自动打开可视化结果失败，请手动打开根目录下生成的`index.html`

### 方法二

1. 安装Firefox浏览器
1. 运行start.exe

## 配置

在`config.json`中可以配置:

- data_root: 数据存储的根路径
- data_path: 数据存储的子路径
- output: 可视化HTML文件生成路径

数据最终将存储到data_root + data_path下

## 可视化效果

- Echarts支持滚轮放大缩小，以及鼠标拖拽
- 鼠标指在节点上可以查看详细信息和相关节点
- 节点数量过多时需要迭代一定的时间才能形成稳定的社交网络图
![效果](https://github.com/Liadrinz/qq-relation/blob/master/demo.png)
