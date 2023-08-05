import os
from setuptools import setup

# ezcurses
# library to help with curses programming


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = []
if os.name == 'nt':
    # Windows users will need unicurses.
    requirements = ['unicurses']


setup(
    name="ezcurses",
    version="0.3.1",
    description="library to help with curses programming",
    author="Johan Nestaas",
    author_email="johannestaas@gmail.com",
    license="GPLv3+",
    keywords="",
    url="https://www.bitbucket.org/johannestaas/ezcurses",
    packages=['ezcurses'],
    package_dir={'ezcurses': 'ezcurses'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=requirements,
)
