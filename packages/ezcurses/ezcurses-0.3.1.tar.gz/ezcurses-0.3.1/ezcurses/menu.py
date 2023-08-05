class _Menu:

    def __init__(self, items, color=None, selected_color=None, selected=0,
                 exit_keys=None):
        color = color or ('white', 'black')
        if isinstance(color, str):
            color = (color, 'black')
        if isinstance(selected_color, str):
            selected_color = (selected_color, 'white')
        self._color = color
        self._selected_color = selected_color or tuple(list(color)[::-1])
        self.items = items
        self.selected = selected
        self.exit_keys = exit_keys or []
        self._size = (max(len(b) + 3 for _, b in items), len(items))
        self._choices = {k_v[0]: (i, k_v[1]) for i, k_v in enumerate(items)}

    def new_win(self, scr, orig=None):
        self._win = scr.new_win(orig=orig, size=self._size)
        self._scr = scr
        self._orig = orig or (0, 0)

    def draw(self, selected=None):
        if selected is not None:
            self.selected = selected
        self._scr.refresh()
        for i, key_msg in enumerate(self.items):
            if self.selected == i:
                color = self._selected_color
            else:
                color = self._color
            key, msg = key_msg
            if key is None:
                self._win.write('   {}'.format(msg), pos=(0, i), color=color)
            else:
                self._win.write('{}) {}'.format(key, msg), pos=(0, i),
                                color=color)
        self._win.move_cursor((0, self.selected or 0))
        self._win.refresh()

    def get_item(self, force=False):
        while True:
            self.draw()
            key = self._scr.getkey()
            if key is not None and key in self._choices:
                return self._choices[key][0]
            if key == 'DOWN':
                self.selected += 1
                self.selected = self.selected % len(self.items)
            elif key == 'UP':
                self.selected -= 1
                self.selected = self.selected % len(self.items)
            elif key == 'ENTER':
                return self.selected
            elif key == 'ESCAPE':
                if force:
                    continue
                return None
            elif key in self.exit_keys:
                return key
