# Moon Nectar
A cross-platform music player designed to be simple yet offer powerful library organization capabilities and easy extensibility through plugins.

## Status

A proof of concept prototype is being developed.

## Project Description

Moon Nectar is a new concept media player designed around the following ideas:

* **Python:** Written in Python v3.7 or newer utilizing the all new features of the language (no backwards compatibility will be maintained).
* **Tags:**  Add tags (labels/keywords) to music files to permit more flexible library organization.  Similar in concept to how GMail uses labels to organize mail instead of using folders.
* **Remote:** The application will be designed specifically to permit a remote control to be developed (android/iOS/etc.).  However, creation of this remote is not a project goal at this time.
* **Simple core functionality:** No unnecessary frills will be added outside of specific project goals.
* **Plugins:** A plugin interface will be provided which permits the addition of new capabilities.  The exact capabilities of the plugin interface are TBD.
* **NoSQL:** A NoSQL data store will be used to contain library information.
* **Cross-Platform:** While the code is being developed on MacOS, it is intended to be a cross-platform media player.
* **GUI Separation:** GUI code will be structurally separate from all other code.  Benefits:
  * Cleaner code.
  * Not locked in to a single user interface.
  * Simplify plugins (only GUI plugins need to worry about GUI related code)
  * Flexibility in future development.
  * Increased utilization of python standard library code

Moon Nectar was inspired by the Quod Libet music player, the Clementine music player, a desire for a new way of organizing music and a deep dissatisfaction with music software available for MacOS.

