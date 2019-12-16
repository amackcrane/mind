

from datetime import datetime, date
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

        #return no_error & (c == context)
        return no_error


    def match_context(context, task_context):
        """Take in task-specific and general contex
        separated into strings, and see if a sublist matches"""
        if len(task_context) > len(context):
            return ContextHolder.match_context(task_context[:-1], context)
        else:
            # don't match on metacontext alone:
            if len(task_context) == 1:
                return False
            return task_context == context


    
    def __str__(self):
        return str(self.contexts)
            
            



                

class Context:
    def __init__(self, dict=None):
#        if  != None:
#            flat_contexts = context.contexts
#            self.contexts = OrderedDict()
#            for k,y in flat_contexts.items():
#                tasklist = list(map())
                
        self.contexts = OrderedDict()

#    def init_from_file(self, context):
#        pass
        

    def add_layer(self, context):
        pass


    def get_tasks(self, tasks):
        # collect a list of pointers to tasks!
        # make a this_context:task map

        for context in self.contexts.keys():
            context_tasks = list(filter(lambda x: context in x.context, tasks))
            self.contexts[context] = context_tasks
            
    def unpack(self, tasks):
        pass

    def reset(self):
        self.contexts = OrderedDict()

    def is_set(self):
        return len(self.contexts) > 0

    def list(self):
        return list(self.contexts.keys())
   
    def get_tasks(self):
        """Currently provides tasks for primary context only

        Returns copy of list"""        
        return list(list(self.contexts.values())[0])

    # TODO
    def __str__(self):
        return str(self.contexts)

    def __repr__(self):
        contexts_rep = {}
        for context,tasks in self.contexts.items():
            task_ids = list(map(lambda x: x.id, tasks))
            contexts_rep[context] = task_ids

        return str(contexts_rep)

       
class Task:

    def init_inner(self, id, content, target_date, sol_date, context):
        """create Task object

        Arguments:
        id - unique integer id, should be typeable
        descr - arbitrary string elaboration of task
        target_date - string in YYYY.MM.DD format; start date for task
        sol_date - string in YYYY.MM.DD; absolute deadline for task
        context - list of something!
        """
        self.id = id
        self.content = content
        self.target = Task.parse_date(target_date)
        self.sol = Task.parse_date(sol_date)

        if self.target >= self.sol:
            raise Exception("Invalid Dates in Task Entry")

        self.context = context
        self.finished = None # date finished

        
    def __init__(self, valid=None, task=None):
        if valid == None or task == None:
            return
        # so that it's possible to write type(Task()). may be a less
        #   hackish way...
        # wait, also used in register_task for manual initialization

        # I think this is parsing tasks which pyyaml has already made
        #   into Task objects, but...
        # not sure why we don't just load them directly into tasklist?
        if type(task) == type(Task()):
            self.init_inner(task.id, task.content, task.target, task.sol, task.context)
            return
            # consider 'return task'????
            # noop. init doesn't return the object

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

        # this is now handled for manual task entry
        # but keep around for now
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

    def set_target(string_date):
        self.target = Task.parse_date(string_date)

    def set_sol(string_date):
        self.sol = Task.parse_date(string_date)

    def set_content(string):
        self.content = string
        
    def __str__(self):
        return """------
        {0}
        id: {1}
        target: {2}
        sol: {3}
        context: {4}
        
        """.format(self.content, self.id, self.target, self.sol, self.context)


    # '==' will give deep equality
    def __eq__(self, other):
        return self.__dict__ == other.__dict__



