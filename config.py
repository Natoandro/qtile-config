# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage

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

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger
import subprocess
from spotify import Spotify
from custom_widgets import WindowName

subprocess.Popen(["compton"])
subprocess.Popen(["xscreensaver", "--no-spash"])
# subprocess.Popen(["qbittorrent"])
# subprocess.Popen(["slack"])

mod = "mod4"
alt = "mod1"

myPrimaryMenu = 'rofi -modi "drun,run" -show drun -show-icons'
mySecondaryMenu = "dmenu_run -fn 'JetBrains Mono-10' -lr 1.5 -p 'Run:'"
terminal = guess_terminal()
myFileManager = f"{terminal} -e vifm"
myFileBrowser = "rofi -show filebrowser"
myWindowSwitcher = 'rofi -modi "window,windowcd" -show window -show-icons'
myWindowSwitcherInGroup = 'rofi -modi "window,windowcd" -show windowcd -show-icons'

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "F1", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control", "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Mine
    Key([mod], "r", lazy.spawn(myPrimaryMenu), desc="My primary menu"),
    Key([mod], "d", lazy.spawn(mySecondaryMenu), desc="DMenu"),
    Key([mod], "e", lazy.spawn(myFileManager), desc="File Manager"),
    Key([mod, "shift"], "e", lazy.spawn(myFileBrowser), desc="File Browser"),
    Key([mod, "control"], "Tab", lazy.spawn(myWindowSwitcher), desc="Window switcher"),
    Key([alt], "Tab", lazy.spawn(myWindowSwitcherInGroup), desc="Window swhitcher"),

    Key([mod], "bracketright", lazy.layout.grow()),
    Key([mod], "bracketleft", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    # Key([mod, "shift"], "r", lazy.layout.reset()),
    Key([mod, "shift"], "space", lazy.layout.flip()),
    Key([mod, "shift"], "Left", lambda qtile: qtile.current_window.toscreen((qtile.current_screen.index - 1) % qtile.num_screens())),
    # Key([mod, "alt"], "h", lazy.window.toscreen(-1)),
    Key([mod, "shift"], "Right", lazy.window.toscreen(1)),

    Key([mod], "f", lazy.window.toggle_floating()),
    Key([mod, "shift"], "m", lazy.window.toggle_maximize()),
    Key([mod], "m", lazy.window.toggle_minimize()),
    Key([mod, "shift"], "f", lazy.window.bring_to_front()),

    # not working
    Key([mod, "shift"], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout"),

    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause player"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),

    # Key([mod], "b", lazy.spawn("browser")),
]

def to_prev_screen(qtile, move_window=True):
    num_screens = len(qtile.screens)
    i = qtile.screens.index(qtile.current_screen)
    target = (i - 1) % num_screens
    if move_window:
        group = qtile.screens[target].group.name
        qtile.current_window.togroup(group)
    qtile.cmd_to_screen(target)

def to_next_screen(qtile, move_window=True):
    num_screens = len(qtile.screens)
    i = qtile.screens.index(qtile.current_screen)
    target = (i + 1) % num_screens
    if move_window:
        group = qtile.screens[target].group.name
        qtile.current_window.togroup(group)
    qtile.cmd_to_screen(target)

keys.extend([
    Key([mod, "shift"], "p", lazy.function(to_prev_screen), desc="Move current window to previous screen"),
    Key([mod, "shift"], "n", lazy.function(to_next_screen), desc="Move current window to next screen"),
    Key([mod], "p", lazy.function(to_prev_screen, move_window=False), desc="Move current window to previous screen"),
    Key([mod], "n", lazy.function(to_next_screen, move_window=False), desc="Move current window to next screen"),
])

group_names = ["web", "code", "term", "file", "social", "media", "work", "sys", "misc"]
group_matches = {}
group_spawns = {"chat": "slack"}

groups = [Group(name, spawn=group_spawns.get(name)) for name  in group_names]

for i, g in enumerate(groups):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                f"{i+1}",
                lazy.group[g.name].toscreen(),
                desc="Switch to group {}".format(g.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                f"{i+1}",
                lazy.window.togroup(g.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(g.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4, margin=4, gap=4),
    layout.MonadTall(margin=6, gap=6, border_normal="#110011", border_focus="#aa00aa"),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


group_box_config=dict(highlight_method="block", inactive="ffffff60")
window_name_config = dict(
    foreground="aa88ff",
    txt_floating="🗗 ",
    mouse_callbacks={
        "Button1": lazy.window.bring_to_front(),
        "Button2": lazy.window.toggle_maximize(),
        "Button3": lazy.window.toggle_minimize(),
    }
)
window_count_config = dict(
    foreground="888888",
    fmt="Windows: {}",
    mouse_callbacks={
        "Button1": lazy.spawn(myWindowSwitcherInGroup),
        "Button3": lazy.layout.next(),  # TODO next window (include all windows in the cycle)
    }
)
task_list_config = dict(highlight_method="block", txt_floating="🗗 ", txt_maximized="🗖 ", txt_minimized="🗕 ")
current_screen_config = dict(active_text="•", inactive_text="•", fontsize=20, mouse_callbacks={"Button1": lazy.spawn(myPrimaryMenu)})

def sp(length=10):
    return widget.Spacer(length=length)

screens = [
    Screen(
        top=bar.Bar(
            [
                sp(),
                widget.CurrentScreen(**current_screen_config),
                widget.GroupBox(**group_box_config),
                # widget.Prompt(),
                widget.WindowName(**window_name_config),
                widget.WindowCount(**window_count_config),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.Spacer(),
                # widget.TaskList(**task_list_config),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                # widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                # widget.QuickExit(),
                widget.CurrentLayoutIcon(scale=0.66),
                sp(),
            ],
            28,
            background="#00000090"
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        wallpaper="~/wallpapers/001.jpg",
        wallpaper_mode="stretch",
    ),
    Screen(
        top=bar.Bar(
            [
                sp(),
                widget.CurrentScreen(**current_screen_config),
                widget.GroupBox(**group_box_config),
                WindowName(**window_name_config),
                widget.WindowCount(**window_count_config),
                #widget.Spacer(),
                #widget.Prompt(),
                #widget.Spacer(),
                # Spotify(play_icon="♫", foreground="ffff00"),
                # widget.Spacer(length=10),
                # widget.TaskList(**task_list_config),
                widget.Mpris2(foreground="ffff00"),
                # widget.CurrentLayout(),
                widget.CPUGraph(
                    border_width=1,
                    line_width=2,
                    mouse_callbacks={
                        "Button1": lazy.spawn(f"{terminal} -e htop"),
                        "Button3": lazy.spawn("gnome-system-monitor"),
                    }),
                widget.MemoryGraph(border_width=1, line_width=2),
                widget.Net(font="monospace", foreground='66aa66', format="U {up} D {down}"),
                widget.Systray(),
                # widget.PulseVolume(fmt="🔊{}"),
                widget.Volume(fmt="🔊{}"),
                sp(),
                widget.KeyboardLayout(configured_keyboards=['us', 'fr'], foreground='aaaaaa'),
                sp(),
                widget.Clock(format="%Y/%m/%d %a %I:%M %p"),
                widget.CurrentLayoutIcon(scale=0.6),
                widget.Wallpaper(label="WP", foreground="00aa00", random_selection=True),
                sp(),
            ],
            28,
            background="#00000090",
        ),
        # wallpaper="~/wallpapers/001.jpg",
        # wallpaper_mode="stretch",
    )
]


# @hook.subscribe.client_focus
# def on_client_focus(window):
#     logger.warn(f"on focus: Window={window}")
#     qtile.current_window.bring_to_front()
#     # window.cmd_bring_to_front()


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
