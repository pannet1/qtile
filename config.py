import os
import json
import subprocess
from typing import List, Text

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import qtile
from libqtile import hook
from pywal import wallpaper

with open("{}/.config/qtile/config/settings.json".format(os.getenv("HOME"))) as file:
    settings = json.load(file)

looks: dict = settings["looks"]
display: dict = settings["display"]

with open("{}/.config/qtile/config/colors.json".format(os.getenv("HOME"))) as file:
    colors_json = json.load(file)

special_clrs = colors_json['special']
clrs = colors_json['colors']
wallpaper = colors_json["wallpaper"]

colors = {
    "bg": special_clrs['background'],
    "fg": special_clrs["foreground"], 
    "current_screen_tab": clrs['color1'], 
    "power1": clrs["color5"], 
    "power2": clrs["color6"], 
    "active": clrs["color13"], 
    "inactive": clrs["color7"], 
    "window_name": special_clrs["foreground"]
}

mod = "mod4"
terminal = "xfce4-terminal"

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

groups = [Group(i) for i in "123456780"]

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
               ("tv", {'layout' : 'max'}),
               ("bone", {'layout': 'monadtall'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))


layout_theme = {"border_width": 2,
                "margin": looks['border-margin'],
                "border_focus": colors['power1'],
                "border_normal": colors['power2'],
                }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font='JetBrains Mono',
    fontsize=11,
    padding=3,
)
extension_defaults = widget_defaults.copy()

widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors["fg"],
                    #    background = colors["power2"]
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors["fg"],
                    #    background = colors["power2"]
                       ),
              widget.GroupBox(
                       font = looks["caret_font"],
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors["active"],
                       inactive = colors["inactive"],
                       rounded = False, 
                       highlight_method = "line",
                       highlight_color = colors["bg"],
                       this_current_screen_border = colors["current_screen_tab"],
                       this_screen_border = colors["power1"],
                       other_current_screen_border = colors["window_name"],
                       other_screen_border = colors["bg"],
                       foreground = colors["fg"],
                    #    background = colors["power2"]
                       ),
              widget.Prompt(
                       padding = 11,
                       foreground = colors["power1"],
                    #    background = colors["power1"]
                       ),
            #   widget.TextBox(
            #       font= looks["caret_font"],
            #       text= "caret-right",
            #       fontsize= looks["caret_font_size"],
            #       padding=0,
            #       foreground=colors["power2"]
            #   ),
              widget.Sep(
                       linewidth = 0,
                       padding = 40,
                       ),
              widget.WindowName(
                       font="JetBrains Mono",
                       foreground = colors["window_name"],
                       padding = 0
                       ),

              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       ),
            #   widget.TextBox(
            #            text = 'caret-left',
            #            font=looks["caret_font"],
            #            foreground = colors["power2"],
            #            padding = 0,
            #            fontsize = looks["caret_font_size"]
            #            ),
              widget.Systray(
                    #    background = colors["power2"],
                       foreground = colors["power2"],
                       padding = 10
                       ),
              widget.Sep(
                  linewidth=0,
                  padding = 12,
              ),
            #   widget.TextBox(
            #            text = 'grip-lines-vertical',
            #            font = looks["caret_font"],
            #            foreground = colors["fg"],
            #            fontsize=20
            #            ),
              widget.Sep(
                  linewidth=0,
                  padding = 5,
              ),
              widget.TextBox(
                       text = "microchip",
                       font=looks["caret_font"],
                       foreground = colors["power1"],
                    #    background = colors["power1"],
                       padding = 0,
                       fontsize = 11
                       ),
              widget.Memory(
                       foreground = colors["power1"],
                    #    background = colors["power1"],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('xfce4-terminal' + ' -e htop')},
                       padding = 5
                       ),
            #   widget.TextBox(
            #            text='caret-left',
            #            font=looks["caret_font"],
            #            background = colors["power1"],
            #            foreground = colors["power2"],
            #            padding = 0,
            #            fontsize = looks["caret_font_size"]
            #            ),
            #   widget.TextBox(
            #            text = '',
            #            background = colors["power1"],
            #            foreground = colors["power2"],
            #            padding = 0,
            #            fontsize = looks["caret_font_size"]
            #            ),
              widget.Sep(
                linewidth = 0,
                padding = 6,
                ),
              widget.TextBox(
                foreground = colors["power2"],
                text="signal",
                font="Font Awesome 5 Free Solid"
              ),
              widget.Net(
                       foreground = colors["power2"],
                       format = '{down}',
                       ),

              widget.Sep(
                  linewidth = 0,
                  padding = 6,
              ),
              widget.TextBox(
                       text = "volume-off",
                       font = "Font Awesome 5 Free Solid",
                       foreground = colors["power1"],
                    #    background = colors["power2"],
                       fontsize = 14,
                       padding = 0
                       ),
              widget.Volume(
                       foreground = colors["power1"],
                    #    background = colors["power2"]
                       ),
            #   widget.TextBox(
            #            text='caret-left',
            #            font=looks["caret_font"],
            #         #    background = colors["power2"],
            #            foreground = colors["power1"],
            #            padding = 0,
            #            padding_bottom = 100,
            #            fontsize = looks["caret_font_size"]
            #            ),
              widget.Sep(
                linewidth = 0,
                padding = 6,
                ),
              widget.TextBox(
                foreground = colors["power2"],
                text="th-large",
                font="Font Awesome 5 Free Solid"
              ),
              widget.CurrentLayout(
                       foreground = colors["power2"],
                    #    background = colors["power1"],
                       padding = 5
                       ),
            #   widget.TextBox(
            #            text='caret-left',
            #            font=looks["caret_font"],
            #         #    background = colors["power1"],
            #            foreground = colors["power2"],
            #            padding = 0,
            #            fontsize = looks["caret_font_size"]
            #            ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       ),
              widget.TextBox(foreground = colors["power1"],
                text="calendar-alt",
                font="Font Awesome 5 Free Solid"),
              widget.Clock(
                       foreground = colors["power1"],
                    #    background = colors["power2"],
                       format = "%A, %B %d - %H:%M "
                       ),
              widget.QuickExit(default_text = 'power-off',
                                font='Font Awesome 5 Free Solid', 
                                fontsize=11, 
                                foreground=colors['power2'])
              ]

screen = Screen(
                wallpaper=wallpaper,
                wallpaper_mode='fill',
                top=bar.Bar(widgets_list,
                    int(looks['panel-size']),
                    background=colors["bg"],
                    opacity = float(looks['panel-opacity']),
                    margin = looks['border-margin'],
                ),
            )

screens = []

i = 0

for i in range(display["screen-count"]):
    screens.append(screen)

# Drag floating layouts.
mouse = [
    Drag([mod], "Button3", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button1", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(**layout_theme, float_rules=[
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

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

@hook.subscribe.startup
def start():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/start.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.


# ^ dont care about those. I want woof tile! :triumph:

wmname = "WoofTile"
