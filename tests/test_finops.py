import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from finops import (
    calculate_total_cost,
    analyze_resources,
    summarize_by_service,
    summarize_by_environment
)


def test_calculate_total_cost():
    resources = [
        {"cost": "100"},
        {"cost": "200"}
    ]

    assert calculate_total_cost(resources) == 300


def test_detect_idle_vm():
    resources = [
        {
            "resource": "VM-TEST",
            "cost": "600",
            "environment": "Test",
            "service": "Virtual Machine",
            "cpu_usage": "2"
        }
    ]

    recommendations = analyze_resources(resources)

    assert len(recommendations) == 1
    assert recommendations[0]["classification"] == "POSSIBLE_IDLE_RESOURCE"
    assert recommendations[0]["estimated_monthly_saving"] == 600


def test_detect_rightsizing():
    resources = [
        {
            "resource": "VM-DEV",
            "cost": "800",
            "environment": "Dev",
            "service": "Virtual Machine",
            "cpu_usage": "15"
        }
    ]

    recommendations = analyze_resources(resources)

    assert recommendations[0]["classification"] == "POSSIBLE_RIGHTSIZING"
    assert recommendations[0]["estimated_monthly_saving"] == 240


def test_summarize_by_service():
    resources = [
        {"service": "Virtual Machine", "cost": "800"},
        {"service": "Virtual Machine", "cost": "600"},
        {"service": "Database", "cost": "3000"}
    ]

    result = summarize_by_service(resources)

    assert result["Virtual Machine"] == 1400
    assert result["Database"] == 3000


def test_summarize_by_environment():
    resources = [
        {"environment": "Dev", "cost": "800"},
        {"environment": "Production", "cost": "3000"}
    ]

    result = summarize_by_environment(resources)

    assert result["Dev"] == 800
    assert result["Production"] == 3000