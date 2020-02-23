from setuptools import setup

setup(
    name='github-organization-manager',
    version='0.1',
    py_modules=['gom'],
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'click',
        'pygithub',
    ],
    entry_points='''
        [console_scripts]
        gom=gom:cli
    ''',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'httpretty'],
)
