def rrotate(s, n):
    n = n % len(s)
    return s[-n:] + s[:-n]

def repeat_to_match_len(s, l):
    assert len(s) > 0
    r = ""
    i = 0
    while len(r) < l:
        r += s[i]
        i += 1
        if i == len(s):
            i = 0
    return r

def minimize_period(period):
    print(period)
    # very inefficient, but I don't care
    for i in range(2, len(period)):
        prefix = period[:i]
        if repeat_to_match_len(prefix, len(period)) == period:
            return prefix
    return period

def minimize_prefix(prefix, period):
    while prefix:
        new_period = prefix[-1] + period[:-1]
        if new_period == rrotate(period, 1):
            period = new_period
            prefix = prefix[:-1]
        else:
            break
    return prefix, period

class PeriodicWord:
    def __init__(self, prefix, period):
        period = minimize_period(period)
        prefix, period = minimize_prefix(prefix, period)
        self.prefix = prefix
        self.period = period
    def __str__(self):
        return "{self.prefix}({self.period})^ω"


if __name__ == "__main__":
    assert rrotate("abc", 0) == "abc"
    assert rrotate("abc", 1) == "cab"
    assert rrotate("abc", 2) == "bca"
    assert rrotate("abc", 3) == "abc"
    assert rrotate("abc", 4) == "cab"

    r = PeriodicWord("a", "b")
    assert r.prefix == "a" and r.period == "b"
    r = PeriodicWord("ab", "b")
    assert r.prefix == "a" and r.period == "b"
    r = PeriodicWord("aba", "b")
    assert r.prefix == "aba" and r.period == "b"
    r = PeriodicWord("aba", "ba")
    assert r.prefix == "" and r.period == "ab"
    r = PeriodicWord("aba", "ab")
    assert r.prefix == "aba" and r.period == "ab"
    r = PeriodicWord("ab", "ab")
    assert r.prefix == "" and r.period == "ab"
    r = PeriodicWord("abab", "ab")
    assert r.prefix == "" and r.period == "ab"
    r = PeriodicWord("ab", "abab")
    assert r.prefix == "" and r.period == "ab"
    r = PeriodicWord("ab", "ababab")
    assert r.prefix == "" and r.period == "ab"
    r = PeriodicWord("a", "bababa")
    assert r.prefix == "" and r.period == "ab"
    r = PeriodicWord("abc", "abcabc")
    assert r.prefix == "" and r.period == "abc"
