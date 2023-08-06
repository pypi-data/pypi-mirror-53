from setuptools import setup

'''
LOCAL: 
install:  pip install .

---------------------------------------
REMOTE:
pip install --user --upgrade twine

## upload
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python -m twine upload -u crazyj --repository-url https://test.pypi.org/legacy/ dist/* --verbose


## install
pip install --index-url https://test.pypi.org/simple/ --no-deps mypackcrazyj

pip uninstall mpackcrazyj
 

'''

setup(name='mypackcrazyj',
      version='0.1.1',
      description='package testing',
      url='http://github.com/crazyj7/python/mypack_crazyj',
      author='crazyj',
      author_email='crazyj7@gmail.com',
      license='MIT',
      packages=['mypackcrazyj'],
      install_requires=['markdown',],
      zip_safe=False)


'''

install_requires : import files...
python_requires='>=3.6'


'''