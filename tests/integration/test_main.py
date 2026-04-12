import pytest
from src.main import main

def test_main(capsys):
    """Test that main entry point works"""
    main()
    captured = capsys.readouterr()
    assert "Welcome to the Oregon Trail" in captured.out