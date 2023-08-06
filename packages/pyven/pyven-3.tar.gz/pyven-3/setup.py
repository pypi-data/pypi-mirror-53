import setuptools

setuptools.setup(
        name = 'pyven',
        version = '3',
        install_requires = ['aridity'],
        packages = setuptools.find_packages(),
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
        py_modules = ['gclean', 'tasks', 'release', 'runtests', 'travis_ci', 'pyven', 'toplevel', 'tests'],
        scripts = ['gclean.py', 'tasks.py', 'pyven', 'release.py', 'runtests.py', 'travis_ci.py', 'pyven.py', 'toplevel.py', 'tests', 'foreignsyms'])
