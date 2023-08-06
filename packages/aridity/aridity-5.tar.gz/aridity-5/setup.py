import setuptools

setuptools.setup(
        name = 'aridity',
        version = '5',
        install_requires = ['pyparsing'],
        packages = setuptools.find_packages(),
        py_modules = ['aridity', 'arid_config'],
        scripts = ['aridity.py', 'arid-config'])
