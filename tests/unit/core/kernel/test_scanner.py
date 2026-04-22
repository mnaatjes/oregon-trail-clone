import pytest
from typing import List
from core.kernel.contracts.scanner import BaseScanner
from core.kernel.contracts.discovery import DiscoveryUnit
from dataclasses import dataclass

@dataclass(frozen=True)
class MockUnit(DiscoveryUnit):
    pass

class MockScanner(BaseScanner[MockUnit]):
    def scan(self, path: str) -> List[MockUnit]:
        return []

def test_base_scanner_implementation():
    scanner = MockScanner()
    assert scanner.scan("/some/path") == []

def test_base_scanner_is_abstract():
    with pytest.raises(TypeError):
        BaseScanner() # type: ignore
