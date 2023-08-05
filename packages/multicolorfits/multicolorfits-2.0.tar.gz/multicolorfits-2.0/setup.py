import setuptools

with open('README.md','r') as fh:
    long_description=fh.read()

setuptools.setup(
    name='multicolorfits',
    version='2.0',
    url='https://github.com/pjcigan/multicolorfits', #'http://multicolorfits.readthedocs.io',
    license='MIT',
    author='Phil Cigan',
    author_email='ciganp@cardiff.ac.uk',
    description='GUI tool to colorize and combine multiple fits images for making visually aesthetic scientific plots',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    py_modules=['multicolorfits',],
    #python_requires='>2.7',
    install_requires=['numpy','matplotlib','astropy','scipy','pyface','traits','traitsui', 'scikit-image'], #'PyQt5',
)
