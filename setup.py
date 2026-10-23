from setuptools import find_packages, setup

setup(
    name='ieee7007',
    packages=find_packages(include=['ieee7007']),
    version='0.1.0',
    description='Library to work with the ontological standards defined on IEEE7007',
    author='hugo.cpolos@gmail.com',
    install_requires=['owlready2'],
    extras_require={'plot': ['networkx', 'matplotlib', 'pygraphviz']},
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    include_package_data=True,
)
