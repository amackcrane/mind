

import sys
from mind.test import Test
from mind.network import Network
from mind.mind import Mind
import os

# Setup

# change wd to mind/
os.chdir(os.path.dirname(os.path.abspath(__file__)))



class Interactor:
    mind = Mind()
    net = Network()
    test = Test()


    # ooooh let's hold a str:func dict!
    funcs = {"register-task": mind.register_task,
             "set-context": mind.set_context,
             "list": None,
             "finish-task": None,
             "delete-task": None,
             "links": None,
             "create-link": net.add_edge_interactive,
             "tasklist": mind.get_tasklist,
             "delete-link": None,
             "test": Test.mind}

    #print("lol")
    #print(funcs)
    
    def halp():
        print("'q' to exit")
        print(list(Interactor.funcs.keys()))

    # hack hack hack
    funcs["help"] = halp

    def interact():

        while True:
            x = input(">")
            if x == "q":
                break
            try:
                x = x.split(" ")
                if len(x) > 1:
                    Interactor.funcs[x[0]](x[1:])
                else:
                    Interactor.funcs[x[0]]()
            except Exception:
                print("Not recognized...")
                Interactor.halp()
                


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
try:
    subcomm = arglist.pop()
    Interactor.funcs[subcomm]()
except IndexError:
    Interactor.interact()

#if subcomm == "test":
#    Test.mind()
#else:
#    print("yikes")
