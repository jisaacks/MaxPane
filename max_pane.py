import sublime, sublime_plugin

# ------

class PaneManager:
    last_layout = False

# ------

class MaxPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        print("MAX PANING")
        w = self.window
        if PaneManager.last_layout:
            w.run_command("unmaximize_pane")
        else:
            w.run_command("maximize_pane")

# ------

class MaximizePaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        g = w.active_group()
        l = w.get_layout()
        PaneManager.last_layout = w.get_layout()
        current_col = l["cells"][g][2]
        current_row = l["cells"][g][3]
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
        w.set_layout(PaneManager.last_layout)
        PaneManager.last_layout = False