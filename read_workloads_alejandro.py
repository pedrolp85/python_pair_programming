import re
from dataclasses import dataclass

import pytest
import yaml


@dataclass
class Label:
    key: str
    value: str

    def __init__(self, string: str):
        self.key, self.value = string.split(":")
        self.key = self.key.replace("label_", "")

    @staticmethod
    def get_labels_from_string(label_string: str):
        if not label_string:
            return []

        return [Label(label) for label in label_string.split("|") if label]


class Pod:
    def __init__(self, dictionary: dict):
        self.pod_name = dictionary["pod_name"]
        self.labels = Label.get_labels_from_string(dictionary.get("labels", ""))

    def get_pod_name(self):
        return self.pod_name

    def get_labels_with_depth(self, regex: str):
        return [(label.key, label.value, 3) for label in self.labels if re.match(regex, label.key)]


class Namespace:
    def __init__(self, values):
        self.name = values[0]
        self.pods = [Pod(pod) for pod in values[1].get("pods", [])]
        self.labels = Label.get_labels_from_string(values[1].get("namespace_labels", ""))

    def get_name(self):
        return self.name

    def get_all_pods(self):
        return [pod for pod in self.pods]

    def get_labels_with_depth(self, regex: str):
        return [
            (label.key, label.value, 2) for label in self.labels if re.match(regex, label.key)
        ] + [
            label_with_depth
            for pod in self.pods
            for label_with_depth in pod.get_labels_with_depth(regex)
        ]


class Node:
    def __init__(self, dictionary: dict):
        self.name = dictionary["node_name"]
        self.labels = Label.get_labels_from_string(dictionary.get("node_labels", ""))
        self.cpu_cores = dictionary["cpu_cores"]
        self.memory_gig = dictionary["memory_gig"]
        self.namespaces = [Namespace(namespace) for namespace in dictionary["namespaces"].items()]

    def get_node_name(self):
        return self.name

    def get_cpu_cores(self):
        return self.cpu_cores

    def get_memory_gig(self):
        return self.memory_gig

    def get_all_namespaces_names(self):
        return [namespace.get_name() for namespace in self.namespaces]

    def get_all_pods(self):
        return [pod for namespace in self.namespaces for pod in namespace.get_all_pods()]

    def get_labels_with_depth(self, regex: str):
        return [
            (label.key, label.value, 1) for label in self.labels if re.match(regex, label.key)
        ] + [
            label_with_depth
            for namespace in self.namespaces
            for label_with_depth in namespace.get_labels_with_depth(regex)
        ]


class Cluster:
    def __init__(self, dictionary: dict):
        self.name = dictionary["data"][0]["OCPCluster"]["cluster_name"]
        self.nodes = [Node(node) for node in dictionary["data"][0]["OCPCluster"]["nodes"]]

    def get_cluster_name(self):
        return self.name

    def get_cpu_count(self):
        return sum([node.get_cpu_cores() for node in self.nodes])

    def get_memory_count(self):
        return sum([node.get_memory_gig() for node in self.nodes])

    def get_all_nodes(self):
        return [node.get_node_name() for node in self.nodes]

    def get_all_namespaces(self):
        return [namespace for node in self.nodes for namespace in node.get_all_namespaces_names()]

    def get_all_pod_names(self):
        return [pod.get_pod_name() for node in self.nodes for pod in node.get_all_pods()]

    def get_ns_by_node(self, node_regex: str):
        return [
            namespace
            for node in self.nodes
            for namespace in node.get_all_namespaces_names()
            if re.match(node_regex, node.get_node_name())
        ]

    def get_all_labels(self, regex: str):
        labels_with_depth = [
            label_with_depth
            for node in self.nodes
            for label_with_depth in node.get_labels_with_depth(regex)
        ]

        # Compute the highest depth structure for each key
        label_highest_depth = {}

        for label, _, depth in labels_with_depth:
            if label not in label_highest_depth or label_highest_depth[label] < depth:
                label_highest_depth[label] = depth

        # Only take into account the highest depth structure for each key
        return [
            value
            for label, value, depth in labels_with_depth
            if depth == label_highest_depth[label]
        ]


def read_yaml_file(file_name):
    with open(file_name) as cluster_file:
        return cluster_file.read()


def parse_yaml_file(yaml_string):
    return yaml.safe_load(yaml_string)


def dict_to_cluster(parsed_yaml):
    return Cluster(parsed_yaml)


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

    cluster = dict_to_cluster(parsed_file)

    cluster_name = cluster.get_cluster_name()

    assert cluster_name == expected_cluster_name


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

    cluster = dict_to_cluster(parsed_file)
    cpu_cores = cluster.get_cpu_count()

    assert cpu_cores == expected_cpu_count, "Unmatched CPU count"


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

    cluster = dict_to_cluster(parsed_file)

    memory_gig = cluster.get_memory_count()

    assert memory_gig == expected_memory_gig, "Unmatched Memory count"


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

    cluster = dict_to_cluster(parsed_file)
    nodes = cluster.get_all_nodes()

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

    cluster = dict_to_cluster(parsed_file)
    namespaces = cluster.get_all_namespaces()

    assert sorted(namespaces) == sorted(expected_namespaces), "Unmatched ns names"


@pytest.mark.parametrize(
    "input_file, expected_pods",
    [
        ("static_files/OCPCluster1.yml", ["pod_1", "pod_2", "pod_3"]),
        ("static_files/OCPCluster2.yml", ["pod_1", "pod_2"]),
        (
            "static_files/OCPCluster3.yml",
            [
                "pod_1",
                "pod_2",
                "pod_3",
                "pod_4",
                "pod_2",
                "pod_1",
                "pod_2",
                "pod_4",
                "pod_1",
                "pod_4",
                "pod_2",
            ],
        ),
        ("static_files/OCPCluster4.yml", ["pod_1", "pod_2"]),
        ("static_files/OCPCluster5.yml", ["pod_1", "pod_2", "pod_3"]),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_all_pods(input_file, expected_pods):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    cluster = dict_to_cluster(parsed_file)
    pods = cluster.get_all_pod_names()

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

    cluster = dict_to_cluster(parsed_file)
    ns = cluster.get_ns_by_node(nodes_regex)
    assert sorted(ns) == sorted(expected_ns), "Unmatched filtered ns names"


@pytest.mark.parametrize(
    "input_file,label,expected_label_values",
    [
        (
            "static_files/OCPCluster1.yml",
            "app",
            ["AppInClusterA", "AppInClusterA2", "AppInClusterA3"],
        ),
        ("static_files/OCPCluster1.yml", "tier", ["pod_1", "pod_2", "pod_3"]),
        ("static_files/OCPCluster1.yml", "node_name", ["node1", "node2"]),
        ("static_files/OCPCluster1.yml", "ns_name", ["ns1", "ns2", "ns3"]),
    ],
    ids=["node1", "node1", "node1", "node1"],
)
def test_get_cluster_labels(input_file, label, expected_label_values):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    cluster = dict_to_cluster(parsed_file)
    label_values = cluster.get_all_labels(label)

    assert label_values == expected_label_values, "Unmatched label_values"


if __name__ == "__main__":
    for i in range(5):
        filename = f"static_files/OCPCluster{i + 1}.yml"
        read_yaml = read_yaml_file(filename)
        parsed_file = parse_yaml_file(read_yaml)
        cluster = dict_to_cluster(parsed_file)
