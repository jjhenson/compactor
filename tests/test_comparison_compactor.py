from compactor.comparison_compactor import ComparisonCompactor

def test_message():
    failure = ComparisonCompactor(0, "b", "c").compact("a")
    assert(failure == "a expected:<[b]> but was:<[c]>")

def test_start_same():
    failure = ComparisonCompactor(1, "ba", "bc").compact(None)
    assert (failure == "expected:<b[a]> but was:<b[c]>")

def test_end_same():
    failure = ComparisonCompactor(1, "ab", "cb").compact(None)
    assert (failure == "expected:<[a]b> but was:<[c]b>")