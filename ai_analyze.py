
import json
import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check your Windows environment variable."
    )

client = genai.Client(api_key=api_key)


def analyze_incident(incident):
    prompt = f"""
You are a technical incident investigation assistant.

Analyse this incident using only the evidence provided.

Incident data:
{json.dumps(incident, indent=2)}

Please provide:
1. A summary of what happened.
2. Observed facts from the logs.
3. Two or three plausible causes, clearly labelled as hypotheses.
4. Three recommended investigation steps.
5. Additional information needed to confirm the root cause.

Do not claim that a hypothesis is a confirmed root cause.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text or "Gemini returned no text."


def main():
    with open("incident_report.json", "r") as file:
        report = json.load(file)

    for incident in report["incidents"]:
        print("\n" + "=" * 50)
        print("CAMERA:", incident["camera"])
        print("SEVERITY:", incident["severity"])
        print("=" * 50)

        try:
            analysis = analyze_incident(incident)
            print(analysis)

        except Exception as error:
            print("AI analysis failed.")
            print("Error type:", type(error).__name__)
            print("Details:", error)


if __name__ == "__main__":
    main()
