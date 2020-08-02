mcimage
===============

A tool written in Python for producing Minecraft function files for map pixel art.

Requirements
------------

Requirements are installed using pip_, and are detailed in ``requirements.txt``.

- NumPy_
- Pillow_

Install these requirements by using the command

.. code::

    python3 -m pip install -r requirements.txt

Or on Windows

.. code::

    py -3 -m pip install -r requirements.txt

Usage
-----

Generating the functions
~~~~~~~~~~~~~~~~~~~~~~~~

First, function file, or files, is/are generated from the image, by doing

.. code::

    python3 main.py <path_to_image>

Or on Windows

.. code::

    py -3 main.py <path_to_image>

This may take a while!

There are also several options you can use.

- ``-d dir``, where ``dir`` is the path (relative or absolute) of the directory to place generated datapacks.
- ``-n name``, where ``name`` is the datapack to export, default is ``mcimage``.
- ``--ns namespace``, where ``namespace`` is the namespace for the functions. By default this is derived from the image filename.
- ``--size size``, where ``size`` is the size that the image will be scaled to for Minecraft. Possible values are 1 or 2, for 128x128 and 256x256 images respectively.

Using the functions in Minecraft
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, a ``datapacks`` folder is generated, containing a folder called ``mcimage``. 
The ``mcimage`` folder is a datapack, and contains the function required to draw the image using Minecraft blocks.

In order to use the datapack, cheats **must** be enabled. 

It's **highly** recommend that you create a new world to execute the commands. You risk losing blocks that are in the same space as the blocks to be placed by the functions.
It is also easier to add the datapack in-game to the new world when it is created.

If you wish, you can add the datapack to an existing cheats-enabled world by copying and pasting it into the world's ``datapacks`` directory.
This is found at ``<minecraft_dir>/saves/<world>/datapacks``, where ``<minecraft_dir>`` is the install location of Minecraft, 
and ``<world>`` is the name of your world.

Datapacks are enabled by default when you open a world, but for worlds that you have already opened, you must execute the ``/reload`` command first.

**Superflat worlds are recommended.**

Functions have a *namespace*. The namespace is derived from the image filename. 
The image filename is lowercased, stripped of its extension, and then all non-alphabetic characters are replaced with underscores.

For example, if the image filename is ``Dark Side of The Moon.jpeg``, then the namespace is ``dark_side_of_the_moon``.

The main function that you'll need to use is the ``setup`` function. So for the above example namespace, run the command ``/function dark_side_of_the_moon:setup``.
This will teleport you to a "viewing platform" with some command blocks. Run the command blocks to draw the image using the button.

The commands may take a while to execute and render. Be patient!

For more information on using the datapack, check the Minecraft Wiki's page on datapacks_ and the `function command`_.

Getting the image onto a map (or maps)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The blocks are placed in the world such that the top-left corner of the image is aligned with the top-left corner of a map drawn within the image. 

- For 128x128 images, create a new map within somewhere within the space between the boundaries of the blocks placed.
- For 256x256 images, create four new maps, one in each quadrant of the blocks placed.

For a 128x128 image, you can view the map whilst you have selected it in your inventory hotbar, but image maps are best viewed in item frames.

License
-------

`MIT License`_

.. _pip: https://pypi.org/project/pip
.. _NumPy: https://pypi.org/project/numpy
.. _Pillow: https://pypi.org/project/Pillow
.. _MIT License: https://choosealicense.com/licenses/mit
.. _datapacks: https://minecraft.gamepedia.com/Datapack
.. _function command: https://minecraft.gamepedia.com/Commands/function