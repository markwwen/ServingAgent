from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='serving_agent',
    version="0.1.0",
    description='A middleware for model serving to speedup online inference.',
    author="wwen",
    author_email="wenwh@mail.sustech.edu.cn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
    ],
    keywords='serving_agent',
    url='https://github.com/HughWen/ServingAgent',
    packages=find_packages(exclude=['example', 'img', '.vscode']),
    python_requires='>=3.5',
    install_requires=['redis'],
    include_package_data=True,
    zip_safe=False,
)
