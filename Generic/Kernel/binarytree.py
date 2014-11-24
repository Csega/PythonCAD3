class BinaryTree(object):
    """
        generic tree binary structure object
    """    
    def __init__(self):
        self.__tree = EmptyNode()
    
    def __repr__(self):
        return str(self.__tree)
    
    def lookUp(self, key):
        return self.__tree.lookUp(key)
    
    def insert(self, key, value):
        self.__tree = self.__tree.insert(key, value)

class EmptyNode(object):
    """
        empty Node
    """
    def __repr__(self):
        return '*'
    
    def lookUp(self, key):
        return None
    
    def insert(self, key, value):
        return BinaryNode(self, key, value, self)
    
class BinaryNode(object):
    """
        this class rappresent a binary node
    """
    def __init__(self, left, key, value, right):
        self.key,  self.data  = key, value
        self.left, self.right = left, right
    
    def lookUp(self, key):
        """
            look up at the value
        """
        if self.key == key:
            return self.data
        elif self.key > key:
            return self.left.lookUp(key)
        else:
            return self.right.lookUp(key)
    
    def insert(self, key, value):
        """
            insert a new value at the node
        """
        if self.key == key:
            self.data = value
        elif self.key > key:
            self.left = self.left.insert(key, value)
        elif self.key < key:
            self.right = self.right.insert(key, value)
        return self
    
    def __repr__(self):
        return '(%s,%s,%s,%s)' % (str(self.left), str(self.key),  str(self.data), str(self.right)


def testBinaryTree():
    x = BinaryTree()
    x.insert('root', "1")
    x.insert('layer_1', "3")
    x.insert('layer_2', "2")   
    print("-->", x.lookUp('layer_1'))
    print("-->%s" % str(x))

if __name__ == '__main__':    
    testBinaryTree()
