class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def print_tree(self):
        if self.left:
            self.left.print_tree()
        print( self.data)
        if self.right:
            self.right.print_tree()

if __name__ == "__main__":
    root = Node(4)
    root.insert(6)
    root.insert(14)
    root.insert(2)
    root.insert(5)
    root.insert(9)
    root.print_tree()