def extract_labels_to_dict(parsed_yaml, labels_attribute):
    result = {}
    label_list = parsed_yaml.get(labels_attribute, [])
    if len(label_list):
        for token in label_list.split('|'):
            k, v = token.split(':')
            result[k[6:]] = v
    return result

class Pod:
    def __init__(self, parsed_yaml):
        self.name = parsed_yaml['pod_name']
        self.labels = extract_labels_to_dict(parsed_yaml, 'labels')

class Namespace:
    def __init__(self, name, parsed_yaml):
        self.name = name
        self.pods = []
        for podinfo in parsed_yaml['pods']:
            self.pods.append(Pod(podinfo))

        self.labels = extract_labels_to_dict(parsed_yaml, 'namespace_labels')


class Node:
    def __init__(self, parsed_yaml):
        self.name = parsed_yaml['node_name']
        self.cpu_cores = int(parsed_yaml['cpu_cores'])
        self.mem = int(parsed_yaml['memory_gig'])
        self.namespaces = []
        for nskey, nsvalue in parsed_yaml['namespaces'].items():
            self.namespaces.append(Namespace(nskey, nsvalue))

        self.labels = extract_labels_to_dict(parsed_yaml, 'node_labels')

    def get_namespace_names(self):
        return [ns.name for ns in self.namespaces]


class Cluster:
    def __init__(self, parsed_yaml):
        self.name = parsed_yaml['data'][0]['OCPCluster']['cluster_name']
        self.nodes = []
        for n in parsed_yaml['data'][0]['OCPCluster']['nodes']:
            self.nodes.append(Node(n))

    def get_cpu_cores(self):
        return sum([int(x.cpu_cores) for x in self.nodes])

    def get_mem(self):
        return sum([int(x.mem) for x in self.nodes])

    def get_node_list(self):
        return [n.name for n in self.nodes]

    def get_namespace_list(self):
        result = []
        for n in self.nodes:
            result += n.get_namespace_names()
        return result

    def get_pods(self):
        result = []
        for n in self.nodes:
            for ns in n.namespaces:
                for p in ns.pods:
                   result.append(p.name)
        return result

    def get_namespaces(self, node_name):
        result = []
        for n in self.nodes:
            if node_name in n.name:
                for ns in n.get_namespace_names():
                    result.append(ns)

        return result

    def get_all_labels(self, labelkey):
        result = []
        candidate = None
        for n in self.nodes:
            if labelkey in n.labels:
                candidate = n.labels[labelkey]
            for ns in n.namespaces:
                if labelkey in ns.labels:
                    candidate = ns.labels[labelkey]
                for p in ns.pods:
                    if labelkey in p.labels:
                        candidate = p.labels[labelkey]
                if candidate:
                    result.append(candidate)
                candidate = None

        return tuple(result)