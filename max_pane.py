import sublime, sublime_plugin

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
        w = window
        wid = window.id()
        return PaneManager.maxgroup[wid]

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
    def run(self):
        w = self.window
        if PaneManager.isWindowMaximized(w):
            w.run_command("unmaximize_pane")
        elif w.num_groups() > 1:
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
        r = range(0,l)
        return [n/float(l-1) for n in r]

# ------

class ShiftPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        w.focus_group(self.groupToMoveTo())

    def groupToMoveTo(self):
        w = self.window
        g = w.active_group()
        n = w.num_groups()-1
        if g == n:
            m = 0
        else:
            m = g + 1
        return m

# ------

class UnshiftPaneCommand(ShiftPaneCommand):
    def groupToMoveTo(self):
        w = self.window
        g = w.active_group()
        n = w.num_groups()-1
        if g == 0:
            m = n
        else:
            m = g - 1
        return m

# ------

class MaxPaneEvents(sublime_plugin.EventListener):
    def on_window_command(self, window, command_name, args):
        unmaximize_before = ["travel_to_pane","carry_file_to_pane",
            "clone_file_to_pane","create_pane","destroy_pane",
            "create_pane_with_file"]

        if command_name in unmaximize_before:
            window.run_command("unmaximize_pane")

        if command_name == "exit":
            # Un maximize all windows before exiting
            windows = sublime.windows()
            for w in windows:
                w.run_command("unmaximize_pane")

        return None

    def on_activated(self, view):
        w = view.window() or sublime.active_window()
        # Is the window currently maximized?
        if PaneManager.isWindowMaximized(w):
            # Is the active group the group that is maximized?
            if w.active_group() != PaneManager.maxedGroup(w):
                w.run_command("unmaximize_pane")
                w.run_command("maximize_pane")




