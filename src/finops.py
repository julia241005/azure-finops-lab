def calculate_total_cost(resources):
    return sum(float(resource["cost"]) for resource in resources)


def analyze_resources(resources):
    recommendations = []

    for resource in resources:
        cost = float(resource["cost"])
        cpu = float(resource["cpu_usage"])

        if resource["service"] != "Virtual Machine":
            continue

        if cpu < 10:
            recommendations.append({
                "resource": resource["resource"],
                "environment": resource["environment"],
                "current_cost": cost,
                "cpu_usage": cpu,
                "classification": "POSSIBLE_IDLE_RESOURCE",
                "recommendation": "Avaliar desligamento, remoção ou agendamento.",
                "estimated_monthly_saving": cost
            })

        elif cpu < 20:
            saving = cost * 0.30

            recommendations.append({
                "resource": resource["resource"],
                "environment": resource["environment"],
                "current_cost": cost,
                "cpu_usage": cpu,
                "classification": "POSSIBLE_RIGHTSIZING",
                "recommendation": "Avaliar se a VM está superdimensionada.",
                "estimated_monthly_saving": saving
            })

    return recommendations


def summarize_by_service(resources):
    summary = {}

    for resource in resources:
        service = resource["service"]
        cost = float(resource["cost"])

        summary[service] = summary.get(service, 0) + cost

    return summary


def summarize_by_environment(resources):
    summary = {}

    for resource in resources:
        environment = resource["environment"]
        cost = float(resource["cost"])

        summary[environment] = summary.get(environment, 0) + cost

    return summary