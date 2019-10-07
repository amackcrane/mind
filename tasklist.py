
import yaml
import functools
from mind.task import Task, Context, ContextHolder
from datetime import datetime, date
import os
from collections import namedtuple


Filenames = namedtuple("Filenames", ["tasks", "contexts",
                                     "next_id", "finished","current_context"])

default_filenames = Filenames(tasks="data/tasks.yml",
                     contexts="data/contexts.yml",
                     next_id="data/next_id.yml",
                     finished="data/finished.yml",
                     current_context="data/current_context.yml")


class Tasklist:

    
    def __init__(self, filename_dict=default_filenames):

        self.task_file = filename_dict.tasks
        self.context_file = filename_dict.contexts
        self.next_id_file = filename_dict.next_id
        self.finished_file = filename_dict.finished
        self.current_context_file = filename_dict.current_context

        # parse in context tree
        try:
            with open(self.context_file) as f:
                metacontext_dict = yaml.load(f)
        except FileNotFoundError:
            raise IOError("I/O fail w/ contexts.yml")

        # metacontext:context_list dict
        # where list element can also be dicts

        # parse YAML dict into ContextHolder object
        self.ch = ContextHolder(metacontext_dict)

        # read in tasks
        try:
            with open(self.task_file) as f:
                task_list = yaml.load(f)
        except FileNotFoundError:
            print("WARNING: didn't find tasks.yml; starting fresh from user input")
            task_list = []
            #raise IOError("I/O fail w/ tasks.yml")

        # list of tasks
        #self.tasks = self.unpack_tasks(task_list)
        self.tasks = task_list  # should parse straight to objects now

        # initialize context
        if os.path.exists(self.current_context_file):
            with open(self.current_context_file) as f:
                self.context = yaml.load(f)
        else:
            self.context = []


    def get_context_interactive(self):
        to_return = []

        print("\nGetting Context!")

        while True:
            context_in = input("enter '.'-delim context, 'q'=quit, 'f'=finish, <Enter> for ref: ")
            if context_in == "q":
                return None
            elif context_in == "f":
                break
            elif self.ch.valid(context_in):
                to_return.append(context_in)
            else:
                #print("Didn't recognize. Try again?")
                print(yaml.dump(self.ch))

        return to_return
        

    def set_context(self, to_set=None):
        if to_set == None:
            to_set = self.get_context_interactive()

        # If user quit interactive context setting, do nothing
        if to_set != None:
            #self.context = []
            #list(map(lambda x: self.context.add_layer(x, self.tasks), to_set))

            self.context = to_set

            # persist it ayyy
            self.dump_context()

    def get_context(self):
        #return self.context.list()
        return self.context

    def print_context(self):
        print(self.context)

    # unnecessary. just assign task_list; it's properly parsing the YAML to tasks...
    #def unpack_tasks(self, task_list):
    #    return list(map(functools.partial(Task, self.ch.valid), task_list))

    # consider moving as much functionality as possible to Task?
    def register_task(self):

        print("\nRegister a Task!\n('q' anytime quits)\n")
        
        context = None
        # check if context already specified
        if len(self.context)>0:
            if input("Use present context? y/n:") == "y":
                context = list(self.get_context)
            else:
                context = self.get_context_interactive()
        else:
            context = self.get_context_interactive()

        if context == None:
            print("Task Registration Failed -- No Context")
            return

        id = self.next_id()
        content = input("Content: ")
        if content == "q": return
        target = input("target date (Y.M.D):")
        if target == "q": return
        sol = input("super duper deadline date (Y.M.D):")
        if sol == "q": return
        
        t = Task()
        t.init_inner(id, content, target, sol, context)
        
        self.tasks.append(t)
        self.dump_tasks()

    def edit_task(self, id=None):
        strid = "!" if id==None else " "+str(id)+'!'
        print("\nEdit Task"+strid)
        print("<enter> to leave as-is")

        if id==None:
            id=input("ID: ")

        id = int(id)

        task = self.get_task_by_id(id)
        content = input("New Description: ")
        if content != "":
            task.set_content(content)
        target = input("New Target Date: ")
        if target != "":
            task.set_target(target)
        sol = input("New SOL Date: ")
        if sol != "":
            task.set_sol(sol)

    # watch out when we get network going
    def delete_task(self, id):
        task = self.get_task_by_id(id)
        self.tasks.remove(task)
        self.dump_tasks()

    def next_id(self):
        with open(self.next_id_file) as f:
            next_dict = yaml.load(f)

        id = next_dict["next_id"]

        # save to file
        next_dict["next_id"] = id + 1
        with open(self.next_id_file, 'w') as f:
            yaml.dump(next_dict, f)

        return id
        
        
    # deprecated but hanging around cuz set ops are cool
    def lowest_inactive_id(self):
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

    def finish_task(self, id, fin=None):
        id = int(id)

        if fin == None:
            fin = date.today()
        
        # dump to feedback
        task = self.get_task_by_id(id)
        if task == []:
            print("Failed to look up by id")
            return

        task.finished = fin
        with open(self.finished_file, 'a') as f:
            yaml.dump([task], f) # think it needsta be a list?
        self.tasks.remove(task)
        self.dump_tasks()

    def get_task_by_id(self, id):
        singleton = list(filter(lambda x: x.id == id, self.tasks))
        return singleton[0]

    def dump_tasks(self):
        with open(self.task_file, 'w') as f:
            yaml.dump(self.tasks, f)

    def dump_context_holder(self):
        with open(self.context_file, 'w') as f:
            yaml.dump(self.ch.contexts, f)

    def dump_context(self):
        if len(self.context) > 0:
            with open(self.current_context_file, 'w') as f:
                yaml.dump(self.context, f)
        elif os.path.exists(self.current_context_file):
                os.remove(self.current_context_file)
            
    def dump(self):
        self.dump_tasks()
        self.dump_context_holder()
        self.dump_context()
        

    # this will prob be piped to grep...
    def print_tasks(self):
        to_print = ""
        for task in self.tasks:
            to_print += "{0}    {1}\n".format(task.id, task.content)

        print(to_print)

    def print_task(self, id=None):
        if id == None:
            id = input("ID?: ")

        id = int(id)
        
        try:
            task = self.get_task_by_id(id)
        except IndexError:
            print("Bad task ID")

        print(yaml.dump(task))
        

    def get_finished(self):
        with open(self.finished_file) as f:
            finished_tasks = yaml.load(f)
            if len(finished_tasks) > 0:
                assert isinstance(finished_tasks[0], Task)
            return finished_tasks
        
    def print_finished(self):
        with open(self.finished_file) as f:
            print(f.read())

    def get_tasks_by_context(self):
        #try:
        #    main_context = self.context[0]
        #except IndexError:
        #    raise Exception("Context Not Set (in get_tasks_by_context())")
        
        #tasks = list(filter(lambda x: main_context in x.context, self.tasks))

        tasks = list(filter(
            functools.partial(
                Tasklist.match_task_context, self.context),
            self.tasks))


        return tasks
        
    def get_tasklist(self):
        if len(self.context) == 0:
            self.set_context()

        # get today's date
        today = datetime.now()

        # first just for primary context...
        #tasks = self.context.get_tasks() # deep list copy

        tasks = self.get_tasks_by_context()

        # for now, let all tasks in...
        #tasks = list(filter(lambda x: x.target < today, tasks))  # only consider current tasks
        #tasks.sort(key = lambda x: x.sol)  # sort based on SOL date
        tasks.sort(key = lambda x: x.urgency(today))

        return tasks

    # Allow more general contexts to match tasks of more specific contexts
    def match_task_context(contexts, task):
        task_contexts = task.context # list
        for tc in task_contexts:
            tcl = tc.split(".")
            for c in contexts:
                cl = c.split(".")
                if ContextHolder.match_context(cl, tcl):
                    return True

        return False

    
# moved to ContextHolder
#    def match_context(context, task_context):
#        """Take in task-specific and general contex
#        separated into strings, and see if a sublist matches"""
#        if len(task_context) > len(context):
#            return Tasklist.match_context(task_context[:-1], context)
#        else:
#            # don't match on metacontext alone:
#            if len(task_context) == 1:
#                return False
#            return task_context == context

    def print_tasklist(self):

        sorted_tasks = self.get_tasklist()

        print(functools.reduce(lambda x,y: x+y,
                               map(str, sorted_tasks),
                               ""))
        
