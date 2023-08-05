from setuptools import setup, find_packages

setup(
    cffi_modules="glta/process_plink/_build.py:ffi",
    name='glta',
    version='2019.9.29',
    description='Genomic Longitudinal Trait Analysis Tool',
    long_description=open('README.rst').read(),
    author='Chao Ning',
    author_email='ningchao91@gmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url="https://github.com/chaoning/GLTA",
    include_package_data = True,
)


install_requires=[
    'numpy>=1.17.2',
    'pandas>=0.25.1',
    'scipy>=1.3.1',
    'cffi>=1.12.3',
    'pandas_plink>=2.0.1',
]
