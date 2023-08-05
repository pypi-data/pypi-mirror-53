from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    # This name that you pip/pipenv install
    # Also the name that appears in the top banner with version
    name='forestry',
    version='0.0.2',  # Removed Forestry from Pipfile
    # Identifies the code base by identifying the top level packages
    packages=['forestry'],
    # Appears in project links
    url='https://github.com/dwightdc/forestry',
    license='MIT',
    # Forms the author/email tag
    author='Dwight D. Cummings',
    author_email='dwight.cummings@yahoo.com',
    # Description appears in the second grey banner
    description='Python Tree data structures and tools.',
    # Appears in the right pane
    long_description=readme(),
    long_description_content_type='text/markdown',
    # classifiers section
    classifiers=[
        "Programming Language :: Python :: 3.7"
    ]
)
