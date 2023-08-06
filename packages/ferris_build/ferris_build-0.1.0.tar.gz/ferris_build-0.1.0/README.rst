======
Ferris
======


.. image:: https://img.shields.io/pypi/v/ferris_build.svg
        :target: https://pypi.python.org/pypi/ferris_build

.. image:: https://img.shields.io/travis/yngtodd/ferris.svg
        :target: https://travis-ci.org/yngtodd/ferris

.. image:: https://readthedocs.org/projects/ferris/badge/?version=latest
        :target: https://ferris.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/yngtodd/ferris/shield.svg
        :target: https://pyup.io/repos/github/yngtodd/ferris/
        :alt: Updates


Building tool for Rust

This is an alpha stage refactor of Rust's x.py_, the tool used to build Rust `[1]`_.
I was curious about the build process for Rust, so I thought that refactoring the
build tool would help me get familiar with it! 


* Free software: BSD license
* Documentation: https://ferris.readthedocs.io.


Credits
-------

At the start of this refactor, there were 70 contributors to Rust's bootstrap.py_. While 
there may be some small changes that I make to the source code here, I want to make sure
to acknowledge their hard work. This little project would not exist without them.

There are many contributors to Rust, and they all deserve a shout out. I am really excited 
to see where the language goes. And, if this project helps anyone, even if that means just 
me, I will be stoked. 

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _x.py: https://github.com/rust-lang/rust/blob/master/x.py
.. _`[1]`: https://rust-lang.github.io/rustc-guide/how-to-build-and-run.html
.. _bootstrap.py: https://github.com/rust-lang/rust/blob/master/src/bootstrap/bootstrap.py
