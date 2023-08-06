import setuptools

setuptools.setup(
        name = 'Concern',
        version = '2',
        install_requires = ['aridity', 'lagoon', 'timelyOSC'],
        packages = setuptools.find_packages(),
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
        py_modules = [],
        scripts = ['Concern'])
