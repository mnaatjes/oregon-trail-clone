# tests/integration/architecture/helpers.py
import os
from .constants import DOMAIN_PATH

def format_architecture_violation(
        domain:str,
        category:str,
        message:str,
        expected_location:str|None=None
):
    """Unified the presentation of architectural errors / missing content"""
    # Build Report
    report = [
        f"\n[ARCHITECTURE VIOLATION] in Domain: '{domain}'",
        f"Category: {category}",
        f"Message: {message}"
    ]

    # Check if there is an expected location associated
    if expected_location:
        report.append(f"Expected: {expected_location}")
    
    # return joined report as single string
    return "\n".join(report)

def get_all_domains():
    """Dynamically discovers all domain packages"""
    if not os.path.exists(DOMAIN_PATH):
        return []
    return [d for d in os.listdir(DOMAIN_PATH)
            if os.path.isdir(os.path.join(DOMAIN_PATH, d)) and not d.startswith("__")]