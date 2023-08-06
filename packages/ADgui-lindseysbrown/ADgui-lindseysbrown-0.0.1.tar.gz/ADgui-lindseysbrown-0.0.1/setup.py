import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name= 'ADgui-lindseysbrown',
        version='0.0.1',
        author = 'Lindsey Brown, Xinyue Wang',
        author_email="lindsey_brown@g.harvard.edu",
        description='A GUI for learning automatic differentiation',
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        url='https://github.com/CS207-AD20/AD20_GUI',
        packages = setuptools.find_packages(),
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6'
)
