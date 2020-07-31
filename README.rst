mcimage
===============

A tool written in Python for producing a Minecraft function file ``.mcfunction`` for map pixel art.

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

Generating the function
~~~~~~~~~~~~~~~~~~~~~~~

First, the function file is generated from the image, by doing

.. code::

    python3 main.py <path_to_image>

Or on Windows

.. code::

    py -3 main.py <path_to_image>

This may take a while!

Use the ``-h`` or ``--help`` flag for customisation options.

Using the function in Minecraft
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, a ``datapacks`` folder is generated, containing a folder called ``mcimage``. 
The ``mcimage`` folder is a datapack, and contains the function required to draw the image using Minecraft blocks.

In order to use the datapack, you can add the datapack to an existing world by copying and pasting it into the world's ``datapacks`` directory.
This is found at ``<minecraft_dir>/saves/<world>/datapacks``, where ``<minecraft_dir>`` is the install location of Minecraft, 
and ``<world>`` is the name of your world.

Datapacks are enabled when the world is first loaded, but for loaded worlds, you must execute the ``/reload`` command first.

Alternatively, you can add the datapack in-game when you create a new world.

Superflat worlds are recommended.

The function name is a namespaced function. The namespace is derived from the image filename. 
It is lowercased, stripped of its extension, and then all non-alphabetic characters are replaced with underscores.

For example, if the image filename is ``Dark Side of The Moon.jpeg``, then the namespace is ``dark_side_of_the_moon``.
The function consists of the namespace, followed by a colon, followed by ``draw``. So for the above example, the command to draw would be ``/function dark_side_of_the_moon:draw``.

The command teleports you to ``0 150 0`` and changes your gamemode to creative. Draw on an empty map to view the image.

The commands may take a while to execute and render. Be patient!

For more information, check the Minecraft Wiki's page on datapacks_ and the `function command`_.

License
-------

`MIT License`_

.. _pip: https://pypi.org/project/pip
.. _NumPy: https://pypi.org/project/numpy
.. _Pillow: https://pypi.org/project/Pillow
.. _MIT License: https://choosealicense.com/licenses/mit
.. _datapacks: https://minecraft.gamepedia.com/Datapack
.. _function command: https://minecraft.gamepedia.com/Commands/function