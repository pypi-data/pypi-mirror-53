from setuptools import setup, find_packages

setup(
    name="2feeds",
    version="1.0.210",
    description="A cli to read feeds",
    author="asif",
    author_email="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    keywords="rss cli urwid",

    packages=['feeds'],
    python_requires='>=3.7.4',
    install_requires=["feedparser==5.2.1", "urwid==2.0.1"],

    entry_points={
        'console_scripts': [
            '2feeds = feeds.main:_start'
        ]
    },

    project_urls={
        "Source Code": "https://github.com/asif42/feed-reader",
    },

)
