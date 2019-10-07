
#import task, network, front
from mind.task import Task, Context, ContextHolder
from mind.tasklist import Tasklist


def tasklist():
    m = Tasklist()
    #print(m.ch)
    #print(m.ch.valid("closure.executive"))
    #print(m.ch.valid("closure.weeds.bikes"))
    #print(m.ch.valid("closure.weeds.hands"))
    #print(m.ch.valid("closure.weeds"))

    #m.set_context()
    #m.dump()
    #m.register_task()
    #m.get_tasklist()
    #print("dumped")
    print(ContextHolder.match_context([],[]))
    print(ContextHolder.match_context(["closure"],["closure"]))
    print(ContextHolder.match_context(["closure","weeds"],["closure","weeds"]))
    print(ContextHolder.match_context(["closure","weeds","hands"],["closure","weeds"]))
    print(ContextHolder.match_context(["closure","weeds"],["closure","weeds","hands"]))
    print(ContextHolder.match_context(["closure","executive"],["closure","weeds","hands"]))

    print("Task")

    x = Task()
    x.init_inner(5, "", "2019.1.1", "2019.2.2", ["closure.weeds.coding", "valence.positive"])
    print(Tasklist.match_task_context([], x))
    print(Tasklist.match_task_context(["closure"], x))
    print(Tasklist.match_task_context(["closure.weeds"], x))
    print(Tasklist.match_task_context(["closure.executive"], x))
    print(Tasklist.match_task_context(["valence.positive"], x))
    print(Tasklist.match_task_context(["closure.executive", "valence.positive"], x))
    print(Tasklist.match_task_context(["closure.reflective", "valence.negative"], x))
    print(Tasklist.match_task_context(["closure.weeds.hands"], x))


def task():
    pass

def context():
    pass

def get_free_id():
    pass





def all():
    tasklist()
