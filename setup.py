from setuptools import find_packages, setup

setup(
    name='avenues',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click>=7.1.2',
        'Flask>=1.1.2',
        'itsdangerous>=1.1.0',
        'Jinja2>=2.11.2',
        'MarkupSafe>=1.1.1',
        'numpy>=1.18.4',
        'pandas>=1.0.3',
        'python-dateutil>=2.8.1',
        'pytz>=2020.1',
        'six>=1.14.0',
        'Werkzeug>=1.0.1'
    ],
)
