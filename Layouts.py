class Layouts:
    @staticmethod
    def getEl(option):
        """
        Returns a list of 16 characters representing the EL layout for the given option.
        Option 0: indices [4, 12, 8, 0, 1, 2, 3] are '1'
        Option 1: indices [0, 1, 2, 3, 7, 11, 15] are '1'
        Option 2: indices [3, 7, 11, 15, 14, 13, 12] are '1'
        Option 3: indices [15, 14, 13, 12, 8, 4, 0] are '1'
        All other positions are set to '0'.
        """
        elLayout = ['0'] * 16
        if option == 0:
            for i in [4, 12, 8, 0, 1, 2, 3]:
                elLayout[i] = '1'
        elif option == 1:
            for i in [0, 1, 2, 3, 7, 11, 15]:
                elLayout[i] = '1'
        elif option == 2:
            for i in [3, 7, 11, 15, 14, 13, 12]:
                elLayout[i] = '1'
        elif option == 3:
            for i in [15, 14, 13, 12, 8, 4, 0]:
                elLayout[i] = '1'
        return elLayout

    @staticmethod
    def getFull():
        """
        Returns a full layout (all positions set to '1').
        """
        return ['1'] * 16

    @staticmethod
    def getOuter():
        """
        Returns an outer layout where the positions:
        0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15 are set to '1',
        and the remaining positions are set to '0'.
        """
        outerLayout = ['0'] * 16
        for i in [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15]:
            outerLayout[i] = '1'
        return outerLayout

    @staticmethod
    def getInitialLayout():
        """
        Returns the initial layout, which is identical to the full layout.
        """
        return ['1'] * 16