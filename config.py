# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from typing import List, Text  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from woofsheme import WoofScheme

# color stuff
woofcolors = WoofScheme()
woofcolors.get_from_json("{}/.config/qtile/colors.json".format(os.getenv("HOME")))

# config

mod = "mod4"
terminal = guess_terminal()

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show run"),
        desc="Spawn a command using a prompt widget"),
    Key([mod], "t", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in "123456"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1+shift+group letter = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(
            i.name,
            switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

group_names = [("code", {'layout': 'monadtall'}),
               ("wifi", {'layout': 'monadtall'}),
               ("box", {'layout':'monadtall'}),
               ("headset", {'layout': 'monadtall'}),
               ("comment", {'layout': 'monadtall'}),
               ("file-word", {'layout': 'monadtall'}),
               ("gamepad", {'layout': 'max'}),
               ("bone", {'layout': 'monadtall'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))


layouts = [
    layout.Columns(border_normal='#635b59',border_focus='#71d75f', margin=3),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    layout.Stack(border_normal='#635b59',border_focus='#71d75f', margin=3, num_stacks=2),
    layout.Floating(border_normal='#635b59',border_focus='#71d75f', margin=3),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(border_normal='#635b59',border_focus='#71d75f', margin=3),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Ubuntu Mono',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = woofcolors.fg,
                       background = woofcolors.power2
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = woofcolors.fg,
                       background = woofcolors.power2
                       ),
              widget.GroupBox(
                       font = "Font Awesome 5 Free Solid",
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = woofcolors.active,
                       inactive = woofcolors.inactive,
                       rounded = False,
                       highlight_color = woofcolors.power1,
                       highlight_method = "line",
                       this_current_screen_border = woofcolors.bg,
                       this_screen_border = woofcolors.power1,
                       other_current_screen_border = woofcolors.window_name,
                       other_screen_border = woofcolors.bg,
                       foreground = woofcolors.butter,
                       background = woofcolors.power2
                       ),
              widget.Prompt(
                       font = "Ubuntu Mono",
                       padding = 10,
                       foreground = woofcolors.group_name,
                       background = woofcolors.power1
                       ),
              widget.TextBox(
                  font= "Font Awesome 5 Free Solid",
                  text= "caret-right",
                  fontsize= 43,
                  padding=0,
                  foreground=woofcolors.power2
              ),
              widget.Sep(
                       linewidth = 0,
                       padding = 40,
                       ),
              widget.WindowName(
                       font="Ubuntu",
                       foreground = woofcolors.window_name,
                       padding = 0
                       ),

              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       ),
              widget.TextBox(
                       text = 'caret-left',
                       font="Font Awesome 5 Free Solid",
                       foreground = woofcolors.power2,
                       padding = 0,
                       fontsize = 43
                       ),
              widget.Systray(
                       background = woofcolors.power2,
                       padding = 5
                       ),
              widget.TextBox(
                       text = 'caret-left',
                       font="Font Awesome 5 Free Solid",
                       background = woofcolors.power2,
                       foreground = woofcolors.power1,
                       padding = 0,
                       fontsize = 43
                       ),
              widget.TextBox(
                       text = " 🖬",
                       foreground = woofcolors.group_name,
                       background = woofcolors.power1,
                       padding = 0,
                       fontsize = 14
                       ),
              widget.Memory(
                       foreground = woofcolors.group_name,
                       background = woofcolors.power1,
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       padding = 5
                       ),
              widget.TextBox(
                       text='caret-left',
                       font="Font Awesome 5 Free Solid",
                       background = woofcolors.power1,
                       foreground = woofcolors.power2,
                       padding = 0,
                       fontsize = 43
                       ),
            #   widget.TextBox(
            #            text = '',
            #            background = woofcolors.power1,
            #            foreground = woofcolors.power2,
            #            padding = 0,
            #            fontsize = 43
            #            ),
              widget.TextBox(
                      text = " Vol:",
                       foreground = woofcolors.group_name,
                       background = woofcolors.power2,
                       padding = 0
                       ),
              widget.Volume(
                       foreground = woofcolors.group_name,
                       background = woofcolors.power2,
                       padding = 5
                       ),
              widget.TextBox(
                       text='caret-left',
                       font="Font Awesome 5 Free Solid",
                       background = woofcolors.power2,
                       foreground = woofcolors.power1,
                       padding = 0,
                       fontsize = 43
                       ),
              widget.CurrentLayout(
                       foreground = woofcolors.group_name,
                       background = woofcolors.power1,
                       padding = 5
                       ),
              widget.TextBox(
                       text='caret-left',
                       font="Font Awesome 5 Free Solid",
                       background = woofcolors.power1,
                       foreground = woofcolors.power2,
                       padding = 0,
                       fontsize = 43
                       ),
              widget.Clock(
                       foreground = woofcolors.group_name,
                       background = woofcolors.power2,
                       format = "%A, %B %d - %H:%M "
                       ),
              ]


screens = [
    Screen(
        wallpaper='~/Pictures/wallpaper.jpg',
        wallpaper_mode='fill',
        top=bar.Bar(widgets_list,
            24,
            background=woofcolors.bg,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "WoofTile"
