# A Python Module for Rosie Pattern Language

This module can be installed using `pip install rosie`.  It requires a Rosie 
installation, which is done separately.  
(See the [Rosie repository](https://gitlab.com/rosie-pattern-language/rosie).)

## Documentation

This module follows the API established by the Python `re` module where possible,
and extends it where necessary.

Documentation is not yet available, but the files 
[examplere](https://gitlab.com/rosie-community/clients/python/blob/master/test/examplere.py) 
and 
[examplerosie](https://gitlab.com/rosie-community/clients/python/blob/master/test/examplerosie.py) 
demonstrate how some typical uses of
`re` can be done with `rosie`.

See also the tests in [test/test.py](https://gitlab.com/rosie-community/clients/python/blob/master/test/test.py).


## Thanks

Many thanks to the original author of this Python binding, Jenna Shockley!



## This is how the PyPI package was created

(1) Test the installation locally:

	pip install -e .

(2) Build the source distribution:

    python setup.py sdist

(3) Upload to PyPI:

	twine upload dist/*

