import gdb
import re
import os

FN_REGEX = r'[0-9]+:\s+\w+\s(\w+)\((?:\([^()]*\)|.)*\)'
DIRECTORY = 'hal/stm32f0xx/Src'
OUTFILE = 'hal/functions.txt'


def process_file(f, out):
    '''
    Write symbols to redefine to the out file.
    Format is "old_symbol new_symbol".
    Do this for each function found in object file.
    '''
    gdb.execute('file %s' % f, False, False)
    info = gdb.execute('info functions', False, True)

    for line in info.splitlines():
        m = re.search(FN_REGEX, line)
        if m:
            sym = m.group(1)
            out.write('{0} {1}_{0}\n'.format(sym, prefix))  # noqa: F821


gdb.execute('set pagination off')
with open(OUTFILE, 'w') as out:
    for f in os.listdir(DIRECTORY):
        if f.endswith('.o'):
            process_file(os.path.join(DIRECTORY, f), out)

gdb.execute('quit')
