class Layout:
    '''
    Helps design a layout flow.
    '''

    def __init__(self, area, border=True):
        self._area = area
        self.w, self.h = self._area.max_size()
        self.rows = []
        self._wins = []
        self.border = border

    def __getitem__(self, item):
        return self.rows[item]

    def __iter__(self):
        yield from self.rows

    def _calc_height(self, num):
        return int((num / 12) * self.h)

    def _calc_width(self, num):
        return int((num / 12) * self.w)

    def add_row(self, height, sizes=None):
        sizes = sizes or [12]
        new = LayoutRow(self, height, sizes)
        self.rows.append(new)
        return new

    def draw(self):
        self._area.refresh()
        self._wins = []
        ht = 0
        for row in self.rows:
            ht2 = self._calc_height(row.height)
            row.draw((0, ht), (self.w, ht2), border=self.border)
            ht += ht2


class LayoutRow(Layout):
    '''
    A row in the layout.
    '''

    def __init__(self, layout, height, sizes):
        self._layout = layout
        self.sizes = sizes
        self.height = height
        self.columns = []

    @property
    def w(self):
        return self._layout.w

    @property
    def h(self):
        return self._layout.h

    def __getitem__(self, item):
        return self.columns[item]

    def __iter__(self):
        yield from self.columns

    def draw(self, orig, size, border=True):
        self.columns = []
        w, h = size
        x, y = orig
        for size in self.sizes:
            col_size = self._calc_width(size)
            col = self._layout._area.new_win(orig=(x, y), size=(col_size, h))
            if border:
                col.border()
            self.columns.append(col)
            col.refresh()
            x += col_size
