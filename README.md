Google Music Helper
===================

A simple collection of scripts to help manage your All Access library.

There are some serious shortcomings since:

1. This was my first time writing Python.
2. I wrote this in a few hours whilst procrastinating!

I'm happy to accept any pull requests that:

* Fix bugs that have been reported in an issue
* Add features that have been discussed in an issue
* Add tests
* Refactor meaningfully - e.g. apply a more 'Pythonic' style :)

Likewise, if you'd like to see something added just submit an issue.

Quick start
===========

I wrote this against Python 2.7.6 with PyCharm; I haven't tested it on anything else.

### Dependencies

* You'll need [The Unofficial Google Music API](https://github.com/simon-weber/Unofficial-Google-Music-API). You can install it using [pip](http://www.pip-installer.org/en/latest/installing.html) with ```pip install gmusicapi```.


Functionality
=============

So, what things can it do?

### Replace uploaded albums with All Access versions

1. Finds all manually uploaded albums in your library
2. One-by-one, searches for the albums on All Access
3. If a result is found, prints the original track list, then the All Access track list
4. Asks whether the album should be replaced
4. If 'yes', deletes the uploaded tracks and adds the All Access ones to your library

#### Notes

When using this, be careful to compare the original data to the All Access data - sometimes All Access matches cover albums and other unwanted things. Be sure to answer 'no' in these cases.

### Add all tracks from all existing artists in your library

1. Finds all unique artists in your library
2. For each artist, finds their associated albums / collaborations
3. Adds all tracks from the found albums / collaborations

#### Notes

I'm not sure that there's a use case for this really. At the very least it should prompt before adding all the tracks associated with an artist. I began running this on my library to test it and ended up with 212 Alison Krauss tracks in my library since I had a single track of hers present in the O' Brother Where Art Thou OST!

