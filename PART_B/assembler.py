"""Hack assembler (Nand to Tetris) - K = 67, K mod 3 = 1
"""
import sys

COMP = {'0':'0101010','1':'0111111','-1':'0111010','D':'0001100','A':'0110000',
 '!D':'0001101','!A':'0110001','-D':'0001111','-A':'0110011','D+1':'0011111',
 'A+1':'0110111','D-1':'0001110','A-1':'0110010','D+A':'0000010','D-A':'0010011',
 'A-D':'0000111','D&A':'0000000','D|A':'0010101',
 'M':'1110000','!M':'1110001','-M':'1110011','M+1':'1110111','M-1':'1110010',
 'D+M':'1000010','D-M':'1010011','M-D':'1000111','D&M':'1000000','D|M':'1010101'}
DEST = {'':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}
JUMP = {'':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}


def predefined():
    s = {'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,'SCREEN':16384,'KBD':24576}
    s.update({f'R{i}': i for i in range(16)})
    return s


def clean(line):
    """Remove comments and all whitespace."""
    return line.split('//')[0].replace(' ', '').replace('\t', '').strip()


def assemble(path):
    symbols = predefined()
    lines = [(n, clean(l)) for n, l in enumerate(open(path), 1)]
    lines = [(n, l) for n, l in lines if l]          # drop blank/comment lines
    errors = []

    # PASS 1: record label addresses
    pc, code = 0, []
    for n, l in lines:
        if l.startswith('('):
            if not l.endswith(')') or len(l) < 3:
                errors.append(f"Line {n}: invalid instruction '{l}'")
                continue
            symbols[l[1:-1]] = pc
        else:
            code.append((n, l))
            pc += 1

    # PASS 2: translate to 16-bit binary; new variables start at RAM[16]
    nxt, out = 16, []
    for n, l in code:
        try:
            if l.startswith('@'):
                v = l[1:]
                if v == '':
                    raise ValueError
                if v.isdigit():
                    val = int(v)
                    if val > 32767:
                        raise ValueError
                else:
                    if v[0].isdigit():
                        raise ValueError
                    if v not in symbols:
                        symbols[v] = nxt
                        nxt += 1
                    val = symbols[v]
                out.append(format(val, '016b'))
            else:
                dest, comp, jmp = '', l, ''
                if '=' in comp:
                    dest, comp = comp.split('=', 1)
                if ';' in comp:
                    comp, jmp = comp.split(';', 1)
                out.append('111' + COMP[comp] + DEST[dest] + JUMP[jmp])
        except (KeyError, ValueError):
            errors.append(f"Line {n}: invalid instruction '{l}'")

    for e in errors:
        print(e)
    return None if errors else out


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python assembler.py File.asm")
        sys.exit(1)
    f = sys.argv[1]
    result = assemble(f)
    if result is None:
        print("Assembly failed.")
        sys.exit(1)
    open(f.rsplit('.', 1)[0] + '.hack', 'w').write('\n'.join(result) + '\n')
    print(f"OK: {len(result)} instructions written.")