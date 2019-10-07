
import yaml
from enum import Enum
from mind.task import Task
import os


class Dependency(Enum):
    weak = 1
    strong = 2


class Edge:
    def __init__(self, src, dep, dep_type=Dependency.weak):
        self.source = src
        self.dependent = dep
        self.dep_type = dep_type

    def __str__(self):
        return "{0} --{2}--> {1}".format(self.source, self.dependent, self.dep_type.__name__)

    def elaborate(self):
        if type(self.source) == type(SimpleTask(-1)):
            pass
        #TODO
        
    def get_task(simpletask):
        pass
    # TODO
        
class SimpleTask:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "Task " + self.id
        
class Network:
    
    def __init__(self):
        self.network_file = "data/network.yml"
    
        if os.path.exists(self.network_file):
            with open(self.network_file) as f:
                self.edges = yaml.load(f)
        else:
            self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_dependencies(self, dependent):
        return list(filter(lambda x: x.dependent == dependent, self.edges))

    def get_dependents(self, source):
        return list(filter(lambda x: x.source == source, self.edges))


    def add_edge_interactive():
        print("\nCreate Link!")

        source = get_node("Source")
        dependent = get_node("Dependent")

        type = Dependency[input("'weak'/'strong': ")]

        self.add_edge(Edge(source, dependent, type))

    # TODO
    def dump(self):
        if len(self.edges) > 0: 
            with open(self.network_file, 'w') as f:
                yaml.dump(self.edges, f)
        else:
            os.remove(self.network_file)

# what is 'which_end'
# what does this do
def get_node(which_end):
    c = input(which_end + "\n't' for task; 'f' for filesystem: ")
    if c == "t":
        id = input("Task id: ")
        node = SimpleTask(id)
    elif c == "f":
        node = input("Filepath: ")
    else:
        print("try again?")
        node = get_node(which_end)

    return node
    


def get_edges():
    pass
#TODO

def dump_edges():
    pass
# TODO
    
