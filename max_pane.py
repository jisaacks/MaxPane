"""
  DESCRIPTION ABOUT SUBLIME TEXT LAYOUTS:

  window.get_layout() and window.set_layout() aren't really documented
  in the API so I am making some notes here about how they work.

    * rows are the positions (from 0.0 to 1.0) that make
      up the horizontal lines around (sides of) views.

    * columns are the positions (from 0.0 to 1.0) that make
      up the vertical lines around (top/bottom of) views

    * cells are the 4 positions (left,top,right,bottom)
      that define the positions of each view

  ROWS:

  0.0        -----------------
             |    |          |
             |    |          |
  0.66       -----------------
             |    |          |
  1.0        -----------------

  COLUMNS:  0.0  0.3        1.0

  CELLS:

    ---------
    | 0 | 0 |
    |0 1|1 2|
    | 1 | 1 |
    ---------
    | 1 | 1 |
    |0 1|1 2|
    | 2 | 2 |
    ---------
"""
import sublime
import sublime_plugin


def sublime_text_synced(fun):
    # https://github.com/SublimeTextIssues/Core/issues/1785
    def decorator(*args, **kwargs):
        sublime.set_timeout(lambda: fun(*args, **kwargs), 10)
    return decorator


def set_layout_and_focus(window, layout):
    # https://github.com/SublimeTextIssues/Core/issues/2919
    active_group = window.active_group()
    window.set_layout(layout)
    window.focus_group(active_group)


class ShareManager:
    """Exposes a list of window ids which currently contain maximized panes.
       Shared via an in-memory .sublime-settings file."""
    maxed_wnds = set([])
    previous = set([])

    @classmethod
    def is_blocked(cls):
        return sublime.load_settings(
            'max_pane_share.sublime-settings').get('block_max_pane')

    @classmethod
    def check_and_submit(cls):
        if cls.maxed_wnds != cls.previous:
            cls.previous = cls.maxed_wnds
            sublime.load_settings('max_pane_share.sublime-settings').set(
                "maxed_wnds", list(cls.maxed_wnds))

    @classmethod
    def add(cls, id):
        cls.maxed_wnds.add(id)
        cls.check_and_submit()

    @classmethod
    def remove(cls, id):
        cls.maxed_wnds.discard(id)
        cls.check_and_submit()


class PaneManager:
    layouts = {}
    maxgroup = {}

    @classmethod
    def is_group_maximized(cls, window):
        return window.id() in cls.layouts or cls.looks_maximized(window)

    @staticmethod
    def looks_maximized(window):
        if window.num_groups() <= 1:
            return False

        layout = window.get_layout()
        return set(layout["cols"] + layout["rows"]) == set([0.0, 1.0])

    @classmethod
    def maximized_group(cls, window):
        return cls.maxgroup.get(window.id())

    @classmethod
    def store_layout(cls, window):
        wid = window.id()
        cls.layouts[wid] = window.get_layout()
        cls.maxgroup[wid] = window.active_group()

    @classmethod
    def pop_layout(cls, window):
        wid = window.id()
        cls.maxgroup.pop(wid, None)
        return cls.layouts.pop(wid, None)


class MaxPaneCommand(sublime_plugin.WindowCommand):
    """Toggles pane maximization."""
    def run(self):
        w = self.window
        if PaneManager.is_group_maximized(w):
            w.run_command("unmaximize_pane")
            ShareManager.remove(w.id())
        elif w.num_groups() > 1:
            ShareManager.add(w.id())
            w.run_command("maximize_pane")


class MaximizePaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        g = w.active_group()
        l = w.get_layout()
        PaneManager.store_layout(w)
        current_col = int(l["cells"][g][2])
        current_row = int(l["cells"][g][3])
        new_rows = []
        new_cols = []
        for index, row in enumerate(l["rows"]):
            new_rows.append(0.0 if index < current_row else 1.0)
        for index, col in enumerate(l["cols"]):
            new_cols.append(0.0 if index < current_col else 1.0)
        l["rows"] = new_rows
        l["cols"] = new_cols
        for view in w.views():
            view.set_status('0_maxpane', 'MAX')
        set_layout_and_focus(w, l)


class UnmaximizePaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        l = PaneManager.pop_layout(w)
        if l:
            set_layout_and_focus(w, l)
        elif PaneManager.looks_maximized(w):
            # We don't have a previous layout for this window
            # but it looks like it was maximized, so lets
            # just evenly distribute the layout.
            w.run_command("distribute_layout")
        for view in w.views():
            view.erase_status('0_maxpane')


class DistributeLayoutCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        l = w.get_layout()
        l["rows"] = self.distribute(l["rows"])
        l["cols"] = self.distribute(l["cols"])
        set_layout_and_focus(w, l)

    def distribute(self, values):
        l = len(values)
        r = range(0, l)
        return [n / float(l - 1) for n in r]


class ShiftPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        w.focus_group((w.active_group() + 1) % w.num_groups())


class UnshiftPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        w.focus_group((w.active_group() - 1) % w.num_groups())


class MaxPaneEvents(sublime_plugin.EventListener):
    UNMAXIMIZE_BEFORE = frozenset((
        "carry_file_to_pane",
        "clone_file_to_pane",
        "create_pane",
        "create_pane_with_file",
        "destroy_pane",
        "new_pane",
        "project_manager",
        "set_layout",
        "travel_to_pane"
    ))

    def on_window_command(self, window, command_name, args):
        if ShareManager.is_blocked():
            return

        if command_name in self.UNMAXIMIZE_BEFORE:
            window.run_command("unmaximize_pane")
            return

        if command_name == "exit":
            # Un maximize all windows before exiting
            windows = sublime.windows()
            for w in windows:
                w.run_command("unmaximize_pane")

    @sublime_text_synced
    def on_activated(self, view):
        if ShareManager.is_blocked():
            return

        w = view.window() or sublime.active_window()
        # Is the window currently maximized?
        if w and PaneManager.is_group_maximized(w):
            # Is the active group the group that is maximized?
            if w.active_group() != PaneManager.maximized_group(w):
                w.run_command("unmaximize_pane")
                w.run_command("maximize_pane")
