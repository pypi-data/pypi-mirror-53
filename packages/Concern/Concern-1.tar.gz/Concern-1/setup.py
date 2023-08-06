import setuptools

setuptools.setup(
        name = 'Concern',
        version = '1',
        install_requires = ['aridity', 'lagoon', 'timelyOSC'],
        packages = setuptools.find_packages(),
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid']},
        py_modules = ['Concern', 'Concern-zip'],
        scripts = ['Concern.py', 'Concern-zip.py'])
