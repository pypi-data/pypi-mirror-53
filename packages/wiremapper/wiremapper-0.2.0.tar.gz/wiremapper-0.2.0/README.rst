Wiremapper
==========

This is a python GTK3 application that uses the pockethernet library
to run various network tests using the Pockethernet hardware (a bluetooth
connected network diagnostics tool)

Features
--------

* Quicktest feature which is a single-button test-everything sensible mode.
  If you have a wiremap inserted it will run a wiremap and otherwise it
  will run link/poe tests

* Pair the pockethernet once with your regular bluetooth menu and
  Wiremapper will deal with connecting for you. There's a dropdown
  in the header to switch between paired pockethernets if you have
  multiple (showing bluetooth device aliases set in the regular bluetooth
  menu)

Screenshots
-----------

.. image:: data/screenshot-wiremap.png

.. image:: data/screenshot-link.png

.. image:: data/screenshot-loopback.png

.. image:: data/screenshot-light-theme.png