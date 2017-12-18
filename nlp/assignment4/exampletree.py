#!/usr/bin/env python3


class Node:
    def __init__(self, tag=None, children=None):
        self.tag = tag
        self.children = children if children else []

    def __nonzero__(self):
        return self.tag != 'kur'  # tags to be excluded

    def __eq__(self, other):
        return self.tag == other.tag and self.children == other.children

    def __str__(self):
        buf, out = [self], []
        while buf:
            # current level
            out.append(", ".join(str(node.tag) for node in buf))
            if any(node for node in buf):
                # add children
                buf = [subnode if subnode else Node()
                       for node in buf
                       for subnode in node.children]
            else:
                break
        return "\n".join(out)

    def __repr__(self):
        if not self:
            return "Node()"
        children_repr = ",".join(repr(child) for child in self.children)
        return "Node({.tag},[{}])".format(self, children_repr)

    def serialize(self):
        return repr(self).replace("Node", "").replace("()", "#")

    @staticmethod
    def deserialize(source):
        # don't use this in production
        return eval(source.replace("#", "()").replace("(", "Node("))


if __name__ == "__main__":
    root = Node(1, [Node(2, [Node(4)]), Node(3, [Node(5), Node(6)])])
    print(repr(root))
    print(root)
    source = root.serialize()
    root2 = Node.deserialize(source)
    print(repr(root2))
    print(root2)
    assert(root == root2)
