import setuptools

setuptools.setup(
        name = 'outjack',
        version = '2',
        install_requires = ['cython', 'nativecommon'],
        packages = setuptools.find_packages(),
        package_data = {'': ['*.pyx', '*.pxd']},
        py_modules = [],
        scripts = [])
