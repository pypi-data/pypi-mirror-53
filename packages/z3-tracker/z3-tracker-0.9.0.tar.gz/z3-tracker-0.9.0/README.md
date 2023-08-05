# z3-tracker

** This is a development version in what you could call 'beta stage'. There will be bugs! **

### Description

z3-tracker is yet another tracker for The Legend of Zelda: A Link to the Past. It features

* item tracking,
* location tracking,
* entrance tracking.

### Installation

z3-tracker is available for Linux, Windows and MacOS. Note that the main development platform is Linux, while MacOS support is entirely untested.

##### Linux

Ensure that Python 3.6 or higher are available. z3-tracker also requires full tkinter support -- since tkinter is part of the core Python library, most distributions include it with the generic python3 package. If you are unsure, the quickest way to check is to try whether the command `python3 -c 'import tkinter.ttk'` is available.

You can run z3-tracker simply by running the z3-tracker.py script (i.e. `python3 z3-tracker.py`). Various other ways are available, including installing via pip (e.g. `pip3 install --user z3-tracker`).

##### Windows

You will need Python 3.6 or higher. You can get it [here](https://www.python.org/downloads/). Be sure not to de-select tkinter during installation. If you've allowed the installer to associate PY files with Python 3, just double-clicking `z3-tracker.py` should suffice.

##### MacOS

No support for installation on MacOS can be given here, but it *should* run. As with the other operating systems, Python 3.6 or higher is required. Again, I can't give any further details as to how to install that and run z3-tracker on MacOS.

##### Config files

z3-tracker creates a config directory (`%LOCALAPPDATA%\z3-tracker` in Windows, `~/.z3-tracker` everywhere else). Storage requirements will be unnoticable. While modifying these files is perfectly fine, it is also entirely unsupported and most likely won't survive a version update.

### Usage

##### General layout

In order to allow as much flexibility as possible in the placement of various parts of z3-tracker, a multi-window layout is used. That means that every component of the tracker opens its own window. Since z3-tracker uses tkinter (i.e. Tcl), it behaves a little bit outdated -- you can't really resize the windows. (On the other hand, using tkinter means that you don't have to install additional GUI libraries.)

##### Supported modes

* entrance shuffle (except insanity)
* all four world states
* no glitches; support for glitched modes is limited
* basic and advanced item placement
* swordless
* all four dungeon item modes
* all five goals
* Ganon's Tower/Ganon crystal requirements

##### Items and dungeons

Everything should be self-explanatory. Left-click and right-click the various objects to activate, deactivate, increase of decrease them. Certain items are grouped together on the same spot. These reflect their grouping in the game's item menu. Some functionality in the dungeon tracker is only available under certain settings.

