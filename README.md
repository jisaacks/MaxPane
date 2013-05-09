## MaxPane

Easily maximize/unmaximize a pane without reseting your multi-pane setup.

Ever use a multi pane setup in Sublime Text and want to maximize a single pane for a bit, *and* be able to switch back to the multi pane layout again when done? *Without losing the positions all your files were in.* You know like how iTerm does.

*Then MaxPane is for you.*

So lets say you have this multi pane setup:

![dual pane](https://raw.github.com/jisaacks/MaxPane/3535650829f9bbb7df2d26428589b9bd47b13591/before.png)

and you want to maximize the active (right) pane for a sec.

Just press <kbd>cmd</kbd>+<kbd>shift</kbd>+<kbd>enter</kbd> and the active pane is now maximized:

![single pane](https://raw.github.com/jisaacks/MaxPane/3535650829f9bbb7df2d26428589b9bd47b13591/after.png)

Press <kbd>cmd</kbd>+<kbd>shift</kbd>+<kbd>enter</kbd> another time and its back:

![dual pane](https://raw.github.com/jisaacks/MaxPane/3535650829f9bbb7df2d26428589b9bd47b13591/before.png)

***It also works great with [Origami](https://github.com/SublimeText/Origami)!***

### Installation

This is a new project, so the only installation method is via `git clone`. I will be adding to [Package Control](http://wbond.net/sublime_packages/package_control) when I believe it is ready for prime time.

#### Issues

When exiting sublime, if a window has a pane maximized, the next time you open sublime, that pane will be stuck in maximized mode. The only way you will be able to get to your other hidden panes is to manually set the layout: **View > Layout**. This could easily be solved if there was a way to unmaximize all windows before quiting sublime. In fact if you exit via the command `window.run_command("exit")` then it does unmaximize all windows fixing the problem ( *this only works in ST3 because it relies on the new __on_window_command__ event.* ). Unfortunately I do not know of anyway to listen and execute code on the default way sublime quits. So for now you should manually unmaximize your panes before quiting. If anyone has any ideas on how to solve this issue I would love to hear them.
