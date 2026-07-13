import os
import json
from google import genai
from google.genai import types  # 🟢 Added for structured schema definitions
from dotenv import load_dotenv

load_dotenv()

class OutreachAgency:
    """Configures system personas with deterministic JSON schemas and temperature tuning."""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing from your environment setup.")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    def run_structured_agent(self, system_instruction: str, target_context: str, temperature: float = 0.2) -> dict:
        """Executes a model call forcing a strict JSON object return value."""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=target_context,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature,
                    response_mime_type="application/json"  # 🟢 Forces API to output valid JSON
                )
            )
            # Parse the text string into a native Python dictionary
            return json.loads(response.text)
            
        except Exception as e:
            print(f"[API Error] Falling back to structured fail-safe mapping: {str(e)}")
            return self.generate_json_fail_safe(system_instruction)

    def generate_json_fail_safe(self, system_instruction: str) -> dict:
        """Fallback engine that returns valid structural dictionaries matching the data contracts."""
        if "Research Lead" in system_instruction:
            return {
                "company_name": "Target Enterprise",
                "core_operations": "Enterprise Infrastructure Scaling",
                "target_audience": "Mid-to-large corporate software engineering teams",
                "commercial_value": "Reducing infrastructure overhead and workflow processing drag."
            }
        elif "Market Strategist" in system_instruction:
            return {
                "friction_points": [
                    "Legacy system architecture scaling bottlenecks",
                    "High operational overhead within digital tracking systems"
                ],
                "strategic_fit_explanation": "Our automation frameworks drop right into scaling infrastructure layers to reduce latency."
            }
        else:
            return {
                "cold_email": {
                    "subject": "Infrastructure bottlenecks",
                    "body": "Hi team,\n\nI noticed you are scaling software operations. That often brings unexpected processing lag.\n\nWe fix this by reducing overhead by 20%. Worth a quick chat?\n\nBest,\n[Name]"
                },
                "linkedin_note": "Hi, noticed your team's expansion in enterprise engineering. Let's connect to share benchmarks on lowering scaling friction!",
                "value_add_follow_up": {
                    "subject": "Re: Infrastructure bottlenecks",
                    "body": "Hi team,\n\nFollowing up—here is a framework checklist on optimizing data tracking overhead during scale windows. Let me know if it helps.\n\nBest,\n[Name]"
                }
            }

    def get_research_lead_persona(self) -> str:
        return """
        You are an Elite Corporate Research Lead. Analyze raw web scrapings and return a JSON object with these EXACT keys:
        {
          "company_name": "String name of organization",
          "core_operations": "A summary of what their platform or business actually does",
          "target_audience": "Who they sell their products or services to",
          "commercial_value": "The primary business benefit they deliver"
        }
        Do not add any text before or after the JSON structure.
        """

    def get_market_strategist_persona(self) -> str:
        return """
        You are a Pragmatic B2B Market Strategist. Analyze a company profile and return a JSON object with these EXACT keys:
        {
          "friction_points": ["List string point 1", "List string point 2"],
          "strategic_fit_explanation": "A detailed evaluation of how our service directly minimizes their problems"
        }
        Do not add any text before or after the JSON structure.
        """

    def get_copywriter_persona(self) -> str:
        return """
        You are an Elite Multi-Channel Copywriter. Review the friction metrics and return a JSON object with these EXACT keys:
        {
          "cold_email": { "subject": "string", "body": "string" },
          "linkedin_note": "string under 300 chars",
          "value_add_follow_up": { "subject": "string", "body": "string" }
        }
        Keep the tone clean, professional, and completely free of corporate buzzwords.
        """