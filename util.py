import math

def longest_common_prefix(words):
    some_str = None
    some_peri_word = None
    for w in words:
        if isinstance(w, str):
            some_str = w
        elif isinstance(w, PeriodicWord):
            some_peri_word = w
        if some_str is not None and some_peri_word is not None:
            break
    if some_str:
        for i in range(len(some_str), -1 , -1):
            prefix = some_str[:i]
            if all(map(lambda s: s.startswith(prefix), words)):
                return prefix
        return ""
    else:
        if all(w == some_peri_word for w in words):
            return some_peri_word
        longest_prefix = ""
        i = 0
        while True:
            prefix = some_peri_word.expand(i)
            if not all([w.startswith(prefix) for w in words]):
                break
            else:
                longest_prefix = prefix
                i += 1
        return longest_prefix

def rrotate(s, n):
    n = n % len(s)
    return s[-n:] + s[:-n]

def minimize_period(period):
    # very inefficient, but I don't care
    for i in range(1, len(period)):
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
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return hash((self.prefix, self.period))
    def __eq__(self, other):
        if isinstance(other, PeriodicWord):
            return self.prefix == other.prefix and self.period == other.period
        return NotImplemented
    def __radd__(self, other):
        if isinstance(other, str):
            return PeriodicWord(other + self.prefix, self.period)
        return NotImplemented
    def expand(self, n):
        if n <= len(self.prefix):
            return self.prefix[:n]
        else:
            rep_len = n - len(self.prefix)
            full_reps = self.period * (rep_len // len(self.period))
            partial_rep = self.period[:rep_len-len(full_reps)]
            return self.prefix + full_reps + partial_rep
    def startswith(self, prefix):
        if isinstance(prefix, str):
            return self.expand(len(prefix)) == prefix
        elif isinstance(prefix, PeriodicWord):
            return prefix == self
        return NotImplemented
    def without_prefix(self, n):
        if n <= len(self.prefix):
            return PeriodicWord(self.prefix[n:], self.period)
        else:
            n -= len(self.prefix)
            new_period = rrotate(self.period, -n)
            return PeriodicWord("", new_period)

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
    assert PeriodicWord("a", "aaaa") == PeriodicWord("", "a")
    assert hash(PeriodicWord("abcab", "cabcab")) == hash(PeriodicWord("", "abc"))
    assert hash(PeriodicWord("abcab", "cabca")) != hash(PeriodicWord("", "abc"))

    assert PeriodicWord("ab", "ab").startswith("")
    assert PeriodicWord("ab", "ab").startswith("ab")
    assert PeriodicWord("ab", "ab").startswith("a")
    assert PeriodicWord("ab", "ab").startswith("abab")
    assert PeriodicWord("ca", "ab").startswith("ca")
    assert PeriodicWord("ca", "ab").startswith("caab")
    assert PeriodicWord("ca", "ab").startswith("caa")
    assert PeriodicWord("ca", "ab").startswith("caaba")
    assert PeriodicWord("cc", "a").startswith("cc")
    assert not PeriodicWord("cc", "a").startswith("ca")
    assert not PeriodicWord("cc", "a").startswith("a")
    assert not PeriodicWord("cc", "a").startswith("ccb")

    assert longest_common_prefix(("a", "b")) == ""
    assert longest_common_prefix(("a", "a")) == "a"
    assert longest_common_prefix(("a", "a", "b")) == ""
    assert longest_common_prefix(("aab", "a", "a")) == "a"
    assert longest_common_prefix(("a", "aab")) == "a"
    assert longest_common_prefix(("aa", "aab")) == "aa"
    assert longest_common_prefix(("aa", PeriodicWord("", "a"))) == "aa"
    assert longest_common_prefix((PeriodicWord("aab", "a"), PeriodicWord("", "a"))) == "aa"
    assert longest_common_prefix((PeriodicWord("aa", "a"), PeriodicWord("", "a"))) == PeriodicWord("a", "aaaa")

    assert PeriodicWord("", "a").without_prefix(1) == PeriodicWord("", "a")
    assert PeriodicWord("ab", "a").without_prefix(2) == PeriodicWord("", "a")
    assert PeriodicWord("", "abc").without_prefix(2) == PeriodicWord("", "cab")
    assert PeriodicWord("", "abcd").without_prefix(2) == PeriodicWord("", "cdab")
    assert PeriodicWord("", "abcd").without_prefix(3) == PeriodicWord("", "dabc")
    assert PeriodicWord("", "abcd").without_prefix(8) == PeriodicWord("", "abcd")
