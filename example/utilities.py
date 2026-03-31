import random
import networkx as nx

def generate_random_subnetworks(main_network: nx.Graph, nodes_in_subnetwork:int) -> list[list[int]]:
    """
    Generate equal subnetworks from the given main network. Returns only the IDs
    :param main_network: networkx graph instance
    :param nodes_in_subnetwork: No. of nodes present in each subnetwork
    :return: 2-D list of indices of nodes with each list being a subnetwork
    """

    nodes = list(main_network)
    random.shuffle(nodes)

    if nodes_in_subnetwork <= 0 or len(nodes) % nodes_in_subnetwork != 0 or nodes_in_subnetwork % 2:
        raise ValueError(f'Invalid no. of nodes = {nodes_in_subnetwork}')

    nsub_networks = int(len(nodes) / nodes_in_subnetwork)

    return [nodes[i * nodes_in_subnetwork: (i + 1) * nodes_in_subnetwork] for i in range(nsub_networks)]

