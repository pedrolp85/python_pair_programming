from dataclasses import dataclass
from dataclasses import field

import pytest
import yaml


@dataclass
class Pod:
    name: str


@dataclass
class Namespace:
    name: str
    pods: list[Pod]

    def __post_init__(self):
        pod_data = []

        for pod in self.pods:
            pod_data.append(Pod(pod["pod_name"]))

        self.pods = pod_data


@dataclass
class Node:
    name: str
    cpu_cores: float
    memory_gig: float
    namespaces: list[Namespace]

    def __post_init__(self):
        ns_data = []
        for ns_name in self.namespaces.keys():
            ns_data.append(Namespace(ns_name, self.namespaces[ns_name]["pods"]))

        self.namespaces = ns_data


@dataclass
class OCPCluster:
    cluster_name: str
    cpu_cores: float = field(init=False)
    memory_gig: float = field(init=False)
    nodes: list[Node]

    def __post_init__(self):
        self.cpu_cores = 0.0
        self.memory_gig = 0.0

        nodes_data = []
        for node in self.nodes:
            nodes_data.append(
                Node(node["node_name"], node["cpu_cores"], node["memory_gig"], node["namespaces"])
            )
            self.cpu_cores += node["cpu_cores"]
            self.memory_gig += node["memory_gig"]

        self.nodes = nodes_data

    def get_all_nodes(self):
        return [node.name for node in self.nodes]


def read_yaml_file(file_name):
    with open(file_name) as cluster_file:
        return cluster_file.read()


def parse_yaml_file(yaml_string):
    return yaml.safe_load(yaml_string)


def dict_to_cluster(parsed_yaml) -> OCPCluster:
    return OCPCluster(**parsed_yaml)


@pytest.mark.parametrize(
    "input_file, expected_cluster_name",
    [
        ("static_files/OCPCluster1.yml", "OCPCluster1"),
        ("static_files/OCPCluster2.yml", "OCPCluster2"),
        ("static_files/OCPCluster3.yml", "OCPCluster3"),
        ("static_files/OCPCluster4.yml", "OCPCluster4"),
        ("static_files/OCPCluster5.yml", "OCPCluster5"),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_cluster_name(input_file, expected_cluster_name):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    OCP_cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])

    assert OCP_cluster.cluster_name == expected_cluster_name, "Unmatched cluster name"


@pytest.mark.parametrize(
    "input_file, expected_cpu_count",
    [
        ("static_files/OCPCluster1.yml", 3.0),
        ("static_files/OCPCluster2.yml", 2.0),
        ("static_files/OCPCluster3.yml", 11.0),
        ("static_files/OCPCluster4.yml", 14.0),
        ("static_files/OCPCluster5.yml", 8.0),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_cpu_count(input_file, expected_cpu_count):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    OCP_cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])

    assert OCP_cluster.cpu_cores == expected_cpu_count, "Unmatched CPU count"


@pytest.mark.parametrize(
    "input_file, expected_memory_gig",
    [
        ("static_files/OCPCluster1.yml", 12.0),
        ("static_files/OCPCluster2.yml", 2.0),
        ("static_files/OCPCluster3.yml", 20.0),
        ("static_files/OCPCluster4.yml", 16.0),
        ("static_files/OCPCluster5.yml", 2.0),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_mem_count(input_file, expected_memory_gig):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    OCP_cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])

    assert OCP_cluster.memory_gig == expected_memory_gig, "Unmatched Memory count"


@pytest.mark.parametrize(
    "input_file, expected_nodes",
    [
        ("static_files/OCPCluster1.yml", ["node1", "node2"]),
        ("static_files/OCPCluster2.yml", ["node1B"]),
        ("static_files/OCPCluster3.yml", ["node1C", "node2C"]),
        ("static_files/OCPCluster4.yml", ["node1C", "node2C"]),
        ("static_files/OCPCluster5.yml", ["node1E", "node2E"]),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_all_nodes(input_file, expected_nodes):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    OCP_cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])
    nodes = OCP_cluster.get_all_nodes()

    assert sorted(nodes) == sorted(expected_nodes), "Unmatched node names"


@pytest.mark.parametrize(
    "input_file, expected_namespaces",
    [
        ("static_files/OCPCluster1.yml", ["ns1", "ns2", "ns3"]),
        ("static_files/OCPCluster2.yml", ["ns1"]),
        ("static_files/OCPCluster3.yml", ["ns1", "ns2", "ns3", "ns4", "ns5"]),
        ("static_files/OCPCluster4.yml", ["ns1", "ns2"]),
        ("static_files/OCPCluster5.yml", ["ns1", "ns2", "ns3"]),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_all_namespaces(input_file, expected_namespaces):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    OCP_cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])
    namespaces = OCP_cluster.get_all_nodes()

    assert sorted(namespaces) == sorted(expected_namespaces), "Unmatched ns names"


@pytest.mark.parametrize(
    "input_file, expected_pods",
    [
        ("static_files/OCPCluster1.yml", ["pod1", "pod2", "pod3"]),
        ("static_files/OCPCluster2.yml", ["pod1", "pod2"]),
        (
            "static_files/OCPCluster3.yml",
            [
                "pod1",
                "pod2",
                "pod3",
                "pod4",
                "pod2",
                "pod1",
                "pod2",
                "pod4",
                "pod1",
                "pod4",
                "pod2",
            ],
        ),
        ("static_files/OCPCluster4.yml", ["pod1", "pod2"]),
        ("static_files/OCPCluster5.yml", ["pod1", "pod2", "pod3"]),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_all_pods(input_file, expected_pods):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    OCP_cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])
    pods = OCP_cluster.get_all_pods()

    assert sorted(pods) == sorted(expected_pods), "Unmatched pod names"


@pytest.mark.parametrize(
    "input_file, nodes_regex,expected_ns",
    [
        ("static_files/OCPCluster1.yml", "node1", ["ns1", "ns2"]),
        ("static_files/OCPCluster1.yml", "node2", ["ns3"]),
        ("static_files/OCPCluster1.yml", "node", ["ns1", "ns2", "ns3"]),
        ("static_files/OCPCluster1.yml", "fake:regex", []),
    ],
    ids=["node1", "node2", "node", "fake_regex"],
)
def test_get_ns_by_node(input_file, nodes_regex, expected_ns):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    OCP_cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])
    ns = OCP_cluster.get_ns_by_node(nodes_regex)

    assert sorted(ns) == sorted(expected_ns), "Unmatched filtered ns names"


@pytest.mark.parametrize(
    "input_file,label,expected_label_values",
    [
        ("static_files/OCPCluster1.yml", "ns_name", ("ns1")),
        ("static_files/OCPCluster1.yml", "tier", ("pod_1", "pod2", "pod_3")),
        ("static_files/OCPCluster1.yml", "node_name", ("node1", "node2")),
        ("static_files/OCPCluster1.yml", "ns_name", ("ns1", "ns2", "ns3")),
    ],
    ids=["node1", "node1", "node1", "node1"],
)
def test_get_cluster_labels(input_file, label, expected_label_values):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    OCP_cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])
    label_values = OCP_cluster.get_cluster_labels()[label]

    assert label_values == expected_label_values, "Unmatched label_values"
