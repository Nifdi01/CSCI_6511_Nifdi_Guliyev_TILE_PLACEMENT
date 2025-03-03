class Arc:
    def __init__(self, n1, n2):
        """
        Initialize an Arc with two Node objects.
          - n1: the left node.
          - n2: the right node.
        """
        assert n1 is not None, "n1 must not be None"
        assert n2 is not None, "n2 must not be None"
        self.n1 = n1
        self.n2 = n2

    def left(self):
        """Return the left node."""
        return self.n1

    def right(self):
        """Return the right node."""
        return self.n2

    @classmethod
    def arc_create(cls, n):
        """
        Creates an Arc from a Node 'n' and its parent.
        Returns Arc(n, n.parent).
        """
        return cls(n, n.parent)

    def __eq__(self, other):
        """Check equality: Two Arcs are equal if their left and right nodes are equal."""
        if other is None:
            return False
        if self is other:
            return True
        if not isinstance(other, Arc):
            return False
        return self.n1 == other.n1 and self.n2 == other.n2