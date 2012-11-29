import os

from distutils.core import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == "":
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

package_dir = "rdns"

packages = []
for dirpath, dirnames, filenames in os.walk(package_dir):
    # ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith("."):
            del dirnames[i]
    if "__init__.py" in filenames:
        packages.append(".".join(fullsplit(dirpath)))

setup(
    name='rdns',
    version='1.2',
    description='Reverse IP Hosts Lookup; Give IPs, Get Hosts',
    keywords='reverse domain name lookup',
    license='MIT License',
    author='Alex Goretoy',
    author_email='alex@goretoy.com',
    maintainer='Alex Goretoy',
    maintainer_email='alex@goretoy.com',
    url='http://github.com/gxela/rdns.py',
    dependency_links=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        "Intended Audience :: End Users/Desktop",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: Utilities"
    ],
    packages=packages,
    include_package_data=True,
    install_requires=read("requirements.txt").split("\n")
)
