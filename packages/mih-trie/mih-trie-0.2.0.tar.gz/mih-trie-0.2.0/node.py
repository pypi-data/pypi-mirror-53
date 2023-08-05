# encoding: utf-8

class Node(object):


    def __init__(self, parent=None, key=None):

        self.parent   = parent
        self.key      = key
        self.value    = 0
        self.children = {}
