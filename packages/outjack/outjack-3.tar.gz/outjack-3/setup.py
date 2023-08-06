import setuptools

setuptools.setup(
        name = 'outjack',
        version = '3',
        install_requires = ['cython', 'nativecommon'],
        packages = setuptools.find_packages(),
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld']},
        py_modules = [],
        scripts = [])
