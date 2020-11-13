import itertools


def empty_check(re, st):
    if not re:
        return True
    if not st:
        return False


def match_char(re, st):
    global esc
    if '\\' in re:
        re = re.replace('\\\\', '\\')
    if not esc:
        if re == '.' or re == st:
            return True
    if re == st:
        return True
    return False


def match_init(re, st):
    if len(re) > 1 and len(st) > 1:
        return match_char(re[0], st[0]) and match_init(re[1:], st[1:])
    return match_char(re, st[0])


def match_substr(re, st, i=0):
    is_empty = empty_check(re, st)
    if is_empty is not None:
        return is_empty
    return match_init(re, st) or match_substr(re, st[i + 1:], i + 1)


def match_ends(re, st, esc_start=False, esc_end=False):
    global esc
    start_match = re.startswith('^')
    end_match = re.endswith('$')
    if start_match or end_match:
        re, st, esc_start, esc_end = escape_mgr(re, st)
    if '.' in re:
        i = re.index('.')
        if re[:i].endswith('\\'):
            re = re[:i-1] + re[i:]
            esc = True
    if start_match and end_match and not esc_start and not esc_end:
        re = re[1:-1]
        return len(st) == len(re) and match_init(re, st)
    if start_match and not esc_start:
        re = re[1:]
        return match_init(re, st)
    if end_match and not esc_end:
        re = re[:-1][::-1]
        st = st[::-1]
        return match_init(re, st)
    return match_substr(re, st)


def none_once(re):
    if '?' in re:
        i = re.index('?')
        if not re[:i].endswith('\\'):
            none = re[:i - 1] + re[i + 1:]
            once = re.replace('?', '')
            return none, once
        else:
            return [re[:i - 1] + re[i:]]
    else:
        return iter([])


def none_more(re, st):
    if '*' in re:
        i = re.index('*')
        char = re[i - 1]
        if char != '\\':
            free_str = re.split(char + '*')
            repeats = ((char * n) for n in range(len(st) + 1))
            return (char.join(free_str) for char in repeats)
        else:
            return re.replace('\\*', '*')
    else:
        return iter([])


def once_more(re, st):
    if '+' in re:
        i = re.index('+')
        char = re[i - 1]
        if char != '\\':
            free_str = re.split(char + '+')
            repeats = ((char * n) for n in range(1, len(st) + 1))
            return (char.join(free_str) for char in repeats)
        else:
            return re.replace('\\+', '+')
    else:
        return iter([])


def one_type_metachar(st):
    return any(match_ends(reg, st) for reg in
               itertools.chain(none_once(regex),
                               none_more(*rs),
                               once_more(*rs)))


def escape_mgr(re, st):
    global esc
    start_esc = False
    end_esc = False
    if re.startswith('\\^'):
        re = re[1:]
        start_esc = True
    if re.endswith('\\$'):
        re = re[:-2] + re[-1]
        end_esc = True
    return re, st, start_esc, end_esc


esc = None
rs = regex, string = input().split('|')

print(one_type_metachar(string) or match_ends(*rs))  # #
