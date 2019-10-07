
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
thisdir = os.path.dirname(os.path.abspath(__file__))


import pytest
from unittest.mock import mock_open
#from mind.task import Task, Context, ContextHolder
from mind.tasklist import Tasklist, Filenames
from mind.task import Task, Context, ContextHolder
from mind.test.test_task import task_valid
from datetime import datetime
from abc import ABCMeta



class tasklist_test(metaclass=ABCMeta):
    pass
    















# create an instance and manually set load/dump file?
#   as fixtures!?

@pytest.fixture(scope="module")
def task_file():
    data="""- !!python/object:mind.task.Task
  content: text josh
  context:
  - closure.executive
  - valence.positive
  id: 1
  sol: 2019-12-31 00:00:00
  target: 2019-09-30 00:00:00
- !!python/object:mind.task.Task
  content: email chris osgood
  context:
  - closure.weeds.research
  id: 2
  sol: 2019-10-15 00:00:00
  target: 2019-09-24 00:00:00
- !!python/object:mind.task.Task
  content: asdf
  context: []
  id: 0
  sol: 2020.1.1
  target: 2019.1.1
- !!python/object:mind.task.Task
  content: hello dobby
  context:
  - valence.positive
  id: 3
  sol: 2020.11.22
  target: 2019.10.5"""

    tmpname = thisdir + "/tmp_task.yml"
    tmpfile = open(tmpname, 'w')
    tmpfile.write(data)
    tmpfile.close()

    yield tmpname

    os.remove(tmpname)



@pytest.fixture
def contextholder_file(scope="module"):
    data = """closure:
  executive: closure.executive
  reflective: closure.reflective
  social: closure.social
  weeds:
    coding: closure.weeds.coding
    food: closure.weeds.food
    hands: closure.weeds.hands
    job: closure.weeds.job
    maintenance: closure.weeds.maintenance
    political: closure.weeds.political
    research: closure.weeds.research
    voluntary: closure.weeds.voluntary
valence:
  negative: valence.negative
  positive: valence.positive
"""
    tmpname = thisdir + "/tmp_ch.yml"
    tmpfile = open(tmpname, 'w')
    tmpfile.write(data)
    tmpfile.close()

    yield tmpname

    os.remove(tmpname)


@pytest.fixture
def empty_context_file():
    tmpname = thisdir + "/tmp_ch.yml"
    os.remove(tmpname)
    return tmpname


@pytest.fixture
def empty_task_file():
    tmpname = thisdir + "/tmp_task.yml"
    os.remove(tmpname)
    return tmpname

@pytest.fixture
def empty_next_id_file():
    data = """next_id: 0"""
    tmpname = thisdir + "/tmp_next.yml"
    tmpfile = open(tmpname, 'w')
    tmpfile.write(data)
    tmpfile.close()

    yield tmpname

    os.remove(tmpname)




@pytest.fixture
def empty_finished_file():
    tmpname = thisdir + "/tmp_finished.yml"
    os.remove(tmpname)
    return tmpname


@pytest.fixture
def context_file():
    data = """- closure.weeds.research
- closure.reflective"""
    tmpname = thisdir + "/tmp_context.yml"
    tmpfile = open(tmpname, 'w')
    tmpfile.write(data)
    tmpfile.close()

    yield tmpname

    os.remove(tmpname)


@pytest.fixture
def next_id_file():
    data = """next_id: 4"""
    tmpname = thisdir + "/tmp_next.yml"
    tmpfile = open(tmpname, 'w')
    tmpfile.write(data)
    tmpfile.close()

    yield tmpname

    os.remove(tmpname)

@pytest.fixture
def finished_file():
    data = """- !!python/object:mind.task.Task
  content: done finished
  context:
  - valence.negative
  id: -1
  sol: 2020.11.22
  target: 2019.10.5
  finished: 2019.10.20"""
    tmpname = thisdir + "/tmp_fin.yml"
    tmpfile = open(tmpname, 'w')
    tmpfile.write(data)
    tmpfile.close()

    yield tmpname

    os.remove(tmpname)



# construction from yaml
#   call task tests??

def tasklist_valid(tl):
    assert isinstance(tl, Tasklist)
    if len(tl.tasks > 0):
        assert isinstance(tl.tasks[0], Task)
        assert task_valid(tl.tasks[0])
    assert isinstance(tl.context, Context)
    assert isinstance(tl.ch, ContextHolder)

def test_tasklist_from_yaml():
    fn = Filenames(tasks=task_file, contexts=contextholder_file,
                   next_id=next_id_file, finished=finished_file,
                   current_context=context_file())
    tasklist_valid(m)
    m = Tasklist(fn)
    assert len(m.tasks) == 4

    # manually set context
    m.set_context(["closure.weeds.research"])

    # get_tasklist
    gt = m.get_tasklist()
    assert gt == m.tasks[1:2]


# construction from input

def test_tasklist_from_input():
    fn = Filenames(tasks=empty_task_file, contexts=contextholder_file,
                   next_id=next_id_file, finished=empty_finished_file,
                   current_context=empty_context_file())

    m = Tasklist(fn)

def test_interactive_set_context(m):
    # set context interactively
    sys.stdin = mock_open(read_data="""valence.negative
closure.weeds.hands
f""")
    m.set_context()
    assert m.get_context() == ["valence.negative", "closure.weeds.hands"]
    
    sys.stdin = mock_open(read_data="""closure.executive
q""")
    m.set_context()
    assert m.get_context() == ["valence.negative", "closure.weeds.hands"]

    sys.stdin = mock_open(read_data="""f""")
    assert m.get_context() == []



def test_register_task(m):    
    # register task
    m.set_context("valence.positive")
    sys.stdin = mock_open(read_data="""y
test task
2019.8.1
2019.9.9""")
    m.register_task()

    next = m.next_id() - 1 # state whoops
    test = Task().init_inner(next, "test task", datetime(2019, 8, 1),
                             datetime(2019.9.9), ["valence.positive"])

    assert m.tasks[len(m.tasks)-1] == test


def test_register_task_quit(m):
    # register task
    m.set_context("valence.positive")
    old_tasks = list(m.tasks)
    sys.stdin = mock_open(read_data="""y
test task
2019.8.1
q""")

    assert old_tasks == m.tasks

    
    

    
    # finish task


@pytest.fixture(scope="module")
def a_tasklist():
    pass



# setting context




# querying context



# load context from file







# allocating IDs



# finishing tasks



# querying tasks


# dumping




# tasklist construction
#   can we do this in terms of the urgency function?
#   sort of outsource that decision from Tasklist class?
# relatedly, we should create an inner method that outputs a list of tasks, r/t
#   going straight to the string output!

def test_get_tasklist():
    




