## Compiling
~~~
rm -rf build byprice_scrapingtools.egg-info dist
python setup.py sdist bdist_wheel
twine upload dist/*
~~