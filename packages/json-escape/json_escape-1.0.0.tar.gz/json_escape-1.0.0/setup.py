from setuptools import setup


setup(
    name='json_escape',
    version='1.0.0',
    packages=['json_escape'],
    entry_points={
        'console_scripts': [
            'je=json_escape.json_escape:main'
        ]
    },
    install_requires=['Click==7.0'],
    description='Json escape',
    long_description="""
        String escape/unescape json files
    """,
    author='Alexandru Obada',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)
