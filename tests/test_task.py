
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import pytest
from mind.task import Task, Context, ContextHolder
from datetime import datetime
import yaml


# test tasks

ex_tasks = """- !!python/object:mind.task.Task
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


def task_valid(task):
    assert isinstance(task, Task)
    assert isinstance(task.id, int)
    assert isinstance(task.sol, datetime)
    assert isinstance(task.target, datetime)
    assert task.urgency() > -999
    assert t0.finished == None  # this input doesn't have it yet...
    


def test_task_load_yaml():
    tasklist = yaml.load(ex_tasks)
    t0 = tasklist[0]
    assert isinstance(t0, Task)
    assert t0.id == 1
    assert isinstance(t0.sol, datetime)
    assert t0.urgency() > -999
    #assert t0.finished == None  # this input doesn't have it yet...
    t2 = tasklist[2]
    assert t2.context == []

    

# this is a bit silly
# BUT recall, we write trivial tests so that we know when we've broken our code!

# loading
#   from yaml
#   from interactive
#     this will go in tasklist
# i.e. do the data types show up properly
# 


def test_context_persistence():
    pass

def test_context_task_aggregation():
    pass

def test_context_holder_persistence():
    pass

