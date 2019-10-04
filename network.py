
from enum import Enum
from mind.task import Task

#import importlib.machinery
#mind = importlib.machinery.SourceFileLoader('mind', "src/mind.py").load_module()
# TODO -- mind doesn't like being named for yaml.load reasons...

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
    
