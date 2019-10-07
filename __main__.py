

import sys
import mind.test as test
#from mind.network import Network
from mind.tasklist import Tasklist
import os

# Setup

# change wd to mind/
os.chdir(os.path.dirname(os.path.abspath(__file__)))



class Interactor:
    tasklist = Tasklist()
    #net = Network()


    # ooooh let's hold a str:func dict!
    funcs = {"register-task": tasklist.register_task,
             "edit-task": tasklist.edit_task,
             "show-task": tasklist.print_task,
             "set-context": tasklist.set_context,
             "list": tasklist.print_tasks,
             "list-finished": tasklist.print_finished,
             "finish-task": tasklist.finish_task,
             "delete-task": tasklist.delete_task,
             "links": None,
             "create-link": None, #net.add_edge_interactive,
             "tasklist": tasklist.print_tasklist,
             "delete-link": None,
             "get-context": tasklist.print_context,
             "test": test.tasklist}

    #print("lol")
    #print(funcs)
    
    def halp():
        print("'q' to exit")
        print(list(Interactor.funcs.keys()))

    # hack hack hack
    funcs["help"] = halp

    def interact():

        while True:
            x = input("> ")
            if x == "q":
                break
            x = x.split(" ")
            if len(x) > 1:
                Interactor.funcs[x[0]](*x[1:])
            else:
                try:
                    Interactor.funcs[x[0]]()
                except KeyError:
                    print("Not recognized...")
                    Interactor.halp()

        # on exit
        Interactor.tasklist.dump()
        #Interactor.net.dump()
                


# problem: i'd been assuming we'd be able to call all these methods on a mind object
# but some are network or test methods.
# try-catch lollllllll
#   nah that's a dangerous way of type checking
# does the function contain info on the class it comes from??
#   maybe! try method.__self__!
# nope, they register as functions when you pass them that way
# options
#   make CLI args more explicit
#   make all python entry points from the same scope
# is it easiest to just have functions defined here???
# I could mix n match
#   pass mind instance to all fxns
#   some naturally want that
#   some (defined here) ignore?
# wait a sec!!!
#   as long as we initialize mind in the Interactor body before we define
#   funcs, we can call things on the actual instances!!!



# Script

arglist = sys.argv[1:]
if arglist == []:
    Interactor.interact()
else:
    subcomm = arglist.pop(0)
    Interactor.funcs[subcomm](*arglist)
    
#if subcomm == "test":
#    Test.mind()
#else:
#    print("yikes")
