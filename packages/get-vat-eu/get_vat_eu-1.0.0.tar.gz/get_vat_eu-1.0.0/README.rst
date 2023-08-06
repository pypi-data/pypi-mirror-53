Get VAT EU
==========

A utility that is able to get and parse EU EC VATs.

Video
-----

TODO

Description
-----------

This library parsers the elements returned by the VIES SOAP API of the 
European Commission. The trader address field usually contains all the needed
information and needs to be separated into various elements such as the city,
postal code, address and house number, etc... This is what this library does.

Documentation
-------------

https://citycommerce.github.io/get-vat-eu

API examples
------------

get-vat-eu has a `public API`_. This means for example that you can you easily get
all trader information like this:


::


    >> import get_vat_eu
    >> print(get_vat_eu.pipeline('01561700293', 'IT'))
    {'name': 'CITYCOMMERCE SRL', 'address': 'Viale Porta Adige 45', 'city': 'Rovigo', 'province': 'RO', 'post_code': '45100', 'vat_number': '01561700293', 'country_code': 'IT'}

.. _public API: https://citycommerce.github.io/get-vat-eu/api.html

CLI Helps
---------

TODO

License
-------

Copyright (c) 2019 CityCommerce srl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
