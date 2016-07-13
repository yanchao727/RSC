(_ROOT, _DEPTH, _BREADTH) = range(3)


class Tree:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, data={}, parent=None):
        node = TreeNode(identifier, data)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)
            self[identifier].set_parent(parent)
        return node

    def display(self, identifier, depth=_ROOT):
        children = self[identifier].children
        data = self[identifier].data
        if depth == _ROOT:
            print("{0}".format(identifier))
        else:
            print("\t"*depth, "{0}".format(identifier))

        depth += 1
        for child in children:
            self.display(child, depth)  # recursive call

    def processHTML(self, fileref, identifier, depth=_ROOT):
        # generate the tree structure in html.
        # the enclosing html should be included in the calling function

        fileref.write("<ul>")
        children = self[identifier].children
        name = self[identifier].data['name'] if self[identifier].data else identifier
        if depth == _ROOT:
            fileref.write("<li>" + "{0}".format(name) + "[" + identifier + "]</li>")
        else:
            fileref.write("<li>" + "{0}".format(name) + "[" + identifier + "]</li>")

        depth += 1
        for child in children:
            self.processHTML(fileref, child, depth)  # recursive call
        fileref.write("</ul>")

    def writeHTML(self, filename="chassisTree.html"):
        htmlfile = open(filename, 'w+')
        htmlfile.write("<html><body><h1>Tree</h1>")
        self.processHTML(htmlfile, "0")
        htmlfile.write("</body></html>")
        htmlfile.close()

    def traverse(self, identifier, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from
        # 'Essential LISP' by John R. Anderson, Albert T. Corbett,
        # and Brian J. Reiser, page 239-241
        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first

    def getPath(self, identifier):
        if self[identifier].parent is not None:
            return self[identifier].data["name"] + "_" + self.getPath(self[identifier].parent)
        else:
            return self[identifier].data['name'] if self[identifier].data else ""

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item


# Class represents Tree Node
class TreeNode:
    def __init__(self, identifier, data={}):
        self.__identifier = identifier
        self.__children = []
        self.__parent = None
        self.__data = data

    @property
    def identifier(self):
        return self.__identifier

    @property
    def children(self):
        return self.__children

    @property
    def parent(self):
        return self.__parent

    @property
    def data(self):
        return self.__data

    def add_child(self, identifier):
        self.__children.append(identifier)

    def set_parent(self, identifier):
        self.__parent = identifier
