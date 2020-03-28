import json

with open('./config.json', 'rb') as f:
    config = json.loads(f.read().decode('utf-8'))
for key in config:
    exec('{0} = "{1}"'.format(key, config[key]))
def update(conf):
    with open('./config.json', 'wb') as f:
        f.write(json.dumps(conf, ensure_ascii=False).encode('utf-8'))
