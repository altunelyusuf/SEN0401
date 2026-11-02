#!/usr/bin/env python3
"""mock_numeric_gen_ch4x v1.0.0 - generator of the hash-search family of numeric templates (chapter 4 extra).
Every key value, step number and wrong value is computed here; nothing is typed in by hand except the parameter lists.
Usage: python3 -I mock_numeric_gen_ch4x_v1_0_0.py --out PATH.json"""
import sys, json

WHY_QUESTION = ("Why this question: mining is a search that nobody can shorten except by accepting more results, "
                "and anyone can check an answer with one hash. Counting the tries shows why a bigger target makes "
                "mining faster and a smaller one slower.")

def f(x): return '{:,}'.format(x)

def wrongs(cands, key):
    out, seen = [], {key}
    for v, why in cands:
        if isinstance(v, int) and 0 < v <= 99999 and v not in seen:
            seen.add(v); out.append({'value': v, 'why': why})
        if len(out) == 3: break
    assert len(out) == 3, (key, cands)
    return out

RULE_POW = 'A hash with {n} bits has 2 to the power {n} possible results.'

# ---- template 1: average tries for one given result (one step)
def t1(n):
    P = 2 ** n
    stems = ['A hash function gives results of %d bits. A hash with %d bits has 2 to the power %d possible results. A search computes one hash per try to find one given result, and on average needs as many tries as there are possible results. You are asked to calculate the average number of tries.' % (n, n, n),
             'A hash function turns any input into a result of %d bits. A hash with %d bits has 2 to the power %d possible results. To find one given result, a search makes one hash per try and needs on average as many tries as there are possible results. You are asked to calculate the average number of tries needed.' % (n, n, n)]
    c = [(2 * n, 'Multiplied the number of bits by 2 instead of raising 2 to the power of the bits.'),
         (2 ** (n - 1), 'Used one bit too few, so the answer is half of the possible results.'),
         (n * n, 'Squared the number of bits instead of raising 2 to the power of the bits.'),
         (2 ** (n + 1), 'Used one bit too many, so the answer is double the possible results.'),
         (P - 1, 'Subtracted one from the possible results, but the average equals the possible results.'),
         (n ** 3, 'Cubed the number of bits instead of raising 2 to the power of the bits.')]
    return stems, P, ['Possible results of the hash: 2 to the power %d = %s.' % (n, f(P)),
                      'Finding one given result takes on average as many tries as there are possible results: %s tries.' % f(P)], \
        'With %d bits there are %s possible results, and a search for one given result needs about that many tries.' % (n, f(P)), c

