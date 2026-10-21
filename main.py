# Welcome to your Python project!

import json


def determine_severity(error_messages, camera, count):
    critical_error_found = any(
        "Detection service timeout" in message
        for message in error_messages
        if camera in message
    )

    if critical_error_found or count >= 3:
        return "HIGH"
    elif count >= 1:
        return "MEDIUM"
    else:
        return "LOW"



def investigate_root_cause(messages):
    combined_logs = " ".join(messages).lower()

    findings = []

    if "frame processing latency" in combined_logs:
        findings.append(
            "High frame processing latency was observed."
        )

    if "detection service timeout" in combined_logs:
        findings.append(
            "The detection service timed out."
        )

    if "failed to publish detection event" in combined_logs:
        findings.append(
            "Detection event publication failed."
        )

    if (
        "frame processing latency" in combined_logs
        and "detection service timeout" in combined_logs
    ):
        hypothesis = (
            "Processing latency may be contributing to "
            "detection service timeouts. Investigate "
            "processing load and service response times."
        )
    elif "detection service timeout" in combined_logs:
        hypothesis = (
            "A detection service timeout occurred. "
            "Inspect service health and response times."
        )
    else:
        hypothesis = (
            "Insufficient evidence to suggest a likely cause."
        )

    return {
        "observed_findings": findings,
        "root_cause_hypothesis": hypothesis
    }


def analyze_logs(logs):
    error_counts = {}
    errors_by_camera = {}

    for log in logs:
       if "ERROR" in log:
             parts = log.split()

             if len(parts) < 4:
                continue

             camera = parts[3]
             message = log.strip()

             error_counts[camera] = error_counts.get(camera, 0) + 1

             if camera not in errors_by_camera:
                errors_by_camera[camera] = []

             errors_by_camera[camera].append(message)

    incidents = []

    for camera, count in error_counts.items():
        messages = errors_by_camera[camera]

    investigation = investigate_root_cause(messages)

    incidents.append({
    "camera": camera,
    "error_count": count,
    "severity": determine_severity(messages, camera, count),
    "status": "Investigation required",
    "evidence": messages,
    "investigation": investigation
                 })
    return incidents



def build_ai_prompt(incident):
    prompt = f"""
You are a technical incident investigation assistant.

Analyse the incident below.

Camera: {incident["camera"]}
Severity: {incident["severity"]}
Error count: {incident["error_count"]}

Observed evidence:
{json.dumps(incident["evidence"], indent=2)}

Existing investigation:
{json.dumps(incident["investigation"], indent=2)}

Your tasks:
1. Summarise what is known from the evidence.
2. Suggest plausible causes without presenting guesses as facts.
3. Recommend three investigation steps.
4. Identify what additional information is needed.

Clearly distinguish observed facts from hypotheses.
Do not claim a root cause is confirmed unless the evidence proves it.
"""
    return prompt.strip()


def main():
    with open("sample_logs.txt", "r") as file:
        logs = file.readlines()

    incidents = analyze_logs(logs)

    report = {
        "total_log_entries": len(logs),
        "total_incidents": len(incidents),
        "incidents": incidents
    }

    with open("incident_report.json", "w") as file:
        json.dump(report, file, indent=4)

    print("Incident report generated successfully.")
    print("Total log entries:", len(logs))
    print("Total incidents:", len(incidents))
    print("Output file: incident_report.json")


if __name__ == "__main__":
    main()
