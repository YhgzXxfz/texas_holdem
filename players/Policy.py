from enum import Enum


class Policy(Enum):
    ALWAYS_CALL = "always_call"
    ALWAYS_CHECK_OR_FOLD = "always_check_or_fold"
