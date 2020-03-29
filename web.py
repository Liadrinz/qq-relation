import json
import webbrowser
from time import sleep
from threading import Thread
from flask import Flask, request, render_template
from build_graph import build_graph, filter_graph, make_index
from render import get_nls
from config import server_port
from urllib.request import urlopen

app = Flask(__name__)
V, E = build_graph()
indices = make_index(V, E)

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/graph')
def graph():
    global V, E, indices
    qqs = request.args.get('qqs', None)
    nV, nE = V, E
    if qqs is not None:
        qqs = [str(q) for q in json.loads(qqs)]
        nV, nE = filter_graph(V, E, indices, qqs=qqs)
    nodes, links = get_nls(nV, nE, main=qqs)
    return render_template("graph.html", data={'V': nodes, 'E': links})

def open_browser():
    url = 'http://localhost:' + server_port
    while True:
        try:
            urlopen(url)
            break
        except Exception as e:
            sleep(0.5)
    webbrowser.open(url)

if __name__ == '__main__':
    print("正在启动服务器, 端口:{0}...".format(server_port))
    Thread(target=open_browser).start()
    app.run(host='127.0.0.1', port=server_port, debug=True)
    
