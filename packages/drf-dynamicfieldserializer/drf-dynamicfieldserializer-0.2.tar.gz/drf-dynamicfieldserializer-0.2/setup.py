from setuptools import setup, find_packages

setup(
    name='drf-dynamicfieldserializer',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'Django >= 1.11',
        'djangorestframework >= 3.8.2'
    ],
    description='SalesForce wrapper',
    author='bzdvdn',
    author_email='bzdv.dn@gmail.com',
    url='https://github.com/bzdvdn/drf-dynamicfieldserializer.git',
    license='MIT',
    python_requires=">=3.6",
)
