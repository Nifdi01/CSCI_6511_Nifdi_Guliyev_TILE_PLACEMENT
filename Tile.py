class Tile:
    def __init__(self, val, lay, name):
        """
        Initialize a Tile with:
          - val: list of characters representing the tile's value
          - lay: list of characters representing the tile's layout
          - name: a string for the layout name
          
        The domain is set to ['O', 'E', 'F'] by default.
        """
        self.value = val
        self.layout = lay
        self.domain = ['O', 'E', 'F']
        self.layoutName = name

    def __str__(self):
        # Build a string similar to the Java toString() method.
        result = "Value: " + str(self.value) + " Layout: " + str(self.layout) + " " + self.layoutName
        return result