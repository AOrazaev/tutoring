"""
Given a string which looks like 2[abc]3[t]
produce string which looks like:
    abcabcttt
by repeating string inside brackets.

Brackets can be nested. Input guaranteed to be correct.

Few more exmaples:
    >>> multiply_string('2[abc]3[t]')
    'abcabcttt'

    >>> multiply_string('')
    ''

    >>> multiply_string('4[ab2[xy]]3[gz]')
    'abxyxyabxyxyabxyxyabxyxygzgzgz'

    >>> multiply_string('0[ab2[xy]]3[gz]')
    'gzgzgz'

    >>> multiply_string('13[u]')
    'uuuuuuuuuuuuu'
"""

def multiply_string(s: str) -> str:
    stack = [[1, '']]
    number = ''

    for ch in s:
        if ch.isdigit():
            number += ch
            continue

        if ch == '[':
            stack.append([int(number), ''])
            number = ''
            continue

        if ch == ']':
            num, ss = stack.pop()
            stack[-1][1] += num * ss
            continue

        stack[-1][1] += ch

    return stack[0][1]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
