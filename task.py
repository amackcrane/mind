

from datetime import datetime
#from aenum import Enum, skip
#from enum import Enum
from collections import OrderedDict



class ContextHolder:

    def unpack_context(stub, context_dict):
        new_dict = {}
        for k,v in context_dict.items():
            newstub = stub + "." + k

            if type(v) == type({}):
                new_dict[k] = ContextHolder.unpack_context(newstub, v)
            elif type(v) == type(None) or type(v) == type(""):
                new_dict[k] = newstub
            else:
                raise Exception("Bad context.yml: got " + str(v))

        return new_dict

    def __init__(self, metacontext_dict):
        self.contexts = {}
        for k,v in metacontext_dict.items():
            self.contexts[k] = ContextHolder.unpack_context(k, v)
            # for now we won't have colons in context syntax (cuz makes recursive
            #   parsing messy)


    def valid(self, context):
        parts = context.split(".")
        c = self.contexts
        no_error = True

        try:
            for p in parts:
                c = c[p]
        except(KeyError):
            no_error = False

        return no_error & (c == context)

    def __str__(self):
        return str(self.contexts)
            
            



                

class Context:
    def __init__(self):
       self.contexts = OrderedDict()

    def add_layer(self, context, tasks):

       # collect a list of pointers to tasks!
       # make a this_context:task map
       context_tasks = list(filter(lambda x: context in x.context, tasks))
       self.contexts[context] = context_tasks


    def reset(self):
       self.contexts = OrderedDict()

    def is_set(self):
       return len(self.contexts) > 0

    def get_tasks(self):
        """Currently provides tasks for primary context only

        Returns copy of list"""        
        return list(list(self.contexts.values())[0])

    # TODO
    def __str__(self):
        return str(self.contexts)

       
class Task:

    def init_inner(self, id, content, target_date, sol_date, context):
        """create Task object

        Arguments:
        id - unique integer id, should be human-typeable
        descr - arbitrary string elaboration of task
        target_date - string in YYYY.MM.DD format; start date for task
        sol_date - string in YYYY.MM.DD; absolute deadline for task
        context - list of something!
        """
        self.id = id
        self.content = content
        self.target = target_date
        self.sol = sol_date
        self.context = context

        
    def __init__(self, valid=None, task=None):
        if valid == None or task == None:
            return
        # so that it's possible to write type(Task()). may be a less hackish way...
        
        if type(task) == type(Task()):
            self.init_inner(task.id, task.content, task.target, task.sol, task.context)
            return

        task_dict = task
        
        context_list = []
        raw_contexts = task_dict["context"]
        for c in raw_contexts:
            if valid(c):
                context_list.append(c)
            else:
                raise Exception("Bad context supplied to task " + task_dict["id"])

        try:
            target = Task.parse_date(task_dict["target"])
            sol = Task.parse_date(task_dict["sol"])
        except ValueError:
            raise Exception("Bad date in task " + task_dict["id"])
            
        self.init_inner(int(task_dict["id"]), task_dict["content"],
                    target, sol, context_list)

    def urgency(self, ref = None):
        """Calculates the time elapsed as proportion of time allotted"""
        if ref == None:
            ref = datetime.now()

        if self.sol < self.target:
            raise Exception("Bad dates in task " + self.id)
            
        return (ref - self.target) / (self.sol - self.target)
            


    # todo: implement a tzinfo for absolute datetime's!
    def parse_date(string_date):
        if type(string_date) == type(datetime.min):
           return string_date

        try:
            list_date = list(map(int, string_date.split(".")))
        except ValueError:
            raise ValueError
        date = datetime(list_date[0], list_date[1], list_date[2])
        return date

    #def serialize_date(date_time):
        
    def __str__(self):
        return """------
        {0}
        id: {1}
        target: {2}
        sol: {3}
        context: {4}
        
        """.format(self.content, self.id, self.target, self.sol, self.context)




