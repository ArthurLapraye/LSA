#!/usr/bin/python 
#-*- encoding: utf-8 -*-


import sys,os

from cx_Freeze import setup, Executable

#Code tiré de http://www.developpez.net/forums/d1489444/autres-langages/python-zope/general-python/pyinstaller-cxfreeze-pur-utiliser-numpy-scipy-matplotlib/
#http://python.jpvweb.com/mesrecettespython/doku.php?id=cx_freeze

includes = [
			#"scipy.special._ufuncs"
			]  # nommer les modules non trouves par cx_freeze
excludes = ["tkinter","Tkinter","collections.abc","collections.sys"]
packages = []  # nommer les packages utilises
# copier les fichiers non-Python et/ou repertoires et leur contenu:

# copier les fichiers non-Python et/ou repertoires et leur contenu:
import scipy,numpy, scipy.special._ufuncs

includefiles = [os.path.dirname(scipy.__file__),
      #  os.path.dirname(scipy.__file__),
		os.path.dirname(scipy.special._ufuncs.__file__),
		
		"lefff-3.4.mlex",
		"xtal.png"
		]

excludefiles = [] 
"""
Icone sous Windows: il faut:
=> un xxx.ico pour integration dans le exe, avec "icon=xxx.ico"
=> un xxx.png pour integration avec PyQt4 + demander la recopie avec includefiles.
"""
 
#############################################################################
# preparation des options
 
# chemins de recherche des modules
# ajouter d'autres chemins (absolus) si necessaire: sys.path + ["chemin1", "chemin2"]
path = sys.path
xtalwin32=Executable("main.py",icon="xtal.ico", base="Win32GUI") 
if sys.platform == "win32":
    #pass
    includefiles += [r"C:\Python27\Lib\site-packages\scipy\special\_ufuncs.pyd"] 
    #: ajouter les recopies specifiques à Windows
elif sys.platform == "linux2":
    pass
    # includefiles += [...] : ajouter les recopies specifiques à Linux
else:
    pass
    # includefiles += [...] : cas du Mac OSX non traite ici
 
# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]
 
# niveau d'optimisation pour la compilation en bytecodes
optimize = 0
# [('path2python\\Lib\\site-packages\\scipy\\special\\_ufuncs.pyd','_ufuncs.pyd')]

options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes,
           "create_shared_zip": False,  # <= ne pas generer de fichier zip
           "include_in_shared_zip": False,  # <= ne pas generer de fichier zip
           "compressed": False,  # <= ne pas generer de fichier zip
           "optimize": optimize,
           #"silent": silent
           }

		   
# pour inclure sous Windows les dll system de Windows necessaires
if sys.platform == "win32":
    options["include_msvcr"] = True
 


setup(
    name = "X-TAL",
    version = "0.7",
	author="Arthur Lapraye",
	 options={"build_exe": options},
    description = "Ce programme permet la classification de réponses à des questions ouvertes",
    executables = [xtalwin32],	)
