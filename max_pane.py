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


SHARE_OBJECT = 'max_pane_share.sublime-settings'

# ------


class ShareManager:
    """Exposes a list of window ids which currently contain maximized panes.
       Shared via an in-memory .sublime-settings file."""
    maxed_wnds = set([])
    previous = set([])

    @classmethod
    def check_and_submit(cls):
        if cls.maxed_wnds != cls.previous:
            cls.previous = cls.maxed_wnds
            s = sublime.load_settings(SHARE_OBJECT)
            s.set("maxed_wnds", list(cls.maxed_wnds))

    @classmethod
    def add(cls, id):
        cls.maxed_wnds.add(id)
        cls.check_and_submit()

    @classmethod
    def remove(cls, id):
        cls.maxed_wnds.discard(id)
        cls.check_and_submit()

# ------


class PaneManager:
    layouts = {}
    maxgroup = {}

    @staticmethod
    def isWindowMaximized(window):
        w = window
        if PaneManager.hasLayout(w):
            return True
        elif PaneManager.looksMaximized(w):
            return True
        return False

    @staticmethod
    def looksMaximized(window):
        w = window
        l = window.get_layout()
        c = l["cols"]
        r = l["rows"]
        if w.num_groups() > 1:
            if set(c + r) == set([0.0, 1.0]):
                return True
        return False

    @staticmethod
    def storeLayout(window):
        w = window
        wid = window.id()
        PaneManager.layouts[wid] = w.get_layout()
        PaneManager.maxgroup[wid] = w.active_group()

    @staticmethod
    def maxedGroup(window):
        wid = window.id()
        if wid in PaneManager.maxgroup:
            return PaneManager.maxgroup[wid]
        else:
            return None

    @staticmethod
    def popLayout(window):
        wid = window.id()
        l = PaneManager.layouts[wid]
        del PaneManager.layouts[wid]
        del PaneManager.maxgroup[wid]
        return l

    @staticmethod
    def hasLayout(window):
        wid = window.id()
        return wid in PaneManager.layouts

# ------


class MaxPaneCommand(sublime_plugin.WindowCommand):
    """Toggles pane maximization."""
    def run(self):
        w = self.window
        if PaneManager.isWindowMaximized(w):
            w.run_command("unmaximize_pane")
            ShareManager.remove(w.id())
        elif w.num_groups() > 1:
            ShareManager.add(w.id())
            w.run_command("maximize_pane")

# ------


class MaximizePaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        g = w.active_group()
        l = w.get_layout()
        PaneManager.storeLayout(w)
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
        w.set_layout(l)

# ------


class UnmaximizePaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        if PaneManager.hasLayout(w):
            w.set_layout(PaneManager.popLayout(w))
        elif PaneManager.looksMaximized(w):
            # We don't have a previous layout for this window
            # but it looks like it was maximized, so lets
            # just evenly distribute the layout.
            self.evenOutLayout()
        for view in w.views():
            view.erase_status('0_maxpane')

    def evenOutLayout(self):
        w = self.window
        w.run_command("distribute_layout")

# ------


class DistributeLayoutCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        l = w.get_layout()
        l["rows"] = self.distribute(l["rows"])
        l["cols"] = self.distribute(l["cols"])
        w.set_layout(l)

    def distribute(self, values):
        l = len(values)
        r = range(0, l)
        return [n / float(l - 1) for n in r]

# ------


class ShiftPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        w.focus_group((w.active_group() + 1) % w.num_groups())

# ------


class UnshiftPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        w.focus_group((w.active_group() - 1) % w.num_groups())

# ------


def sublime_text_synced(fun):
    def decorator(*args, **kwargs):
        sublime.set_timeout(lambda: fun(*args, **kwargs), 10)
    return decorator

# ------


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
        if sublime.load_settings(SHARE_OBJECT).get('block_max_pane'):
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
        if sublime.load_settings(SHARE_OBJECT).get('block_max_pane'):
            return

        w = view.window() or sublime.active_window()
        # Is the window currently maximized?
        if w and PaneManager.isWindowMaximized(w):
            # Is the active group the group that is maximized?
            if w.active_group() != PaneManager.maxedGroup(w):
                w.run_command("unmaximize_pane")
                w.run_command("maximize_pane")
