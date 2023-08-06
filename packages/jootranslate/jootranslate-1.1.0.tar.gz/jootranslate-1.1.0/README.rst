|image0| |image2| |image3| |PyPI - Python Version| |image4| |Docs|

jootranslate
------------

**hint**

The needed directory structure has changed in version 0.7.2

Used search filters in php and xml files:

* JText::_("COM_COMPONENTNAME")
* JText::script("COM_COMPONENTNAME")
* label="COM_COMPONENTNAME"
* description="COM_COMPONENTNAME"
* hint="COM_COMPONENTNAME"
* title="COM_COMPONENTNAME"
* <name>COM_COMPONENTNAME</name>
* <description>COM_COMPONENTNAME</description>
* <![CDATA[COM_COMPONENTNAME]]>

This is just a little helper so you don\`t have to copy and paste all
your translation strings by hand.

Your ini files need the following syntax

::

    TRANSLATION_STRING = 'translation'
    do not use a syntax like
    TRANSLATION_STRING='translation'

    and only use ' not "

Or you start without any ini files and let jootranslate create it for you.

Your component needs the following directory structure

::

    admin
        - controllers
        - language
        - etc ...
    site
        - controllers
        - language
        - etc...

**installation**

use pip

::

    pip install --user jootranslate

local

::

    python setup.py install

**usage**

::

    jootranslate --source /path/to/component/root --com your_component

to see a full list of all options

::

    jootranslate -h

    usage: jootranslate [-h] -s PATH -c COM [-l LANG] [-t]

    A translation ini file generator for joomla developers

    optional arguments:
      -h, --help            show this help message and exit
      -s PATH, --source PATH
                            directory to search in
      -c COM, --com COM     the name of the component
      -l LANG, --lang LANG  language localisation. default is en-GB
      -t, --translate       If you want to translate the strings on console


.. |image0| image:: https://img.shields.io/pypi/v/jootranslate.svg
   :target: https://pypi.python.org/pypi?name=jootranslate&:action=display
.. |image2| image:: https://pyup.io/repos/github/pfitzer/jtranslate/shield.svg?t=1520427395490
   :target: https://pyup.io/account/repos/github/pfitzer/jtranslate/
.. |image3| image:: https://pyup.io/repos/github/pfitzer/jtranslate/python-3-shield.svg?t=1520427395491
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/jootranslate.svg
   :target: https://pypi.python.org/pypi?name=jootranslate&:action=display
.. |image4| image:: https://img.shields.io/pypi/dm/jootranslate.svg
    :target: https://pyup.io/repos/github/pfitzer/jtranslate/
    :alt: PyPI - Downloads
.. |Docs| image:: https://readthedocs.org/projects/jootranslate/badge/?version=latest&style=flat
    :target: https://jootranslate.readthedocs.io/
    :alt: Read the Docs
