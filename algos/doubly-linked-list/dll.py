class LLNode:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None


class Deque:
    def __init__(self):
        self.top = None
        self.bottom = None

    def push(self, item):
        """
        push the object onto the top of the stack
        """
        node = LLNode(item)
        if self.top is None:
            self.top = node
            self.bottom = node
        else:
            self.top.prev = node
            node.next = self.top
            self.top = node


    def push_oldest(self, item):
        """
        push the object below the bottom of the stack
        """
        node = LLNode(item)
        if self.bottom is None:
            self.top = node
            self.bottom = node
        else:
            self.bottom.next = node
            node.prev = self.bottom
            self.bottom = node


    def pop(self):
        """
        pop the newest object
        """
        rtn = None
        if self.top is not None:
            rtn = self.top.val
            if self.bottom == self.top:
                self.bottom = self.top = None
            else:
                self.top = self.top.next

        return rtn


    def pop_oldest(self):
        """
        pop the oldest object
        """
        rtn = None
        if self.bottom is not None:
            rtn = self.bottom.val
            if self.bottom == self.top:
                self.top = self.bottom = None
            else:
                self.bottom = self.bottom.prev

        return rtn


x = Deque()
x.push(1)
x.push(2)
x.push(3)
x.push_oldest(0)
assert x.pop() == 3
assert x.pop() == 2
assert x.pop_oldest() == 0
assert x.pop_oldest() == 1
assert x.pop() == None
assert x.pop_oldest() == None
print("ok")
