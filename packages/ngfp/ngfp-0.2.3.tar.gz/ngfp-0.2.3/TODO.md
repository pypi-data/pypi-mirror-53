Mon 07 Oct 2019 11:45:53 AM EDT


  Bugs and comments to Ant <ant@anthive.com> or via the
project page.


Wishlist (for someone else to do if they'd like :) )

  - it would simplify licensing if I had not used artwork 
    from gfpoken version 1-2.  I don't see myself having 
    the time in the near future to make new artwork.  I 
    really need to spend some more time studying Python 3
    and OOP concepts instead.


Notes

  I'm not planning on doing networking version at this 
time - I've never used it myself.


v1.0.0 - ?  This TODO

  - packaging for debian

  - restructure code (encapsulate, objectify, clean it up,
    tests and comments)

  - figure out man page


v0.2.3

  - restart game bug fix (needed to recount mirrors)


v0.2.2

  - added restart game key (F5)


v0.2.1

  - end of game bug
    - marbles and arrows getting out of sync
      when checking if we've won


v0.2.0

  - end of game freeze fixed
  - add version.py


v0.1.19

  - stop animation if absorbed


v0.1.18

  - stop the animation at the edges


v0.1.17

  - adjust some dialog messages


v0.1.16

  - improve help dialogs and manual page
  - make complex check more in depth
  - make it so the Green and Pink indicators are used to 
    display game state:
    - Green in Guess grid
    - Pink in puzzle grid


v0.1.15

  - allow change markers only in guess board

  - end of game complex check matching bug the
    display did not reflect game correctly after
    checking

  - markers did not show if loaded from file


v0.1.14

  - moved the control column (light green squares)
    - once in a while it was too easy to click a check or
      flip board control square by mistake


v0.1.13

  - change window to not be resizeable

  - add information about executable directory to the About screen


v0.1.12

  - moved the markers a little so they weren't right on the
    edge

  - removed some redundant code (self.pic_list was a copy of
    cfg.pic_list)


v0.1.11

  - bug fix for ToggleMarker in board.py, if there was no
    initial movement by the mouse over the board the value
    looked up didn't exist.


v0.1.10

  - Revert PyGObject requirement as it gives the same error 
    as before and also deprecation warnings when running


v0.1.9

  - add more directions to the README.md about how to install and run


v0.1.8

  - Use PyGObject >= 3.31.1.dev0 in setup to avoid error on
    install


v0.1.7

  - fixed missing MANIFEST.in


v0.1.6

  - packaging for PyPI Test (works)
    - make all imports include the ngfp (done)
    - change all the image imports to use cfg.png_path (done)


v0.1.5

  - packaging work for PyPI

  - create subdirectory for ngfp, move png/ and create doc/


v0.1.4

  - licensing
    - new contributions go under Apache-2.0
      - new artwork Apache-2.0
    - artwork used from gfpoken version 1-2 is GPL3+

  - start on packaging

  - removed some of the artwork files that were not being used


v0.1.3

  - markers (done)


v0.1.2

  - sometimes changes are not reflected immediately in the
      the left scales of the config dialog (works)

  - comparing boards
    - exact match is easy (works)
    - functional match is harder (works)

  - help screen (works)

  - about screen (works)

  - man page (done)


v0.1.1

  many changes and some reorganization of code.
a lot of testing and debugging of what has 
been done is still needed yet.  please don't 
report bugs - i know of a lot already...  :)

  - some global values were moved into config.py

  - configuration files and directory under
    $HOME/.config/ngfp (for a posix system, i don't	
    know much about where on windows yet)

    - configuration file name is config_ngfp.json

    - initial run of program just uses defaults from
      config.py, but eventually clicking on Save Config
      will create the directory and file and from then
      on when you start the game it will use the 
      previously saved configuration

  - restore defaults (sorta works)

  - save and load games (mostly works)

    - files in $HOME/.local/share/ngfp (for a posix 
      system, i don't	know much about where on windows yet)

    - much better dialogs and more flexibility in naming

  - new random game (mostly works)

  - resizing game (mostly works)

    - the limits i have set in config.py are for a screen
      size of 1920 x 1080 pixels, you can adjust them to
      fit your screen size:

      - min_cols = 1      # this actually works
      - min_rows = 6      # for the moment
      - max_cols = 22     # on 1920 x 1080
      - max_rows = 13     # on 1920 x 1080

        - eventually i want to get min_rows smaller
          or even have the widget counts/piles in their
          own window - this will make it easier to get
          going for children who may not want to start
          on games bigger then 4x4 or so...


v0.1.0

  - save and load games the initial simple version (works)
    - load from a gfpoken save file (works)
      - when you save it use file name "save.ngfp"
    - load as json file (works)
      - use file name "save.json"
    - save to json file (works)
      - always overwrites or writes file name "save.json"


    Notes:

      if both files ("save.ngfp" and "save.json") exist for now
    the first one "save.ngfp" is loaded and "save.json" is 
    ignored.  if you only want "save.json" used then, rename 
    "save.ngfp" or remove it.


v0.0.9

  - fix label code a bit (works)
    - can use label.text to change label

  - some animation or way of showing what happens on guess board (works)


v0.0.8

  - a bit of fun showing where the marble is bouncing
    around in the game - this doesn't stay in the final
    version, but i may leave it in as an option/toggle
    anyways because it might help in debugging...


v0.0.7


  - flipping mirrors (3-4,5-8,13-14,17-18,23-30) (works)
  - last two mirrors - they move (works)


v0.0.6

  - some game logic (works)
    - all the easy mirrors (1,2,9,10,11,12,15,16,19,20,21,22) (works)
    - putting a marble in motion (works)
    - detecting where it comes out (works)
    - history with colored markers (works)


v0.0.3-v0.0.5

  - grab widgets and put on guess board (works)
  - update counts text (works)
  - moving items (works)
  - removing items from board to go back to widget piles (works)
  - rotating guesses (works)


v0.0.0 - v0.0.2
  initial import of code so far and a few basic changes



