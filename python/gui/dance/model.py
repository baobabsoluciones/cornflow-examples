import pulp
import pytups as pt
from cornflow_client import group_variables_by_name
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def build_model(data, dataset_name=''):
    nodes = data['nodes']
    pairs = data['pairs']
    num_max_colors = len(nodes)
    colors = range(num_max_colors)
    color_weight = pt.SuperDict.fromkeys(colors).kapply(lambda k: k)

    nodes_color = pt.TupList((n, c) for n in nodes for c in colors)
    node_color = pulp.LpVariable.dicts(name='node_color', indexs=nodes_color, cat=pulp.LpBinary)
    node_color = pt.SuperDict(node_color)
    color_used = pulp.LpVariable.dicts('color_used', colors, 0, 1, cat=pulp.LpBinary)
    color_used = pt.SuperDict(color_used)

    colors_per_node = node_color.to_tuplist().to_dict(result_col=2, indices=[0])
    nodes_per_color = node_color.to_tuplist().to_dict(result_col=2, indices=[1])

    model = pulp.LpProblem('dance_pairing_' + dataset_name, sense=pulp.LpMinimize)
    model += pulp.lpSum(color_used * color_weight), "objective"

    for n in nodes:
        model += pulp.lpSum(colors_per_node[n]) == 1, "node_{}".format(n)

    for c in colors:
        model += color_used[c]*len(nodes) >= pulp.lpSum(nodes_per_color[c]), "color_{}".format(c)

    for c in colors:
        for p1, p2 in pairs:
            model += node_color[p1, c] + node_color[p2, c] <= 1, "color_pair_{}_{}_{}".format(c, p1, p2)
    return model.to_dict()

def solve_model(model_dict):
    model_vars, model = pulp.LpProblem.from_dict(model_dict)
    model.solve()
    return model.to_dict()

def get_solution_from_model(model_dict):
    model_vars, model = pulp.LpProblem.from_dict(model_dict)
    named_vars = group_variables_by_name(model_vars, ['color_used', 'node_color'], force_number=True)
    pt.SuperDict(named_vars['color_used']).vapply(pulp.value).vfilter(lambda v: v > 0.5).keys_tl()
    return \
        pt.SuperDict(named_vars['node_color']).\
        vapply(pulp.value).\
        vfilter(lambda v: v > 0.5).\
        keys_tl().\
        to_dict(result_col=1, is_list=False)

def graph_solution(data, solution, path='path.png'):
    """

    :param dict solution: {node: color}
    :return:
    """
    _colors = list(colors.BASE_COLORS.keys())
    _colors += _colors
    solution_colored = \
        pt.SuperDict(solution).vapply(lambda v: dict(color=_colors[v])).items_tl()
    node_colors = solution_colored.take(1).vapply(lambda v: v['color'])
    nodes = solution_colored.take(0)
    nodes_labels = nodes.to_dict(None).vapply(lambda v: v)
    G = nx.Graph()
    edges = data['pairs']
    G.add_nodes_from(solution_colored)
    G.add_edges_from(edges)
    plt.show()
    options = {"node_size": 500}
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx_nodes(G=G, pos=pos, node_color=node_colors, **options)
    nx.draw_networkx_edges(G=G, pos=pos, edgelist=edges)
    nx.draw_networkx_labels(G=G, pos=pos, labels=nodes_labels, font_color='white', font_size=16)
    plt.savefig(path)
    return


def read_file(filePath):
    with open(filePath, 'r') as f:
        contents = f.read().splitlines()

    pairs = \
        pt.TupList(contents[1:]).\
        vapply(lambda v: v.split(' ')).\
        vapply(lambda v: [int(v[0]), int(v[1])]).\
        vapply(tuple)
    num_nodes, num_pairs = [int(a) for a in contents[0].split(' ')]
    nodes = range(num_nodes)
    return dict(nodes=nodes, pairs=pairs)

if __name__ == '__main__':
    fileName = './python/gui/Baile/data/gc_4_1'
    data = read_file(fileName)
    model_dict = build_model(data)
    model_dict = solve_model(model_dict)
    solution = get_solution_from_model(model_dict)
    graph_solution(data, solution)