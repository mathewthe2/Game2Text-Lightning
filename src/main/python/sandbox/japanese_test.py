import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from japanese import initLanguage

translator = initLanguage()
term = translator.findTerm('家のお使いだったから')
print(term[0])

assert(term[0][0]['expression'] == '家')
assert(term[0][0]['reading'] == 'いえ')
assert('home' in list(term[0][0]['glossary'])[0])