# ---- template 2: bits from number of results (one step)
def t2(n):
    N = 2 ** n
    stems = ['A hash function has %s possible results. Each extra bit in the result doubles the number of possible results, and a hash with 1 bit has 2 possible results. You are asked to calculate how many bits the hash result has.' % f(N),
             'A hash function can give %s different results. Every added bit doubles the number of possible results, and 1 bit gives 2 possible results. You are asked to calculate how many bits the hash result has.' % f(N)]
    c = [(N, 'Gave the number of results instead of the number of bits.'),
         (n + 1, 'Counted one bit too many; doubling %d times from 1 bit stops at %d bits.' % (n - 1, n)),
         (n - 1, 'Counted only the doublings after the first bit; the first bit already gives 2 results.'),
         (N // 2, 'Halved the number of results instead of counting the doublings.'),
         (2 * n, 'Doubled the number of bits after counting them.'),
         (N - 1, 'Subtracted one from the results instead of counting the doublings.')]
    return stems, n, ['Each bit doubles the results, so the results are 2 to the power of the bits: 2 to the power %d = %s.' % (n, f(N)),
                      'The result count %s matches 2 to the power %d, so the hash has %d bits.' % (f(N), n, n)], \
        '%s is 2 multiplied by itself %d times, so the hash has %d bits.' % (f(N), n, n), c

# ---- template 3: seconds from tries and speed (one step)
def t3(r, s):
    T = r * s
    stems = ['A machine makes %d tries per second, and each try is one hash. A search needs %s tries in total. Seconds equal tries divided by tries per second. You are asked to calculate the number of seconds the search takes.' % (r, f(T)),
             'A search needs %s tries in total, and each try is one hash. The machine makes %d tries per second. Seconds equal tries divided by tries per second. You are asked to calculate how many seconds the search takes.' % (f(T), r)]
    c = [(T, 'Gave the number of tries instead of seconds; the division by the speed is missing.'),
         (T * r, 'Multiplied the tries by the speed instead of dividing.'),
         (T - r, 'Subtracted the speed from the tries instead of dividing.'),
         (s + r, 'Added the speed to the correct number of seconds.'),
         (T + r, 'Added the speed to the tries instead of dividing.')]
    return stems, s, ['Total tries: %s. Speed: %d tries per second.' % (f(T), r),
                      'Seconds = tries divided by tries per second = %s / %d = %s seconds.' % (f(T), r, f(s))], \
        'A machine that makes %d tries every second needs %s divided by %d seconds for %s tries.' % (r, f(T), r, f(T)), c

# ---- template 4: average tries, k accepted results (two steps)
def t4(n, k):
    P = 2 ** n; key = P // k
    stems = ['A hash with %d bits has 2 to the power %d possible results. The search accepts any result in a set of %d results, so on average the tries needed equal the possible results divided by the accepted results. You are asked to calculate the average number of tries.' % (n, n, k),
             'A hash has %d bits, so it has 2 to the power %d possible results. A search stops at any result in a set of %d results, and on average needs as many tries as the possible results divided by the accepted results. You are asked to calculate the average number of tries.' % (n, n, k)]
    c = [(P, 'Forgot to divide by the number of accepted results.'),
         (P * k, 'Multiplied by the accepted results instead of dividing.'),
         (P - k, 'Subtracted the accepted results instead of dividing.'),
         (key * 2, 'Divided by half of the accepted results.'),
         (key // 2, 'Divided by twice the accepted results.'),
         (n * k, 'Multiplied the bits by the accepted results instead of using 2 to the power of the bits.')]
    return stems, key, ['Possible results: 2 to the power %d = %s.' % (n, f(P)),
                        'Accepted results: %d. Average tries = %s / %d = %s.' % (k, f(P), k, f(key))], \
        'Accepting %d results makes each try %d times as likely to succeed, so the %s possible results shrink to %s tries.' % (k, k, f(P), f(key)), c

# ---- template 5: seconds for one given result (two steps)
def t5(n, r):
    P = 2 ** n; key = P // r
    stems = ['A hash with %d bits has 2 to the power %d possible results. A search for one given result needs on average as many tries as there are possible results. The machine makes %d tries per second. You are asked to calculate the average number of seconds the search takes.' % (n, n, r),
             'A machine makes %d tries per second. It searches for one given result of a hash with %d bits, which has 2 to the power %d possible results, and needs on average as many tries as there are possible results. You are asked to calculate the average number of seconds the search takes.' % (r, n, n)]
    c = [(P, 'Gave the number of tries instead of seconds; the division by the speed is missing.'),
         (P * r, 'Multiplied the tries by the speed instead of dividing.'),
         (P - r, 'Subtracted the speed from the tries instead of dividing.'),
         (key * 2, 'Divided by half of the speed.'),
         (key // 2, 'Divided by twice the speed.'),
         (n * r, 'Multiplied the bits by the speed instead of using 2 to the power of the bits.')]
    return stems, key, ['Possible results: 2 to the power %d = %s, so about %s tries.' % (n, f(P), f(P)),
                        'Seconds = tries divided by tries per second = %s / %d = %s seconds.' % (f(P), r, f(key))], \
        'The search makes %s tries, and a machine making %d tries every second finishes them in %s seconds.' % (f(P), r, f(key)), c

# ---- template 6: seconds, k accepted results (three steps)
def t6(n, k, r):
    P = 2 ** n; tries = P // k; key = tries // r
    assert P % (k * r) == 0
    stems = ['A hash with %d bits has 2 to the power %d possible results. The search accepts any result in a set of %d results, so the average tries equal the possible results divided by the accepted results. The machine makes %d tries per second. You are asked to calculate the average number of seconds the search takes.' % (n, n, k, r),
             'A machine makes %d tries per second. It searches a hash with %d bits, which has 2 to the power %d possible results, and stops at any result in a set of %d results. The average tries equal the possible results divided by the accepted results. You are asked to calculate the average number of seconds the search takes.' % (r, n, n, k)]
    c = [(P // r, 'Forgot to divide by the number of accepted results.'),
         (tries, 'Gave the average tries instead of seconds; the division by the speed is missing.'),
         (P * k // r, 'Multiplied by the accepted results instead of dividing.'),
         (tries * r, 'Multiplied the tries by the speed instead of dividing.'),
         (P, 'Gave all possible results; both divisions are missing.'),
         (key * 2, 'Divided by half of the accepted results or of the speed.'),
         (key // 2, 'Divided by twice the accepted results or the speed.'),
         (key + r, 'Added the speed to the correct number of seconds.')]
    return stems, key, ['Possible results: 2 to the power %d = %s.' % (n, f(P)),
                        'Average tries = possible results / accepted results = %s / %d = %s.' % (f(P), k, f(tries)),
                        'Seconds = tries / tries per second = %s / %d = %s seconds.' % (f(tries), r, f(key))], \
        'Accepting %d results cuts the %s possible results to %s tries, and %d tries per second turn those tries into %s seconds.' % (k, f(P), f(tries), r, f(key)), c

# ---- template 7: speed needed (two steps)
def t7(n, s):
    P = 2 ** n; key = P // s
    stems = ['A hash with %d bits has 2 to the power %d possible results. A search for one given result needs on average as many tries as there are possible results. It must finish in %d seconds on average. You are asked to calculate how many tries per second the machine must make.' % (n, n, s),
             'A search for one given result of a hash with %d bits, which has 2 to the power %d possible results, needs on average as many tries as there are possible results. It must take %d seconds on average. You are asked to calculate how many tries per second the machine must make.' % (n, n, s)]
    c = [(P, 'Gave the number of tries instead of tries per second; the division by the seconds is missing.'),
         (P * s, 'Multiplied the tries by the seconds instead of dividing.'),
         (P - s, 'Subtracted the seconds from the tries instead of dividing.'),
         (key * 2, 'Divided by half of the seconds.'),
         (key // 2, 'Divided by twice the seconds.')]
    return stems, key, ['Possible results: 2 to the power %d = %s, so about %s tries.' % (n, f(P), f(P)),
                        'Tries per second = tries divided by seconds = %s / %d = %s.' % (f(P), s, f(key))], \
        'A speed is tries divided by time, so %s tries in %d seconds need %s tries every second.' % (f(P), s, f(key)), c

# parameter lists (all different per instance; keys all different within a template)
TEMPLATES = [
    ('n4x_1', t1, [(3,), (4,), (6,), (7,), (9,), (10,), (11,), (13,)], 'tries', 'Every added bit doubles the number of possible results.', False),
    ('n4x_2', t2, [(3,), (4,), (6,), (7,), (9,), (10,), (13,), (14,)], 'bits', 'Count how many times 2 is doubled to reach the results.', False),
    ('n4x_3', t3, [(3, 90), (5, 240), (6, 175), (9, 600), (12, 350), (15, 480), (20, 1250), (40, 375)], 'seconds', 'Divide the tries by the tries made in one second.', False),
    ('n4x_4', t4, [(6, 4), (8, 2), (9, 8), (10, 4), (11, 2), (13, 4), (14, 32), (15, 8)], 'tries', 'More accepted results mean fewer tries on average.', False),
    ('n4x_5', t5, [(8, 4), (9, 2), (10, 2), (11, 16), (13, 4), (14, 2), (15, 32), (16, 4)], 'seconds', 'First count the tries, then turn the tries into seconds.', False),
    ('n4x_6', t6, [(13, 4, 32), (14, 2, 64), (15, 4, 32), (11, 2, 2), (16, 2, 32), (16, 2, 16), (15, 2, 4), (9, 8, 4)], 'seconds', 'Divide by the accepted results first, then by the speed.', True),
    ('n4x_7', t7, [(8, 4), (10, 8), (13, 32), (11, 4), (15, 32), (14, 8), (16, 16), (16, 8)], 'tries per second', 'A speed is the number of tries divided by the seconds.', False),
]

def build():
    items = []
    for tid, fn, plist, unit, tip, c4 in TEMPLATES:
        inst = []
        for j, p in enumerate(plist):
            stems, key, steps, why, cands = fn(*p)
            inst.append({'stem': stems[j % 2], 'key_value': key, 'steps': steps, 'why_right': why,
                         'common_wrong': wrongs(cands, key)})
        items.append({'id': tid, 'type': 'numeric', 'chapter': 4, 'points': 3, 'can_be_4': c4, 'unit': unit,
                      'tip': tip, 'why_question': WHY_QUESTION, 'instances': inst})
    return {'chapter': 4, 'family': 'hash_search', 'items': items}

if __name__ == '__main__':
    out = sys.argv[sys.argv.index('--out') + 1]
    d = build()
    with open(out, 'w') as fh: json.dump(d, fh, indent=1, ensure_ascii=False)
    print('wrote %s: %d templates, %d instances' % (out, len(d['items']), sum(len(i['instances']) for i in d['items'])))
