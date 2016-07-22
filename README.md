# better-xdotool
xDoTool is awesome.  Except for, y'know, having to spell out special characters

0.  Changelog:
  
  Version 1.1 7th July 2016

    * Renamed to better_xdotool.py because xdotool_plus doesn't feel right
    * Terminal colors!  That's right, no more walls of white text (mostly).
    * Basics of exception handling.  KeyboardInterrupt events should be nice and clean,
      but it still needs handling for xdotool events
    * Text formatting is much cleaner than it was before.
    * Speaking of cleanup, it should exit cleanly now instead of crashing out with an Interrupt
  
  Version 1.0 6th July 2016

    * The thing works, mostly.  Still a lot of cleanup to do in the code and make it nicer
      but it works

I.  What is this thing?
  
  It's a front-end for the old xdotool utility for,
  among other things, sending keystrokes to an open remote x11 session.
  
  In fact, that's all it does at the moment.  Maybe the ability to use other functions of
  xdotool will be implemented in the future, but this was created to solve a specific problem.

II. Why?
  Using xdotool from your friendly neighborhood apt repository is all fine and it works,
  but guess what?  Spelling out symbols like $#@ & ^ is annoying!
  (What even *is* asciicircum anyway?)
  So, this tool lets you feed xdotool plain old bash commands
  -and possibly those for other shells too -
  and still get the same commands on the remote machine!

    In short, it turns their terminal into yours.

III. What can I use this for?
  ~~leet x11 hacking~~  Any time you'd want to send keystrokes to a remote x11 window.
  Where do you get one?  Sorry, can't help you there.  Don't do illegal or stupid things, kids.

IV.  Okay...what do I need to run it?  (Dependencies)
  * Python 3.5, mostly.  Yes, 3.5.  There's a neat little function in there that I actually used.
      Maybe legacy support can come in the future.  It doesn't look too nasty (I hope)
  * xdotool is kind of important.
  * You'll also need other tools for using x11 sessions - namely XWinInfo, xdpyinfo, and other such things
  * A Linux box to run it on.  I use Kali 2 (the rolling one), but I don't know why it couldn't work on other *nixen
    Cross-platform support could be forthcoming, assuming you can port over the x utilities
  * You might need a few Python packages.  Working on somehow packaging these,
    but you might need to grab termcolor or others in the meantime.

V.  How do I use it?
  * chmod +x script.py and run as any ordinary script on Linux.
    Sure, you could probably run it by doing python3 script.py, but where's the fun in that?
  * Input your info as prompted.
  * ???
  * Profit

VI. Who built this monstrosity, and can I hack on it too?
  * @bassitone wrote this, and of course you can!  I <3 open source (and the GPL or whatever license is "in" these days)
