from day07 import Node, load


def run():
    Node.populate(load('day07.input'))
    return Node.find_root().name
