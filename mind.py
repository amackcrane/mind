
import yaml
import functools
from mind.task import Task, Context, ContextHolder
from datetime import datetime



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
        self.ch = ContextHolder(metacontext_dict)

        # read in tasks
        with open("data/tasks.yml") as f:
            task_dict = yaml.load(f)
        try: task_dict
        except NameError:
            raise IOError("I/O fail w/ tasks.yml")

        # list of tasks
        self.tasks = self.unpack_tasks(task_dict)

        # initialize context
        self.context = Context()


    def get_context(self):
        to_return = []

        print("\nGetting Context!")

        while True:
            context_in = input("enter '.'-delim context, 'q' to quit, <Enter> for ref: ")
            if context_in == "q":
                break
            elif self.ch.valid(context_in):
                to_return.append(context_in)
            else:
                #print("Didn't recognize. Try again?")
                print(yaml.dump(self.ch))

        return to_return
        

    def set_context(self):
        list(map(lambda x: self.context.add_layer(x, self.tasks),
            self.get_context()))
        
    def unpack_tasks(self, task_list):
        return list(map(functools.partial(Task, self.ch.valid), task_list))

    def register_task(self):

        print("\nRegister a Task!")
        
        context = None
        # check if context already specified
        if self.context.is_set():
            if input("Use present context? y/n:") == "y":
                context = list(self.context.keys())
            else:
                context = self.get_context()
        else:
            context = self.get_context()

        if context == None:
            print("Task Registration Failed -- No Context")
            return

        id = self.get_free_id()
        content = input("Content: ")
        target = input("target date (Y.M.D):")
        sol = input("super duper deadline date (Y.M.D):")

        t = Task()
        t.init_inner(id, content, target, sol, context)
        
        self.tasks.append(t)

        self.dump_tasks()

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


    def dump_tasks(self):
        with open(self.task_file, 'w') as f:
            yaml.dump(self.tasks, f)

    def dump_contexts(self):
        with open(self.context_file, 'w') as f:
            yaml.dump(self.ch.contexts, f)

    def dump(self):
        self.dump_tasks()
        self.dump_contexts()

    # this will prob be piped to grep...
    def print_tasks(self):
        to_print = ""
        for task in self.tasks:
            to_print += "{0}    {1}\n".format(task.id, task.content)

        print(to_print)

    def get_tasklist(self):
        if not self.context.is_set():
            self.set_context()

        # get today's date
        today = datetime.now()

        # first just for primary context...
        tasks = self.context.get_tasks() # deep list copy
        tasks = list(filter(lambda x: x.target < today, tasks))  # only consider current tasks
        tasks.sort(key = lambda x: x.sol)  # sort based on SOL date
        #tasks.sort(key = lambda x: x.urgency())

        print(functools.reduce(lambda x,y: x+y, map(str, tasks)))
        
