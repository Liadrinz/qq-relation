import os
from config import config, update

config['me'] = input('请输入QQ: ')
update(config)
os.system('.\start.bat')
