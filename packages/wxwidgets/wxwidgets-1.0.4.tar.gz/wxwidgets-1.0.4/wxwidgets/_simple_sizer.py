from wx import BoxSizer


class SimpleSizer(BoxSizer):
    _parent = None

    def __init__(self, parent, orient):
        super().__init__(orient)
        self._parent = parent

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._parent.SetSizer(self)