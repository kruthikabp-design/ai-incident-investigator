
import unittest
from main import (
    determine_severity,
    investigate_root_cause,
    build_ai_prompt
)


class TestIncidentSeverity(unittest.TestCase):

    def test_timeout_is_high(self):
        messages = [
            "ERROR camera_101 Detection service timeout"
        ]
        result = determine_severity(messages, "camera_101", 1)
        self.assertEqual(result, "HIGH")

    def test_three_errors_are_high(self):
        messages = []
        result = determine_severity(messages, "camera_101", 3)
        self.assertEqual(result, "HIGH")

    def test_two_noncritical_errors_are_medium(self):
        messages = [
            "ERROR camera_101 Failed to publish event",
            "ERROR camera_101 Connection reset"
        ]
        result = determine_severity(messages, "camera_101", 2)
        self.assertEqual(result, "MEDIUM")

    def test_zero_errors_are_low(self):
        result = determine_severity([], "camera_101", 0)
        self.assertEqual(result, "LOW")

    
    def test_latency_and_timeout_produce_hypothesis(self):
        messages = [
            "WARN camera_101 Frame processing latency exceeded threshold",
            "ERROR camera_101 Detection service timeout"
        ]

        result = investigate_root_cause(messages)

        self.assertIn(
            "may be contributing",
            result["root_cause_hypothesis"]
        )

    def test_timeout_without_latency(self):
        messages = [
            "ERROR camera_101 Detection service timeout"
        ]

        result = investigate_root_cause(messages)

        self.assertIn(
            "A detection service timeout occurred",
            result["root_cause_hypothesis"]
        )
    
    def test_ai_prompt_includes_incident_evidence(self):
        incident = {
            "camera": "camera_101",
            "severity": "HIGH",
            "error_count": 1,
            "evidence": [
                "ERROR camera_101 Detection service timeout"
            ],
            "investigation": {
                "observed_findings": [
                    "The detection service timed out."
                ],
                "root_cause_hypothesis":
                    "Inspect service health."
            }
        }

        prompt = build_ai_prompt(incident)

        self.assertIn("camera_101", prompt)
        self.assertIn("Detection service timeout", prompt)
        self.assertIn("Clearly distinguish", prompt)



if __name__ == "__main__":
    unittest.main()
