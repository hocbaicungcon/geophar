# -*- coding: utf-8 -*-
from __future__ import division # 1/2 == .5 (par defaut, 1/2 == 0)

#    WxGeometrie
#    Dynamic geometry, graph plotter, and more for french mathematic teachers.
#    Copyright (C) 2005-2013  Nicolas Pourcelot
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


# Ce module sert à tester que toutes les dépendances sont satisfaites,
# et à y remédier dans le cas contraire (si possible).

import sys, imp, platform

# ------------------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------------------

from .version import NOMPROG

# Les valeurs sont les noms des paquets sous Debian/Ubuntu.
dependances = {'PyQt4': 'python-qt4',
               'matplotlib': 'python-matplotlib',
               'scipy': 'python-scipy',
               'numpy': 'python-numpy',
               'mpmath': 'python-mpmath',
               'sip': 'python-sip',
               'PyQt4.Qsci': 'python-qscintilla2',
               }

python_version_min = (2, 6)
python_version_max = (2, 7)

plateforme = platform.system() #'Windows' ou 'Linux' par exemple.

# Paramètres de matplotlib
# Utiliser une installation LaTeX existante (meilleur rendu mais très lent !)
latex = False
latex_unicode = True
moteur_de_rendu = 'Qt4Agg'

# ------------------------------------------------------------------------------


def tester_dependances():
    if hasattr(sys, 'frozen'):
        # Ne pas faire ces tests avec py2exe/py2app/CxFreeze (non seulement inutiles, mais en plus ils échouent).
        return
    # Make sure I have the right Python version.
    version_python_supportee = True
    if sys.version_info[:2] < python_version_min:
        print(u" ** Erreur fatale **")
        print(NOMPROG + u" nécessite Python %d.%d au minimum." % python_version_min)
        version_python_supportee = False
    elif sys.version_info[:2] > python_version_max:
        print(u" ** Erreur fatale **")
        print(NOMPROG + u" supporte Python %d.%d au maximum." % python_version_max)
        version_python_supportee = False

    if not version_python_supportee:
        print(u"Python %d.%d détecté." % sys.version_info[:2])
        sys.exit(-1)

    # Test for dependencies:
    modules_manquants = []
    for module in dependances:
        module_name = module
        try:
            # imp.find_module() doesn't support submodules.
            path = None
            while '.' in module:
                module, submodule = module.split('.', 1)
                f, filename, description = imp.find_module(module, path)
                module = submodule
                path = [filename]
            imp.find_module(module, path)
        except ImportError:
            modules_manquants.append(module_name)

    if modules_manquants and plateforme == 'Linux':
        paquets = [dependances[module] for module in modules_manquants]
        import dbus
        try:
            bus = dbus.SessionBus()
            try:
                proxy = bus.get_object('org.freedesktop.PackageKit', '/org/freedesktop/PackageKit')
                iface = dbus.Interface(proxy, 'org.freedesktop.PackageKit.Modify')
                iface.InstallPackageNames(dbus.UInt32(0), paquets, "show-confirm-search,hide-finished", timeout=1000)
                modules_manquants = []
            except dbus.DBusException, e:
                print 'Unable to use PackageKit: %s' % str(e)
        except dbus.DBusException, e:
            print 'Unable to connect to dbus: %s' % str(e)

    if modules_manquants:
        print(u'** Erreur fatale **\nLes modules suivants sont introuvables !')
        print(u'MODULE(S) MANQUANT(S): %s.' % ', '.join(modules_manquants))
        sys.exit(-1)


def configurer_dependances():
    # ---------------------
    # Configuration de PyQt
    # ---------------------
    # Le module sip doit être importé très tôt, avant Qt bien sûr,
    # mais bizarrement également avant sympy (depuis sympy 0.7.5 au moins).
    try:
        import sip
        # PyQt new API (PyQt 4.6+)
        sip.setapi('QDate', 2)
        sip.setapi('QDateTime', 2)
        sip.setapi('QString', 2)
        sip.setapi('QTextStream', 2)
        sip.setapi('QTime', 2)
        sip.setapi('QUrl', 2)
        sip.setapi('QVariant', 2)
    except ImportError:
        print("Warning: sip not found.")

    # ---------------------------
    # Configuration de Matplotlib
    # ---------------------------
    try:
        # Cx_Freeze version needs this (so that matplotlib can found pyparsing).
        import pyparsing
    except ImportError:
        pass
    import matplotlib
    matplotlib.use(moteur_de_rendu, warn=False)
    matplotlib.rcParams['text.usetex'] = latex
    matplotlib.rcParams["text.latex.unicode"] = latex_unicode

    # A changer *avant* d'importer pylab ?
    matplotlib.rcParams['font.family'] ='serif'
    #matplotlib.rcParams['font.sans-serif'] ='STIXGeneral'
    matplotlib.rcParams['font.serif'] ='STIXGeneral'
    #matplotlib.rcParams['font.monospace'] ='STIXGeneral'
    matplotlib.rcParams['mathtext.fontset'] ='stix'

    # import pylab_ as pylab
    # le fichier pylab_.py est modifie lors d'une "compilation" avec py2exe
