import math

def rrotate(s, n):
    n = n % len(s)
    return s[-n:] + s[:-n]

def minimize_period(period):
    # very inefficient, but I don't care
    for i in range(2, len(period)):
        prefix = period[:i]
        expanded_prefix = prefix * int(math.ceil((len(period) / i)))
        if expanded_prefix[:len(period)] == period and period.startswith(expanded_prefix[len(period):]):
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
        assert len(period) > 0
        period = minimize_period(period)
        prefix, period = minimize_prefix(prefix, period)
        self.prefix = prefix
        self.period = period
    def __str__(self):
        return f"{self.prefix}({self.period})^ω"
    def __hash__(self):
        return hash((self.prefix, self.period))
    def __eq__(self, other):
        return self.prefix == other.prefix and self.period == other.period

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

    assert PeriodicWord("abc", "abcabc") == PeriodicWord("", "abc")
    assert PeriodicWord("abcabc", "abcabc") == PeriodicWord("", "abc")
    assert PeriodicWord("abcab", "cabcab") == PeriodicWord("", "abc")
    assert hash(PeriodicWord("abcab", "cabcab")) == hash(PeriodicWord("", "abc"))
    assert hash(PeriodicWord("abcab", "cabca")) != hash(PeriodicWord("", "abc"))
