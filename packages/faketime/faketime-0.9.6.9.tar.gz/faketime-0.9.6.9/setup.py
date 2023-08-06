# -*- coding: utf-8 -*
from os.path import join, realpath, dirname, exists, abspath
from setuptools.command.install import install
from setuptools import find_packages
from setuptools import setup
import subprocess
import faketime
import codecs
import sys
import os


class CustomInstall(install):
    def run(self):
        """Compile libfaketime."""
        if sys.platform == "linux" or sys.platform == "linux2":
            libname = 'libfaketime.so.1'
            libnamemt = 'libfaketimeMT.so.1'
        elif sys.platform == "darwin":
            libname = 'libfaketime.1.dylib'
            libnamemt = 'libfaketimeMT.1.dylib'
        else:
            sys.stderr.write("WARNING : libfaketime does not support platform {}\n".format(sys.platform))
            sys.stderr.flush()
            return

        faketime_lib = join('faketime', libname)
        faketime_lib_mt = join('faketime', libnamemt)
        self.my_outputs = []

        setup_py_directory = dirname(realpath(__file__))
        faketime_directory = join(setup_py_directory, "faketime")
        os.chdir(faketime_directory)
        if sys.platform == "linux" or sys.platform == "linux2":
            subprocess.check_call(['make',])
        else:
            os.chdir(setup_py_directory)
            if "10.12" in subprocess.check_output(["sw_vers", "-productVersion"]).decode('utf8'):
                self.copy_file(
                    join('faketime', "libfaketime.c.sierra"),
                    join('faketime', "libfaketime.c")
                )

            os.chdir(faketime_directory)
            subprocess.check_call(['make', '-f', 'Makefile.OSX'])
        os.chdir(setup_py_directory)

        dest = join(self.install_purelib, dirname(faketime_lib))
        dest_mt = join(self.install_purelib, dirname(faketime_lib_mt))

        try:
            os.makedirs(dest)
        except OSError as e:
            if e.errno != 17:
                raise
        self.copy_file(faketime_lib, dest)

        if exists(faketime_lib_mt):
            self.copy_file(faketime_lib_mt, dest_mt)
        self.my_outputs.append(join(dest, libname))

        install.run(self)

    def get_outputs(self):
        outputs = install.get_outputs(self)
        outputs.extend(self.my_outputs)
        return outputs



def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)) as f:
        return f.read()


setup(name="faketime",
      version=read('VERSION').replace('\n', ''),
      description="Libfaketime wrapper.",
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Libraries',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      keywords='libfaketime faketime',
      author='Colm O\'Connor',
      author_email='colm.oconnor.github@gmail.com',
      url='https://github.com/hitchdev/faketime/',
      license='GPLv2',
      install_requires=[],
      packages=find_packages(exclude=["docs", "*.so.1", "*.1.dylib", ]),
      package_data={},
      zip_safe=False,
      include_package_data=True,
      cmdclass={'install': CustomInstall},
)
