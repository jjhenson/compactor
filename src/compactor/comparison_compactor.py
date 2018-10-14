from typing import Optional


class AssertDummy:
    @staticmethod
    def format(msg: Optional[str], expect: Optional[str], actual: Optional[str]) -> str:
        msg = '' if msg is None else msg + ' '
        expect = 'None' if expect is None else expect
        actual = 'None' if actual is None else actual
        return msg + "expected:<" + expect + "> but was:<" + actual + ">"


class ComparisonCompactor:
    ELLIPSIS = "..."
    DELTA_END = "]"
    DELTA_START = "["

    def __init__(self, context_length: int, expected: str, actual: str):
        self.f_context_length: int = context_length
        self.f_expected: str = expected
        self.f_actual: str = actual
        self.f_prefix: int = 0
        self.f_suffix: int = 0

    def compact(self, message: Optional[str]=None) -> str:
        if self.f_expected is None or self.f_actual is None or self._are_strings_equal():
            return AssertDummy.format(message, self.f_expected, self.f_actual)
        self._find_common_prefix()
        self._find_common_suffix()
        expected = self._compact_string(self.f_expected)
        actual = self._compact_string(self.f_actual)
        return AssertDummy.format(message, expected, actual)

    def _compact_string(self, source: str) -> str:
        result = self.DELTA_START + source[self.f_prefix: len(source) - self.f_suffix + 1] + self.DELTA_END
        if self.f_prefix > 0:
            result = self._compute_common_prefix() + result
        if self.f_suffix - 1 > 0:
            result = result + self._compute_common_suffix()
        return result

    def _find_common_prefix(self):
        min_len = min(len(self.f_expected), len(self.f_actual))
        try:
            self.f_prefix = next(i for i in range(min_len) if self.f_expected[i] != self.f_actual[i])
        except StopIteration:
            self.f_prefix = min(len(self.f_expected), len(self.f_actual))

    def _find_common_suffix(self):
        min_len = min(len(self.f_expected), len(self.f_actual))
        try:
            self.f_suffix = next(i for i in range(1, min_len + 1) if self.f_expected[-i] != self.f_actual[-i] or
                                 min_len - i + 1 == self.f_prefix)
        except StopIteration:
            self.f_suffix = min(len(self.f_expected), len(self.f_actual)) + 1

    def _compute_common_prefix(self) -> str:
        return (self.ELLIPSIS if self.f_prefix > self.f_context_length else "") + \
            self.f_expected[max(0, self.f_prefix - self.f_context_length): self.f_prefix]

    def _compute_common_suffix(self):
        end = len(self.f_expected) - max(self.f_suffix - 1 - self.f_context_length, 0)
        return self.f_expected[len(self.f_expected) - self.f_suffix + 1: end] + (
            self.ELLIPSIS if len(self.f_expected) - self.f_suffix + 1 < len(self.f_expected) - self.f_context_length
            else ""
        )

    def _are_strings_equal(self) -> bool:
        return self.f_expected == self.f_actual
