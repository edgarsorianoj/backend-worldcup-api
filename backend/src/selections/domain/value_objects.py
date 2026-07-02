from dataclasses import dataclass

import validators

from src.selections.domain.exception import SelectionFlagNotValid


@dataclass(frozen=True, kw_only=True)
class SelectionFlag:
    value: str

    def __post_init__(self) -> None:
        if not validators.url(self.value):
            raise SelectionFlagNotValid