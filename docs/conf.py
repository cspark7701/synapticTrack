import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'synaptictrack'
copyright = '2025, Chong Shik Park'
author = 'Chong Shik Park'
release = '0.1.0'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']

