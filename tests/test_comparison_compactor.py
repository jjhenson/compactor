from compactor.comparison_compactor import ComparisonCompactor


def test_message():
    failure = ComparisonCompactor(0, "b", "c").compact("a")
    assert(failure == "a expected:<[b]> but was:<[c]>")


def test_start_same():
    failure = ComparisonCompactor(1, "ba", "bc").compact()
    assert(failure == "expected:<b[a]> but was:<b[c]>")


def test_end_same():
    failure = ComparisonCompactor(1, "ab", "cb").compact()
    assert(failure == "expected:<[a]b> but was:<[c]b>")


def test_same():
    failure = ComparisonCompactor(1, "ab", "ab").compact()
    assert(failure == "expected:<ab> but was:<ab>")


def test_no_context_start_and_end_same():
    failure = ComparisonCompactor(0, "abc", "adc").compact()
    assert (failure == "expected:<...[b]...> but was:<...[d]...>")


def test_start_and_end_context():
    failure = ComparisonCompactor(1, "abc", "adc").compact()
    assert (failure == "expected:<a[b]c> but was:<a[d]c>")


def test_start_and_end_context_with_ellipses():
    failure = ComparisonCompactor(1, "abcde", "abfde").compact()
    assert (failure == "expected:<...b[c]d...> but was:<...b[f]d...>")


def test_comparison_error_start_same_complete():
    failure = ComparisonCompactor(2, "ab", "abc").compact()
    assert (failure == "expected:<ab[]> but was:<ab[c]>")


def test_comparison_error_end_same_complete():
    failure = ComparisonCompactor(0, "bc", "abc").compact()
    assert (failure == "expected:<[]...> but was:<[a]...>")


def test_comparison_error_end_same_complete_context():
    failure = ComparisonCompactor(2, "bc", "abc").compact()
    assert (failure == "expected:<[]bc> but was:<[a]bc>")


def test_comparison_error_overlapping_matches():
    failure = ComparisonCompactor(0, "abc", "abbc").compact()
    assert (failure == "expected:<...[]...> but was:<...[b]...>")


def test_comparison_error_overlapping_matches_context():
    failure = ComparisonCompactor(2, "abc", "abbc").compact()
    assert (failure == "expected:<ab[]c> but was:<ab[b]c>")


def test_comparison_error_overlapping_matches2():
    failure = ComparisonCompactor(0, "abcdde", "abcde").compact()
    assert (failure == "expected:<...[d]...> but was:<...[]...>")


def test_comparison_error_overlapping_matches2_context():
    failure = ComparisonCompactor(2, "abcdde", "abcde").compact()
    assert (failure == "expected:<...cd[d]e> but was:<...cd[]e>")


def test_comparison_error_with_actual_none():
    failure = ComparisonCompactor(0, "a", None).compact()
    assert (failure == "expected:<a> but was:<None>")


def test_comparison_error_with_actual_none_context():
    failure = ComparisonCompactor(2, "a", None).compact()
    assert (failure == "expected:<a> but was:<None>")


def test_comparison_error_with_expected_none():
    failure = ComparisonCompactor(0, None, "a").compact()
    assert (failure == "expected:<None> but was:<a>")


def test_comparison_error_with_expected_none_context():
    failure = ComparisonCompactor(2, None, "a").compact()
    assert(failure == "expected:<None> but was:<a>")


def test_bug_609972():
    failure = ComparisonCompactor(10, "S&P500", "0").compact()
    assert (failure == "expected:<[S&P50]0> but was:<[]0>")
