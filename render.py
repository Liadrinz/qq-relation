import os

from build_graph import build_graph, signature, User
from pyecharts import options as opts
from pyecharts.charts.basic_charts.graph import Graph

from config import output

def get_nls(V, E, main=None):
    if main is not None:
        main = [signature(qq) for qq in main]
    nodes = []
    links = []
    for v in V:
        if main is not None and v.uuid in main:
            nv = User(value=v)
            nv.cate = 'me'
            nodes.append(nv.json())
        else:
            nodes.append(v.json())
    for e in E:
        links.append(e.json())
    rev_links = [{'source': l['target'], 'target': l['source']} for l in links]
    links += rev_links
    return nodes, links

# def render():
#     print('正在绘制可视化图形')
#     V, E = build_graph()
#     nodes, links = get_nls(V, E)
#     graph = Graph()
#     graph.add("", nodes, links, 
#         repulsion=500, 
#         label_opts=opts.LabelOpts(
#             is_show=False
#         ),
#         tooltip_opts=opts.TooltipOpts(is_show=False),
#         categories=[opts.GraphCategory(name='me', symbol_size=50), opts.GraphCategory(name='poster', symbol_size=35), opts.GraphCategory(name='liker', symbol_size=10)]
#     ).set_global_opts(title_opts=opts.TitleOpts(title="QQ空间好友关系图"))
#     graph.render(output)
#     print('绘制完成，准备打开{0}'.format(output))
#     os.system('start {0}'.format(output))
# 
# if __name__ == "__main__":
#     render()
