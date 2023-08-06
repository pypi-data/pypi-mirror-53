


# General Information

ngfp aka new gfpoken aka gfpoken-in-python, is a Python 3 adaptation of the gfpoken program using pyglet and GTK3.  ngfp is a puzzle game where you place mirrors to interact with marbles rolling through a grid.  The complexity and size of the game can be adjusted.  Some games may have more than one solution but they will all count as winning games.  Have fun!



# To Install for a Linux/Posix Type System

  I am still working on some details but it should work.  I can only test on a Debian Linux system locally so I welcome bug or informational reports from people who try it out.

  I usually set up a virtual environment to install and try out things as this isolates the newly downloaded dependencies from the rest of the system.  If you are not familiar with that process look into the


```shell
  $ python3 -m venv <dir>
```


 command.  Once that is set up and you have activated it then you can install ngfp by using the command


```shell
  $ pip install ngfp
```

  This should bring in any depencies needed.

  Once this completes then to run ngfp from a console terminal you should be able to use the command


```shell
  $ runngfp
```


  When you are done playing the game and don't want to install other things you can run the following to deactivate it


```shell
  $ deactivate
```


  When I can figure out how to get Menu items added and a more clickable way to start the program that will help out people who don't use the terminal command lines.



# New Coding or Artwork Contributions

  - check TODO or ask to make sure efforts are not duplicated

  - new code or artwork will be licensed under Apache-2.0
    - attribution will be to "Name" <email@address>


# To Make Spacing Consistent

  Use the following commands before submitting pull requests or 
patches.


  To see what the changes would look like


```shell
     $ autopep8 . --recursive --select=E101,E121 --diff
```


  To make the changes


```shell
     $ autopep8 . --recursive --select=E101,E121 --in-place
```



# Previous Artwork and Manual Page

  From gfpoken version 1-2 the following things were used (see AUTHORS for the list of files and their copyrights and licensing):

  - artwork which was rescaled to 64 pixels

  - the man page was adapted/edited but needs to be set up yet...



