from distutils.core import setup
import setuptools
import atexit
from distutils.command.install import install

class PostInstallCommand(install):
      def run(self):
            import os
            import shutil
            import mangrove
            install.run(self)
            print("WHAAAAAAAAAAAAAAAAAAAAAAAAAAT")
            try:
                  DESKTOP_FOLDER = os.path.join(os.getenv("HOMEPATH"), "Desktop")
                  NAME = "Mangrove"

                  if sys.argv[1] == '-install':
                        create_shortcut(
                              target=os.path.join(sys.prefix, 'python.exe') + " " + os.path.join(os.path.dirname(mangrove.__file__), "mgvUI.py"),
                              description="Mangrove UI",
                              filename=NAME,
                              workdir=DESKTOP_FOLDER,
                              iconpath=os.path.join(os.path.dirname(mangrove.__file__),"icons","mgv.ico"))

                        shutil.move(os.path.join(os.getcwd(), NAME), os.path.join(DESKTOP_FOLDER, NAME))
                        #file_created(os.path.join(DESKTOP_FOLDER, NAME))

                  if sys.argv[1] == '-remove':
                      pass
            except:
                  pass
            

setup(name='mgv',
      version='1.0.30',
      scripts=['mgv'],
      description='An open-source nodal pipeline manager',
      long_description="""Mangrove is a simple tool to help you to manage your projects.
It's has been thought to be used by every one, from scholar teams to private companies, with or without any technical skills.
With a clean and intuitive interface, users create, open, connect or version data easily
without any knowledge of the nomenclatures and the data structure.
Based on a nodal interface, you plug pre-scripted nodes by your own TDs or the community to create and manage your files.
Originaly created for 3d post production ease, it's widely open and can be used for a non limited type of projects.""",
      url='https://gitlab.com/TheYardVFX/mangrove',
      author='Bekri Djelloul',
      author_email='mangrove@theyard-vfx.com',
      license='LGPL v3',
      packages=setuptools.find_packages(),
      install_requires=['xlrd', 'PySide', 'Qt.py', 'pymongo', 'firebase_admin'],
      include_package_data=True,
      cmdclass={'install': PostInstallCommand})
