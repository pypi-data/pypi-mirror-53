class Dereferencing:
    '''
    '''

    def __init__(self):
        self._derefers_to = []

    @property
    def derefers_to(self):
        return self._derefers_to

    @derefers_to.setter
    def derefers_to(self, p):
        self._derefers_to = p

