import csv
import json
from pathlib import Path

from finops import (
    calculate_total_cost,
    analyze_resources,
    summarize_by_service,
    summarize_by_environment
)


def load_costs(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def main():
    project_root = Path(__file__).resolve().parent.parent

    data_file = project_root / "data" / "costs.csv"
    report_file = project_root / "reports" / "analysis.json"

    resources = load_costs(data_file)

    total_cost = calculate_total_cost(resources)
    recommendations = analyze_resources(resources)

    service_summary = summarize_by_service(resources)
    environment_summary = summarize_by_environment(resources)

    monthly_saving = sum(
        item["estimated_monthly_saving"]
        for item in recommendations
    )

    annual_saving = monthly_saving * 12

    report = {
        "summary": {
            "total_monthly_cost": round(total_cost, 2),
            "estimated_monthly_saving": round(monthly_saving, 2),
            "estimated_annual_saving": round(annual_saving, 2),
            "resources_analyzed": len(resources),
            "recommendations_found": len(recommendations)
        },
        "cost_by_service": service_summary,
        "cost_by_environment": environment_summary,
        "recommendations": recommendations
    }

    with open(report_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print("=" * 50)
    print("AZURE FINOPS LAB")
    print("=" * 50)
    print()

    print(f"Custo mensal: R$ {total_cost:.2f}")
    print(f"Economia potencial mensal: R$ {monthly_saving:.2f}")
    print(f"Economia potencial anual: R$ {annual_saving:.2f}")
    print()

    print(f"Recursos analisados: {len(resources)}")
    print(f"Recomendações: {len(recommendations)}")
    print()

    print("RECOMENDAÇÕES")
    print("-" * 50)

    for item in recommendations:
        print(
            f"{item['resource']} | "
            f"{item['classification']} | "
            f"CPU: {item['cpu_usage']:.0f}% | "
            f"Economia: R$ "
            f"{item['estimated_monthly_saving']:.2f}/mês"
        )

    print()
    print(f"Relatório gerado: {report_file}")


if __name__ == "__main__":
    main()