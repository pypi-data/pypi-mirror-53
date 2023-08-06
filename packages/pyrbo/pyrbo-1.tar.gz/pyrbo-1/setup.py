import setuptools

setuptools.setup(
        name = 'pyrbo',
        version = '1',
        install_requires = ['numpy', 'cython', 'nativecommon'],
        packages = setuptools.find_packages(),
        py_modules = ['pyrbo'],
        scripts = [])
