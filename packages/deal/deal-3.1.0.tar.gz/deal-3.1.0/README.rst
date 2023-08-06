

.. image:: https://raw.githubusercontent.com/orsinium/deal/master/logo.png
   :target: https://raw.githubusercontent.com/orsinium/deal/master/logo.png
   :alt: Deal

======================================================================================================================================================================


.. image:: https://travis-ci.org/orsinium/deal.svg?branch=master
   :target: https://travis-ci.org/orsinium/deal
   :alt: Build Status
 
.. image:: https://coveralls.io/repos/github/orsinium/deal/badge.svg
   :target: https://coveralls.io/github/orsinium/deal
   :alt: Coverage Status
 
.. image:: https://img.shields.io/pypi/v/deal.svg
   :target: https://pypi.python.org/pypi/deal
   :alt: PyPI version
 
.. image:: https://img.shields.io/pypi/status/deal.svg
   :target: https://pypi.python.org/pypi/deal
   :alt: Development Status
 
.. image:: https://img.shields.io/github/languages/code-size/orsinium/deal.svg
   :target: https://github.com/orsinium/deal
   :alt: Code size


**Deal** -- python library for `design by contract <https://en.wikipedia.org/wiki/Design_by_contract>`_ (DbC) programming.

That's nice ``assert`` statements in decorators style to validate function input, output, available operations and object state. Goal is make testing much easier and detect errors in your code that occasionally was missed in tests.

Features
--------


* Functional declaration.
* Custom exceptions.
* Raising exceptions from contract.
* Django Forms styled validators.
* Attribute setting invariant validation.
* Dynamically assigned attributes and methods invariant validation.
* Decorators to control available resources: forbid input/output, network operations, raising exceptions

Available decorators
--------------------

CLassic DbC:


* ``@deal.pre`` -- validate function arguments (pre-condition)
* ``@deal.post`` -- validate function return value (post-condition)
* ``@deal.inv`` -- validate object internal state (invariant)

Take more control:


* ``@deal.offline`` -- forbid network requests
* ``@deal.raises`` -- allow only list of exceptions
* ``@deal.safe`` -- forbid exceptions
* ``@deal.silent`` -- forbid output into stderr/stdout.

Installation
------------

.. code-block:: bash

   pip3 install --user deal

Quick Start
-----------

.. code-block:: python

   import re

   import attr
   import deal

   REX_LOGIN = re.compile(r'^[a-zA-Z][a-zA-Z0-9]+$')

   class PostAlreadyLiked(Exception):
       pass

   @deal.inv(lambda post: post.visits >= 0)
   class Post:
       visits: int = attr.ib(default=0)
       likes: set = attr.ib(factory=set)

       @deal.pre(lambda user: REX_LOGIN.match(user), message='invalid username format')
       @deal.raises(PostAlreadyLiked)
       @deal.chain(deal.offline, deal.silent)
       def like(self, user: str) -> None:
           if user in self.likes:
               raise PostAlreadyLiked
           self.likes.add(user)

       @deal.post(lambda result: 'visits' in result)
       @deal.post(lambda result: 'likes' in result)
       @deal.post(lambda result: result['likes'] > 0)
       @deal.pure
       def get_state(self):
           return dict(visits=self.visits, likes=len(self.likes))

Now, Deal controls conditions and states of the object at runtime:


#. ``@deal.inv`` controls that visits count in post always non-negative.
#. ``@deal.pre`` checks user name format. We assume that it should be validated somewhere before by some nice forms with user-friendly error messages. So, if we have invalid login passed here, it's definitely developer's mistake.
#. ``@deal.raises`` says that only possible exception that can be raised is ``PostAlreadyLiked``.
#. ``@deal.chain(deal.offline, deal.silent)`` controls that function has no network requests and has no output in stderr or stdout. So, if we are making unexpected network requests somewhere inside, deal let us know about it.
#. ``deal.post`` checks result format for ``get_state``. So, all external code can be sure that fields ``likes`` and ``visits`` always represented in the result and likes always positive.

If code violates some condition, sub-exception of ``deal.ContractError`` will be raised:

.. code-block:: python

   p = Post()
   p.visits = -1
   # InvContractError:

Dive deeper on `deal.readthedocs.io <https://deal.readthedocs.io/>`_.
