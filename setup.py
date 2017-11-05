from setuptools import setup

setup(
    name='interpret_z',
    packages=['interpret_z'],
    version='0.0.2',
    description='A lightweight compiler for Sailthru\'s Zephyr scripting language',
    author='Ian Hoffman',
    author_email='ianhoffman10@gmail.com',
    url='https://github.com/ianhoffman/interpret_z',
    license='MIT',
    download_url='https://github.com/ianhoffman/interpret_z/archive/0.1.1.tar.gz',
    keywords='zephyr, sailthru, compiler, interpreter, parser, scanner',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 3 - Alpha',
	'Intended Audience :: Developers',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Testing',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6',
    ]
)

