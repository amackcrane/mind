
import yaml, datetime
#from aenum import Enum, skip
from enum import Enum
from collections import OrderedDict
import functools


class Mind:

    def __init__(self):
        self.task_file = "data/tasks.yml"
        self.context_file = "data/context.yml"

        # parse in context tree
        with open("data/context.yml") as f:
            metacontext_dict = yaml.load(f)
        try: metacontext_dict
        except:
            raise IOError("I/O fail w/ context.yml")

        # metacontext:context_list dict
        # where list element can also be dicts

        # parse YAML dict into ContextHolder object
        self.ch = ContextHolder(unpack_contexts(metacontext_dict))

        # read in tasks
        with open("data/tasks.yml") as f:
            task_dict = yaml.load(f)
        try: task_dict
        except NameError:
            raise IOError("I/O fail w/ tasks.yml")

        # list of tasks
        self.tasks = unpack_tasks(task_disk)

        # initialize context
        self.context = None

    def get_context(self):
        to_return = []
        # list metacontexts and prompt for one
        metacontexts = self.ch.keys()
        while True:
            mc_ind = input("pick a metacontext by index\n" + str(metacontexts))
            mc = self.ch[metacontexts.pop(mc_ind)] # pointer to context enum
            contexts = mc.list()
            c_ind = input("pick a context by index\n" + str(contexts))
            context = mc(c_ind) # does this work???

            to_return.append(context)

            brk = input("Done? y/n:")
            if brk == "y":
                break

    def set_context(self):
        self.context = Context()
        map(lambda x: self.context.add_layer(x),
            self.get_context())
        
            

        
    def unpack_contexts(metacontext_dict):
        """convert key:list context dict to list<Enum>"""
        metacontexts = []
        for key,value in metacontext_dict.items():
            metacontexts.append(unpack_context(key, value))

        return metacontexts


    def unpack_context(metacontext, context_list):
        """Convert metacontext : context_list dict to Enum
        named 'metacontext' with elements from context_list

        if context_list contains another dict, recur and save the
        resultant Enum as the value corresponding to the element
        """
        flat_context_list = []
        nested_context_dict = {}

        for context in context_list:
            if type(context) == type(""): # if string, just slot in
                flat_context_list.append(context)
            elif type(context) == type({}):  # if dict
                # pull out key
                key = list(context.keys())[0]
                # slot key in
                flat_context_list.append(key)
                # save Enum of subcontexts
                nested_context_dict[key] = unpack_context(key, context[key])
            else:
                raise Exception("Bad context.yml: got " + str(context))

        # from flat list, make a context : int dict for Enum
        context_dict = dict(zip(flat_context_list, range(len(context_list))))

        # insert nested subcontext enum in place of int where indicated
        for key,value in nested_context_dict.items():
            context_dict[key] = value

        return Enum(metacontext, context_dict)

    def unpack_tasks(task_list):
        return list(map(self.unpack_task, task_list))
    
    def unpack_task(self, task_dict):
        context_list = []
        raw_contexts = task_dict["context"]
        for c in raw_contexts:
            c = c.split(".")
            metacontext = context[0]
            context = context[1]
            try:
                context_list.append(self.ch.contexts[metacontext][context])
            except KeyError:
                raise Exception("context name error in task " + task_dict["id"])

        target = parse_date(task_dict["content"])
        sol = parse_date(task_dict["sol"])
            
        return Task(int(task_dict["id"]), task_dict["content"],
                    target, sol, context_list)
                                         

    # todo: implement a tzinfo for absolute datetime's!
    def parse_date(string_date):
        list_date = string_date.split(".")
        date = datetime(list_date[0], list_date[1], list_date[2])


    def get_free_id(self):
        free_ids = {}
        taken_ids = list(map(lambda x: x.id, self.tasks))

        it = 0
        while True:
            nums = set(range(100 * it, 100 * (it + 1)))
            free_nums = nums.difference(taken_ids)
            if len(free_nums) > 0:
                break
            else:
                it += 1

        return min(free_nums)

    
    class Task:

        def __init__(self, id, content, target_date, sol_date, context):
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

    def register_task(self):
        context = None
        # check if context already specified
        if self.context.is_set():
            if input("Use present context? y/n:") == "y":
                context = list(self.context.keys())
            else:
                context = self.get_context()

        id = self.get_free_id()
        content = input("Content: ")
        target = input("target date (Y.M.D):")
        sol = input("super duper deadline date (Y.M.D):")

        self.tasks.append(Task(id, content, target, sol, context))

        self.dump_tasks()

    def dump_tasks(self):
        with open(self.task_file) as f:
            yaml.dump(self.tasks, f)

    class ContextHolder:

        def __init__(self, metacontext_list):
            """ContextHolder; holds name:Enum map of dynamically created context objs"""
            self.contexts = {}
            for metacontext in metacontext_list:
                self.contexts[metacontext.__name__] = metacontext


    class Context:
        def __init__(self):
           self.contexts = OrderedDict()

        def add_layer(self, context):

           # collect a list of pointers to tasks!
           # make a this_context:task map
           tasks = functools.filter(lambda x: context in x.context,
                                    self.tasks)
           self.contexts[context] = tasks


        def reset(self):
           self.contexts = OrderedDict()

        def is_set(self):
           return len(self.contexts) > 0

        # TODO
        def toString(self):
            return str(self.contexts)
        
       
