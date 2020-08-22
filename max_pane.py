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


# With ST3 layouts and maximized groups are stored persistent in the session.
PERSIST_LAYOUTS = hasattr(sublime.Window, "settings")
if PERSIST_LAYOUTS:

    def is_editor_maximized(window):
        return window.settings().has("max_editor")

    def maximized_group(window):
        return window.settings().get("max_pane", {}).get("group")

    def active_layout(window):
        return window.layout()

    def has_stored_layout(window):
        return window.settings().has("max_pane")

    def pop_stored_layout(window):
        settings = window.settings()
        layout = settings.get("max_pane", {}).get("layout")
        settings.erase("max_pane")
        return layout

    def store_layout(window, layout, group):
        window.settings().set("max_pane", {"layout": layout, "group": group})


# ST2 doesn't provide a window settings API to store layouts persistent.
else:
    _store = {}

    def is_editor_maximized(window):
        return False

    def maximized_group(window):
        return _store.get(window.id(), {}).get("group")

    def active_layout(window):
        return window.get_layout()

    def has_stored_layout(window):
        return window.id() in _store

    def pop_stored_layout(window):
        try:
            return _store.pop(window.id()).get("layout")
        except KeyError:
            return None

    def store_layout(window, layout, group):
        _store[window.id()] = {"layout": layout, "group": group}


def is_group_maximized(window):
    return has_stored_layout(window) or looks_maximized(window)


def looks_maximized(window):
    if window.num_groups() < 2:
        return False

    layout = active_layout(window)
    return set(layout["cols"] + layout["rows"]) == set([0.0, 1.0])


def maximize_active_group(window):
    group = window.active_group()
    layout = active_layout(window)
    store_layout(window, layout, group)
    cells = layout["cells"]
    current_col = int(cells[group][2])
    current_row = int(cells[group][3])
    window.set_layout(
        {
            "rows": [
                0.0 if index < current_row else 1.0
                for index, row in enumerate(layout["rows"])
            ],
            "cols": [
                0.0 if index < current_col else 1.0
                for index, col in enumerate(layout["cols"])
            ],
            "cells": cells,
        }
    )
    window.focus_group(group)
    for view in window.views():
        view.set_status("0_maxpane", "MAX")
    ShareManager.add(window.id())


def unmaximize_group(window):
    layout = pop_stored_layout(window)
    if layout is None and looks_maximized(window):
        # We don't have a previous layout for this window
        # but it looks like it was maximized, so lets
        # just evenly distribute the layout.
        layout = active_layout(window)
        layout["rows"] = distribute(layout["rows"])
        layout["cols"] = distribute(layout["cols"])
    if layout:
        group = window.active_group()
        window.set_layout(layout)
        window.focus_group(group)
    for view in window.views():
        view.erase_status("0_maxpane")
    ShareManager.remove(window.id())


def distribute(values):
    num_values = len(values)
    return [n / float(num_values - 1) for n in range(0, num_values)]


class ShareManager:
    """Exposes a list of window ids which currently contain maximized panes.
       Shared via an in-memory .sublime-settings file."""

    maxed_wnds = set()
    previous = set()

    @classmethod
    def is_blocked(cls):
        return sublime.load_settings("max_pane_share.sublime-settings").get(
            "block_max_pane"
        )

    @classmethod
    def check_and_submit(cls):
        if cls.maxed_wnds != cls.previous:
            cls.previous = cls.maxed_wnds
            sublime.load_settings("max_pane_share.sublime-settings").set(
                "maxed_wnds", list(cls.maxed_wnds)
            )

    @classmethod
    def add(cls, id):
        cls.maxed_wnds.add(id)
        cls.check_and_submit()

    @classmethod
    def remove(cls, id):
        cls.maxed_wnds.discard(id)
        cls.check_and_submit()


class MaxEditorCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        return PERSIST_LAYOUTS

    def is_visible(self):
        return PERSIST_LAYOUTS

    def run(self, maximized=None):
        w = self.window
        s = w.settings()

        max_editor = s.get("max_editor")

        if maximized is True and max_editor is not None:
            return
        if maximized is False and max_editor is None:
            return

        if max_editor:
            # restore normal state from session
            w.set_menu_visible(max_editor.get("menu_visible", True))
            w.set_minimap_visible(max_editor.get("minimap_visible", True))
            w.set_sidebar_visible(max_editor.get("sidebar_visible", True))
            w.set_status_bar_visible(max_editor.get("status_bar_visible", True))
            w.set_tabs_visible(max_editor.get("tabs_visible", True))
            if not max_editor.get("group_maximized", False):
                unmaximize_group(w)
            s.erase("max_editor")

        else:
            # store current state in session
            group_maximized = is_group_maximized(w)
            s.set(
                "max_editor",
                {
                    "menu_visible": w.is_menu_visible(),
                    "minimap_visible": w.is_minimap_visible(),
                    "sidebar_visible": w.is_sidebar_visible(),
                    "status_bar_visible": w.is_status_bar_visible(),
                    "tabs_visible": w.get_tabs_visible(),
                    "group_maximized": group_maximized,
                },
            )
            w.set_menu_visible(False)
            w.set_minimap_visible(False)
            w.set_sidebar_visible(False)
            w.set_status_bar_visible(False)
            w.set_tabs_visible(False)
            if not group_maximized:
                maximize_active_group(w)


class MaxPaneCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        return not is_editor_maximized(self.window)

    def run(self):
        w = self.window
        if is_group_maximized(w):
            unmaximize_group(w)
        elif w.num_groups() > 1:
            maximize_active_group(w)


class MaximizePaneCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        return not is_editor_maximized(self.window)

    def run(self):
        maximize_active_group(self.window)


class UnmaximizePaneCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        return not is_editor_maximized(self.window)

    def run(self):
        unmaximize_group(self.window)


class MaxPaneEvents(sublime_plugin.EventListener):
    UNMAXIMIZE_BEFORE = frozenset(
        (
            "carry_file_to_pane",
            "clone_file_to_pane",
            "create_pane",
            "create_pane_with_file",
            "destroy_pane",
            "move_to_group",
            "move_to_neighbouring_group",
            "new_pane",
            "project_manager",
            "set_layout",
            "travel_to_pane",
        )
    )

    def on_window_command(self, window, command_name, args):
        if ShareManager.is_blocked():
            return

        if command_name in self.UNMAXIMIZE_BEFORE:
            unmaximize_group(window)
            return

        if PERSIST_LAYOUTS is False and command_name == "exit":
            for window in sublime.windows():
                unmaximize_group(window)

    @sublime_text_synced
    def on_activated(self, view):
        if ShareManager.is_blocked():
            return

        window = view.window() or sublime.active_window()
        # Is the window currently maximized?
        if window and is_group_maximized(window):
            # Is the active group the group that is maximized?
            if window.active_group() != maximized_group(window):
                unmaximize_group(window)
                maximize_active_group(window)


def plugin_loaded():
    # restore status bar indicator after startup
    if PERSIST_LAYOUTS:
        for window in sublime.windows():
            if is_group_maximized(window):
                for view in window.views():
                    view.set_status("0_maxpane", "MAX")
