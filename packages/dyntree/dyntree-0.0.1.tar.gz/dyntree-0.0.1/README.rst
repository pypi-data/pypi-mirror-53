==========================
dyntree
==========================

Provides possibility to create and manage tree built by id and parent for every node.
Insert's operations can be unordered, you can insert parent node after child node.
Finalize method will reorder the structure for you.

Install
=======

Use pip::

   pip install dyntree

Usage
=====

See the example.

Code::

    from dyntree import DynTree

    t1 = DynTree()
    t1.insert(1, 1)
    t1.insert(2, 2)
    t1.insert(11, 11, 2)
    t1.insert(30, 30, 20)
    t1.insert(20, 20, 2)
    t1.insert(13, 13, 15)
    t1.insert(15, 15)
    t1.finalize()

Result::

    {
        "1": {
            "value": 1,
            "parent": null,
            "children": {}
        },
        "2": {
            "value": 2,
            "parent": null,
            "children": {
                "11": {
                    "value": 11,
                    "parent": 2,
                    "children": {}
                },
                "20": {
                    "value": 20,
                    "parent": 2,
                    "children": {
                        "30": {
                            "value": 30,
                            "parent": 20,
                            "children": {}
                        }
                    }
                }
            }
        },
        "15": {
            "value": 15,
            "parent": null,
            "children": {
                "13": {
                    "value": 13,
                    "parent": 15,
                    "children": {}
                }
            }
        }
    }

Visit::

    for idx, val in t1.items():
        print('idx: %s, value: %s' % (idx, val))

    idx: 1, value: 1
    idx: 2, value: 2
    idx: 2.1, value: 11
    idx: 2.2, value: 20
    idx: 2.2.1, value: 30
    idx: 3, value: 15
    idx: 3.1, value: 13

