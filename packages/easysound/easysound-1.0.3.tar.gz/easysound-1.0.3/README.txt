Easy\_Sound
-----------

EasySound is a simple, easy sound programming in Python,Support MP3 and
WAV files, all sound interactions are invoked by simple function calls.
EasySound runs on Python 3

Example Usage
-------------

If you want to play the sound, you have two choices:

1.  Play without GUI

        >>> from easysound import play
        >>> play.play(test.mp3)
        >>> play.play(test.wav)

2.  Play with GUI This will open the default player

        >>> from easysound import play
        >>> play.ui_play(test.mp3)
        >>> play.ui_play(test.wav)

If you want to record

    >>> from easysound import rec
    >>> rec.rec("test.wav",2,"start","stop")

Full documentation is always available.

BUG FIXES
---------

Please report any problems found.

KNOWN ISSUES
------------

Errors occur when using `import easysound`
