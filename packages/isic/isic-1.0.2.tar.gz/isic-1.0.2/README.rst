ISIC
====

This is just a Python-friendly way to reference revision 4 of the International
Standard Industrial Classification (ISIC).  It's the result of pulling down
`this URL`_ and formatting it into a native Python object.  For more
information, or to see this data in other original source formats, visit the UN
`here`_.

.. _this URL: https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/ISIC_Rev_4_english_structure.Txt
.. _here: https://unstats.un.org/unsd/classifications/Econ/isic


How Do I Use It?
----------------

It's really not very advanced.  Just import it and reference it however you
like:

.. code-block:: python

    from isic import ISIC


    print(ISIC["02"])  # "Forestry and logging"
    print(ISIC["B"])  # "Mining and quarrying"

It's also handy if you want to use it in a Django model:

.. code-block:: python

    from django.db import models
    from isic import ISIC


    class MyModel(models.Model):
        industry = models.CharField(max_length=5, choices=ISIC.items())


Installation
------------

It's on PyPi, so just install it with pip.

.. code-block:: shell

    $ pip install isic
