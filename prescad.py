
def prescad(prefile):
    splitpoint = prefile.index('!PRESCAD!')
    r = [prefile[:splitpoint]]
    all_lines = prefile[splitpoint + 9:].split('\n')
    all_lines = [x for x in all_lines if x.lstrip()[:2] not in ('', '//')]
    pos = -2
    while pos + len(all_lines) >= 0:
        x = all_lines[pos]
        x = x[:x.index('=')].strip()
        for line in all_lines[pos+1:-1]:
            if x in line[line.index('=')+1:].strip():
                break
        else:
            if x not in all_lines[-1]:
                print "WARNING: unused parameter '" + x + "'"
                del all_lines[pos]
                continue
        pos -= 1
    func_num = 0
    parameters = []
    right_lines = []
    for x in all_lines[:-1]:
        parameters.append(x[:x.index('=')].strip())
        right_lines.append(x[x.index('=')+1:].strip())
    right_lines.append(all_lines[-1].strip())
    parameters_take = [[] for i in range(len(right_lines))]
    i = 0
    while i < len(parameters):
        p = parameters[i]
        last = None
        for j in range(i+1, len(right_lines)):
            if j != i+1 and parameters[j-1] == p:
                break
            if p in right_lines[j]:
                last = j
        if last is None:
            print "WARNING: parameter redefined before use: '" + parameters[i] + "'"
            del parameters[i]
            del right_lines[i]
            del parameters_take[i]
            continue
        for k in range(i+1, last+1):
            parameters_take[k].append(p)
        i += 1
    for i in range(len(right_lines) - 1):
        strings = ';'.join(['children(' + str(parameters_take[i].index(x)) + ')' for x in parameters_take[i+1][:-1]])
        if strings != '':
            strings += ';'
        nextline = right_lines[i]
        for j, newparam in enumerate(parameters_take[i]):
            nextline = nextline.replace(newparam, 'children(' + str(j) + ')')
        r.append('module prescadfunc' + str(i) + '() prescadfunc' + str(i+1) + '() {' + strings + nextline + '}')
    nextline = right_lines[-1]
    for j, newparam in enumerate(parameters_take[-1]):
        nextline = nextline.replace(newparam, 'children(' + str(j) + ')')
    r.append('module prescadfunc' + str(len(right_lines) - 1) + '() ' + nextline)
    r.append('prescadfunc0();')
    r.append('')
    return '\n'.join(r)

from sys import argv

if __name__ == '__main__':
    assert argv[1][-8:] == '.prescad'
    h = open(argv[1], 'r')
    f1 = h.read()
    h.close()
    f2 = prescad(f1)
    h2 = open(argv[1][:-8] + '.scad', 'w')
    h2.write(f2)
    h2.close()
