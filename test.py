
#import task, network, front
from mind.task import Task, Context, ContextHolder
from mind.mind import Mind



class Test:

    def mind():
        m = Mind()
        print(m.ch)
        print(m.ch.valid("closure.executive"))
        print(m.ch.valid("closure.weeds.bikes"))
        print(m.ch.valid("closure.weeds.hands"))
        print(m.ch.valid("closure.weeds"))

        #m.set_context()
        #m.dump()
        #m.register_task()
        #m.get_tasklist()
        print("dumped")
        
        
    def task():
        pass

    def context():
        pass

    def get_free_id():
        pass

