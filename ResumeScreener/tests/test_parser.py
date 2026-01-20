"""
Unit tests for resume parser
"""

import sys
import os

# Add project root to path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from core.parser import parse_resume


def test_parse_resume_returns_dict():
    result = parse_resume("dummy.pdf")
    assert isinstance(result, dict)


def test_parse_resume_keys():
    result = parse_resume("dummy.pdf")
    assert "text" in result
    assert "skills" in result
    assert "experience" in result


def test_parse_resume_empty():
    result = parse_resume("not_exists.pdf")
    assert result["text"] == ""
    assert result["skills"] == []
    assert result["experience"] == 0