Note that marking a dungeon as completed is not required to mark any locations dependent on the pendant/crystal of this dungeon (e.g. Master Sword Pedestal, Ganon's Tower) as available.

Crystal requirements can be set at the bottom right of the dungeon tracker window.

##### Map locations

If entrance randomiser is activated, big round symbols denote overworld items. You can left-click them to mark and unmark them as checked. An explanation of the symbol colours is provided in the in-program help.

Other types of generic item locations are only shown if entrance randomiser is disabled.

##### Entrance locations

Entrances are marked as small squares. Just like with item locations, they can be left-clicked to mark them as checked or unchecked (although it is up to the user as to find a suitable meaning of 'checked' in this case).

However, entrances also support two more actions:

* Middle-clicking an entrance and then middle-clicking another (or the same) entrance will connect the entrance of the first-clicked location with the interior of the second-clicked one. This connection is established in both directions -- i.e. the interior is also connected to the entrance, but *no* connection is made between the entrance of the second location with the interior of the first one.
* Right-clicking anywhere on the map aborts any first middle-click. If an entrance is right-clicked on, any connection that this entrance might have is removed.

When moving the mouse over an entrance with an established connection, the borders of various other (or the same) entrances may change colour. The meaning of these colours are explained in the in-program help.

##### Dungeons

Dungeons are big squares with a smaller inset square. They generally follow the same colours as items (which are explained in the in-program help). The inner square denotes whether the item reward is available, while the outer square shows whether all items in the dungeon can be collected. Since the boss in a dungeon can always hold an item, the outer square will never show itself as fully available without the inner square doing so.

Dungeon buttons can't be interacted with. They are controlled via the dungeon tracker.

##### Retro mode

Retro includes certain dungeon buttons relevant to this mode even if entrance randomiser is switched off. In this case they do not offer any functionality beyond left-clicking.

### Saving

##### Autosaving

While some may have noticed the Save and Load buttons, most users should not need them. z3-tracker stores progress automatically everytime something changes. When z3-tracker is closed and restarted, this autosave is restored.

##### Manual saving and loading

If you wish to track several states at the same time, you can also create dedicated save files using the Save button. The Load button restores any save file -- but in order to do so, it closes z3-tracker. You have to restart it manually, I'm afraid. (Sorry, the Load button is just a fringe use case to begin with.)

##### Resetting

The Reset button clears all progress *and deletes the autosave*. Note that changing any settings will not cause a reset (but vigorously switching between entrance randomiser and Retro will probably cause some display issues).

### Issues/bugs

A project like this will always come with a plethora of bugs -- especially on weirder settings. However, there are a few areas where users should be especially careful:

* There are still some minor UI bugs to be sorted out.
* There is a weird bug with autosaving. More specifically, checking off locations might get lost. So, you probably shouldn't rely on this too much at the moment. Sadly, manual saving is no help either. If anybody finds a constellation which makes this bug reproducible, please file a bug report.
* Inverted crossworld shuffle (and inverted in general) probably hass issues for locations which require Moon Pearl. This is just a matter of me forgetting some bush or pot somewhere.
* Support for glitched modes is limited. I do not wish to claim to be an authority on the rules applying to these modes, so I only included glitches which are clearly part of the item randomiser code -- which means not very many, since that code is not designed to contain such information. Major glitches especially mostly boils down to frame clipping without Pegasus Shoes and Bottle Music.
* Hearts and Bottles beyond the first one are currently not tracked. This is mostly an issue in basic item placement where certain dungeons and bosses require this. Some of these will therefore be marked as available earlier than they should.
* Insanity entrance shuffle is not supported. While z3-tracker internally knows the difference between going in and going out, I couldn't come up with a good user interface.
* Don't put any trust into the dungeon availability display, especially in anything that deviates from the normal Standard/Open non-entranced-randomised game. My original idea didn't work out and I've yet to sit down and think of something else. This is less of an issue with randomised small and big keys (although in this mode bosses might be shown as available too early, since z3-tracker doesn't strictly assume 'stupid' key-usage for this mode).
* Misery Mire and Turtle Rock entrances (and the entire accessible through them) are marked as unavailable if their medallion isn't known and not all three medallions are marked in the item tracker.
* In the same vein, random crystals is treated essentially the same as seven crystals.
* Possession of bombs isn't consistently checked (but the randomiser assumes them to always be available anyway).
* Some options (notably most of the goals) don't actually change the tracker behaviour.
* Many people who have only come in contact with the the Twitch-centred community surrounding the VT8 randomiser and their nomenclature will probably find some location names unfamiliar.

Bugs may be reported on Github. Bug reports should include the contents of the config directory. If you're feeling adventurous, you can also take a look at the ruleset/vt8 directory. This is where the actual location rules reside and should be easy to read.

### Credits

- The authors of the entrance randomiser variant of the VT8 randomiser. (No worries, I didn't incorporate any code this time.)
- I also had a cursory look around other trackers before writing this one, most notably Orphis' (sadly unfinished) entrance tracker.
- The artwork (owned by Nintendo) was copied from various places.
