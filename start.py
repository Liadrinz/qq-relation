import os
from config import config, update

config['me'] = input('请输入QQ: ')
update(config)
if len(os.sys.argv) > 1 and os.sys.argv[1] == 'sh':
    os.system('.\start.sh')
else:
    os.system('.\start.bat')
