Google Music Helper
===================
A simple collection of scripts to help manage your All Access library.

There are some serious shortcomings since:
1. This was my first time writing Python.
2. I wrote this in a few hours whilst procrastinating!

I'm happy to accept any pull requests that:
* Fix bugs that have been reported in an issue
* Add features that have been discussed in an issue

Likewise, if you'd like to see something added just submit an issue

Quick start
===========

I wrote this against Python 2.7.6 with PyCharm; I haven't tested it on anything else.

### Dependencies
* You'll need [The Unofficial Google Music API](https://github.com/simon-weber/Unofficial-Google-Music-API). You can install it using [pip](http://www.pip-installer.org/en/latest/installing.html) with ```pip install gmusicapi```.


Functionality
=============

What does this thing do?

### Automatically replace uploaded albums with All Access versions

1. Finds all manually uploaded albums in your library
2. One-by-one, searches for the album on All Access
3. If a result is found, prints the original track list, then the All Access track list
4. If prompted, deletes the uploaded tracks and adds the All Access ones to your library

# Notes
When using this, be careful to compare the original data to the All Access data - sometimes All Access matches cover albums and other unwanted things. Be sure to answer NO! in these cases.

