## MaxPane

Easily maximize/unmaximize a pane without resetting your multi-pane setup.

Ever used a multi pane setup in Sublime Text and want to maximize a single pane for a bit, *and* be able to switch back to the multi pane layout again when done?

*Then MaxPane is for you.*

It also works great with [BetterTabCycling](https://github.com/ahuff44/sublime-better-tab-cycling), [Origami](https://github.com/SublimeText/Origami) and [Distraction Free Window](https://github.com/aziz/DistractionFreeWindow#changing-layout)!

So lets say you have this multi pane setup:

![normal](https://user-images.githubusercontent.com/16542113/65072662-a304d900-d991-11e9-92a3-b5ab1b3396bd.png)

### Maximize Panes

Press <kbd>ctrl + k</kbd>, <kbd>ctrl + f</kbd> _(Linux/Windows)_ / <kbd>super + k</kbd>, <kbd>super + f</kbd> _(MacOS)_ to maximize the active (upper right) pane:

![max_pane](https://user-images.githubusercontent.com/16542113/65072721-bfa11100-d991-11e9-86b9-787081649aa0.png)

Press <kbd>ctrl + k</kbd>, <kbd>ctrl + f</kbd> _(Linux/Windows)_ / <kbd>super + k</kbd>, <kbd>super + f</kbd> _(MacOS)_ another time to return to the original state.


## Maximize Editor

Press <kbd>ctrl + k</kbd>, <kbd>ctrl + m</kbd> _(Linux/Windows)_ / <kbd>super + k</kbd>, <kbd>super + m</kbd> _(MacOS)_ to hide everything but the active pane.

![max_editor](https://user-images.githubusercontent.com/16542113/65072758-cf205a00-d991-11e9-8b53-33942e645edb.png)

Press <kbd>ctrl + k</kbd>, <kbd>ctrl + m</kbd> _(Linux/Windows)_ / <kbd>super + k</kbd>, <kbd>super + m</kbd> _(MacOS)_ another time to return to the original state.


## Switch Panes

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
