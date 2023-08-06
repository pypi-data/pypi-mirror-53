admcycles
=========

admcycles is a `SageMath <https://www.sagemath.org>`_ module to compute with
the tautological ring of the moduli spaces of complex curves.

Prerequisites
-------------

Make sure that `SageMath <https://www.sagemath.org>`_ is installed on your computer. Detailed installation instructions for different operating systems are available `here <http://doc.sagemath.org/html/en/installation/binary.html>`_ and at the Sage-website.

Installation
------------

The most convenient way to use admcycles is to add the package to your Sage-installation. The exact procedure for this depends on your operating system and how you installed Sage, see below. If the installation instructions below should fail, see below how to use it without installation. 

- if you manually installed Sage by downloading it from the website or
  compiled it yourself, then run::

      $ sage -pip install admcycles --user

- if you have archlinux and installed the sagemath package (via pacman),
  then run::

     $ pip2 install admcycles --user

- if you have Ubuntu or Debian and installed the sagemath package (via
  apt) then run::
  
     $ source /usr/share/sagemath/bin/sage-env
     $ pip install admcycles --user


In all the commands above, the option ``--user`` is optional and makes it so that
it will install the module into your user space. If you want a system install,
remove this option. On the other hand, if you want to install the latest (development) version
of admcycles and have the versioning software git installed, replace  ``admcycles`` in the commands above by ``git+https://gitlab.com/jo314schmitt/admcycles``.

Use without installation
------------------------

To use the package without installing, download the package as a `zip`-file either from `PyPI <https://pypi.org/project/admcycles/>`_ or from `gitlab <https://gitlab.com/jo314schmitt/admcycles/-/archive/master/admcycles-master.zip>`_.
Unpack the `zip`-file, creating a folder ``admcycles-master``, which should contain files such as ``setup.py``. In the future, when you want to use admcycles, you should run sage from the folder ``admcycles-master``. So if the full path of this folder is ``/u/You/Downloads/admcycles``, you should start the Sage-session below by::

  sage: cd /u/You/Downloads/admcycles
  sage: from admcycles import *
  
If you run Sage in Windows using cygwin, the path above should be a cygwin path and will looks something like ``/cygdrive/c/Users/You/Downloads/admcycles-master``.

To start using admcycles, start a Sage-session in the command line (e.g. by opening the command line and typing ``sage``). Then type::

   sage: from admcycles import *

To try a first computation, you can compute the degree of the class kappa_1 on Mbar_{1,1} by::

   sage: kappaclass(1,1,1).evaluate()
   1/24


Example
-------

A simple computation::

   sage: from admcycles import *

   sage: t1 = 3*sepbdiv(1,(1,2),3,4) - psiclass(4,3,4)^2
   sage: t1
   Graph :      [1, 2] [[1, 2, 5], [3, 4, 6]] [(5, 6)]
   Polynomial : 3*
   <BLANKLINE>
   Graph :      [3] [[1, 2, 3, 4]] []
   Polynomial : (-1)*psi_4^2

Build documentation
-------------------

To build the documentation, go in the repository docs/ and
then run in a console::

    $ sage -sh
    (sage-sh)$ make html
    (sage-sh)$ exit

The documentation is then available in docs/build/

Running doctests
----------------

To run doctests, use the following command::

    $ sage -t --force-lib admcycles/ docs/source

If it succeeds, you should see a message::

    All tests passed!

License
-------

admcycles is distributed under the terms of the GNU General Public License (GPL)
published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version. See http://www.gnu.org/licenses/.

Authors
-------

- `Aaron Pixton <http://math.mit.edu/~apixton/>`_
- `Johannes Schmitt <https://people.math.ethz.ch/~schmittj/>`_
- `Vincent Delecroix <http://www.labri.fr/perso/vdelecro/>`_
- `Jason van Zelm <https://sites.google.com/view/jasonvanzelm>`_
