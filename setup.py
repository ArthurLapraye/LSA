#!/user/bin/python 

from cx_Freeze import setup, Executable

#Code tiré de http://www.developpez.net/forums/d1489444/autres-langages/python-zope/general-python/pyinstaller-cxfreeze-pur-utiliser-numpy-scipy-matplotlib/

includes = []  # nommer les modules non trouves par cx_freeze
excludes = []
packages = []  # nommer les packages utilises
# copier les fichiers non-Python et/ou repertoires et leur contenu:

setup(
    name = "",
    version = "0.7",
    description = "Ce programme permet la classification de réponses à des questions ouvertes",
    executables = [Executable("main.py")],
)