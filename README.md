## MaxPane

Easily maximize/unmaximize a pane without resetting your multi-pane setup.

Ever use a multi pane setup in Sublime Text and want to maximize a single pane for a bit, *and* be able to switch back to the multi pane layout again when done? *Without losing the positions all your files were in.* You know like how iTerm does.

*Then MaxPane is for you.*

So lets say you have this multi pane setup:

![dual pane](https://raw.github.com/jisaacks/MaxPane/3535650829f9bbb7df2d26428589b9bd47b13591/before.png)

and you want to maximize the active (top left) pane for a sec.

Just press <kbd>cmd + shift + enter</kbd> and the active pane is now maximized:

![single pane](https://raw.github.com/jisaacks/MaxPane/3535650829f9bbb7df2d26428589b9bd47b13591/after.png)

Press <kbd>cmd + shift + enter</kbd> another time and its back:

![dual pane](https://raw.github.com/jisaacks/MaxPane/3535650829f9bbb7df2d26428589b9bd47b13591/before.png)

***It also works great with [BetterTabCycling](https://github.com/ahuff44/sublime-better-tab-cycling), [Origami](https://github.com/SublimeText/Origami) and [Distraction Free Window](https://github.com/aziz/DistractionFreeWindow#changing-layout)!***


### Switch Panes

MacOS users can switch panes with the key bindings:

<kbd>cmd + ctrl + ←</kbd> - focus previous pane

<kbd>cmd + ctrl + →</kbd> - focus next pane


#### Sublime Text 2

Windows / Linux users need to setup their own key bindings.

The following examples show possible key bindings to imitate Sublime Text 3 behaviour.

_User/Default (Linux).sublime-keymap:_

```JS
    { "keys": ["ctrl+k", "ctrl+left"], "command": "unshift_pane" },
    { "keys": ["ctrl+k", "ctrl+right"], "command": "shift_pane" },
```

_User/Default (OSX).sublime-keymap:_

```JS
    { "keys": ["super+k", "super+left"], "command": "unshift_pane" },
    { "keys": ["super+k", "super+right"], "command": "shift_pane" },
```

_User/Default (Windows).sublime-keymap:_

```JS
    { "keys": ["ctrl+k", "ctrl+left"], "command": "unshift_pane" },
    { "keys": ["ctrl+k", "ctrl+right"], "command": "shift_pane" },
```


#### Sublime Text 3 

You can switch panes with the built-in key bindings provided by Sublime Text 3 out of the box:

**Linux/Windows**

<kbd>ctrl + k</kbd>, <kbd>ctrl + ←</kbd> - focus previous pane

<kbd>ctrl + k</kbd>, <kbd>ctrl + →</kbd> - focus next pane

**MacOS**

<kbd>super + k</kbd>, <kbd>super + ←</kbd> - focus previous pane

<kbd>super + k</kbd>, <kbd>super + →</kbd> - focus next pane

If you want to modify them, you can look for the `focus_neighboring_group` in...

_Default/Default (Linux).sublime-keymap:_

```JS
    { "keys": ["ctrl+k", "ctrl+left"], "command": "focus_neighboring_group", "args": {"forward": false} },
    { "keys": ["ctrl+k", "ctrl+right"], "command": "focus_neighboring_group" },
```

_Default/Default (OSX).sublime-keymap:_

```JS
    { "keys": ["super+k", "super+left"], "command": "focus_neighboring_group", "args": {"forward": false} },
    { "keys": ["super+k", "super+right"], "command": "focus_neighboring_group" },
```

_Default/Default (Windows).sublime-keymap:_

```JS
    { "keys": ["ctrl+k", "ctrl+left"], "command": "focus_neighboring_group", "args": {"forward": false} },
    { "keys": ["ctrl+k", "ctrl+right"], "command": "focus_neighboring_group" },
```

**Deprecation Notice**

The built-in `focus_neighboring_group` command replaces both `shift_pane` and `unshift_pane`. Therefore they are provided for compatibility with existing key bindings only and might be disabled for use in Sublime Text 3 in a future release.


### Installation

Install via [Package Control](http://wbond.net/sublime_packages/package_control)
