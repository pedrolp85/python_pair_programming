import pytest
import yaml


def read_yaml_file(file_name):
    with open(file_name) as cluster_file:
        return cluster_file.read()


def parse_yaml_file(yaml_string):
    return yaml.safe_load(yaml_string)


def dict_to_cluster(parsed_yaml):
    return None


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

    cluster_name = None

    assert cluster_name == expected_cluster_name


@pytest.mark.parametrize(
    "input_file, expected_cpu_count",
    [
        ("static_files/OCPCluster1.yml", 3.0),
        ("static_files/OCPCluster2.yml", 5.0),
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
    cpu_cores = None

    assert cpu_cores == expected_cpu_count, "Unmatched CPU count"


@pytest.mark.parametrize(
    "input_file, expected_memory_gig",
    [
        ("static_files/OCPCluster1.yml", 12.0),
        ("static_files/OCPCluster2.yml", 6.0),
        ("static_files/OCPCluster3.yml", 20.0),
        ("static_files/OCPCluster4.yml", 16.0),
        ("static_files/OCPCluster5.yml", 2.0),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_mem_count(input_file, expected_memory_gig):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])

    memory_gig = None

    assert memory_gig == expected_memory_gig, "Unmatched Memory count"


@pytest.mark.parametrize(
    "input_file, expected_nodes",
    [
        ("static_files/OCPCluster1.yml", ["node1", "node2"]),
        ("static_files/OCPCluster2.yml", ["node1B"]),
        ("static_files/OCPCluster3.yml", ["node1C", "node2C"]),
        ("static_files/OCPCluster4.yml", ["node1D", "node2D"]),
        ("static_files/OCPCluster5.yml", ["node1E", "node2E"]),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_all_nodes(input_file, expected_nodes):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])
    nodes = None

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

    cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])
    namespaces = None

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

    cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])
    pods = None

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

    cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])
    ns = None
    assert sorted(ns) == sorted(expected_ns), "Unmatched filtered ns names"


@pytest.mark.parametrize(
    "input_file,label,expected_label_values",
    [
        (
            "static_files/OCPCluster1.yml",
            "app",
            ("AppInClusterA", "AppInClusterA2", "AppInClusterA3"),
        ),
        ("static_files/OCPCluster1.yml", "tier", ("pod_1", "pod2", "pod_3")),
        ("static_files/OCPCluster1.yml", "node_name", ("node1", "node2")),
        ("static_files/OCPCluster1.yml", "ns_name", ("ns1", "ns2", "ns3")),
    ],
    ids=["node1", "node1", "node1", "node1"],
)
def test_get_cluster_labels(input_file, label, expected_label_values):
    read_yaml = read_yaml_file(input_file)
    parsed_file = parse_yaml_file(read_yaml)

    cluster = dict_to_cluster(parsed_file["data"][0]["OCPCluster"])
    label_values = None

    assert label_values == expected_label_values, "Unmatched label_values"
