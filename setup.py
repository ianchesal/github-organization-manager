from setuptools import setup

setup(
    name='github-organization-manager',
    version='0.1',
    py_modules=['gom'],
    include_package_data=True,
    install_requires=[
        'click',
        'pygithub',
    ],
    entry_points='''
        [console_scripts]
        gom=gom:cli
    ''',
)
