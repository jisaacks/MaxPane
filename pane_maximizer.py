import sublime, sublime_plugin

# ------

class PaneManager:
    last_layout = False
    view_positions = []

# ------

class PaneMaximizerCommand(sublime_plugin.WindowCommand):
    def run(self):
        print("PMC")
        w = self.window
        if w.num_groups() > 1:
            w.run_command("maximize_pane")
        elif PaneManager.last_layout:
            w.run_command("unmaximize_pane")

# ------

class MaximizePaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        print("MAX")
        w = self.window

        if w.num_groups() == 1:
            print("exiting")
            return False
            exit()

        PaneManager.last_layout = w.get_layout()

        new_layout = {
            'rows': [0.0,1.0],
            'cols': [0.0,1.0],
            'cells': [[0, 0, 1, 1]]
        }

        PaneManager.view_positions = []
        for view in w.views():
            group, index = w.get_view_index(view)
            PaneManager.view_positions.append([view, group, index])

        w.set_layout(new_layout)

# ------

class UnmaximizePaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        print("MIN")
        w = self.window

        last_layout = PaneManager.last_layout
        PaneManager.last_layout = False
        active_view = w.active_view()
        if last_layout:
            # print(PaneManager.view_positions)

            # for group, indexes in PaneManager.views_by_groups

            w.set_layout(last_layout)

            for positions in PaneManager.view_positions:
                w.set_view_index(*positions)

            PaneManager.view_positions = []

            w.focus_view(active_view)