from setuptools import setup, find_packages
install_requires = ['click','pyyaml','deepdiff','ordered-set']
setup(
    name='DiffPrinter',
    py_modules=['DiffPrinter'],
    version='1,0,0',
    author_email='eldar.erel@gmail.com',
    url='https://github.com/EldarErel/',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pdiff = DiffPrinter:cli'
        ],
    }
)
