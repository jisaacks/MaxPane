import sublime, sublime_plugin

# ------

class PaneManager:
    last_layout = False

# ------

class MaxPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        if PaneManager.last_layout:
            w.run_command("unmaximize_pane")
        elif w.num_groups() > 1:
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
        if PaneManager.last_layout:
            w.set_layout(PaneManager.last_layout)
        PaneManager.last_layout = False

# ------

class ShiftPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        if PaneManager.last_layout:
            maximize = True
            w.run_command("unmaximize_pane")
        g = w.active_group()
        n = w.num_groups()-1
        if g == n:
            m = 0
        else:
            m = g + 1
        w.focus_group(m)
        if maximize:
            w.run_command("maximize_pane")

# ------

class UnshiftPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        w = self.window
        if PaneManager.last_layout:
            maximize = True
            w.run_command("unmaximize_pane")
        g = w.active_group()
        n = w.num_groups()-1
        if g == 0:
            m = n
        else:
            m = g - 1
        w.focus_group(m)
        if maximize:
            w.run_command("maximize_pane")

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
