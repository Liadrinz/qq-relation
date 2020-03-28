import os

from build_graph import build_graph
from pyecharts import options as opts
from pyecharts.charts.basic_charts.graph import Graph

from config import output

def get_nls():
    V, E = build_graph()
    nodes = [v.json() for v in V]
    links = [e.json() for e in E]
    rev_links = [{'source': l['target'], 'target': l['source']} for l in links]
    links += rev_links
    return nodes, links

def render():
    print('正在绘制可视化图形')
    nodes, links = get_nls()
    graph = Graph()
    graph.add("", nodes, links, 
        repulsion=500, 
        label_opts=opts.LabelOpts(
            is_show=False
        ),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        categories=[opts.GraphCategory(name='me', symbol_size=50), opts.GraphCategory(name='poster', symbol_size=35), opts.GraphCategory(name='liker', symbol_size=10)]
    ).set_global_opts(title_opts=opts.TitleOpts(title="QQ空间好友关系图"))
    graph.render(output)
    print('绘制完成，准备打开{0}'.format(output))
    os.system('start {0}'.format(output))

if __name__ == "__main__":
    render()
