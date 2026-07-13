import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_sales_pitch(company_data: str, target_service: str) -> str:
    """Sends company profile to Gemini with an automatic backup model fallback if servers are busy."""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return "Missing API Key! Ensure GEMINI_API_KEY is defined in your .env file."
        
    # 🟢 UPDATE: Using the correct, fully-supported GenAI production models
    models_to_try = ['gemini-2.5-flash', 'gemini-2.5-pro']
    
    prompt = f"""
    You are an elite corporate B2B sales copywriter.
    
    Below is raw data collected from a target company's website:
    ---
    {company_data}
    ---
    
    I want to pitch them the following solution/service: {target_service}
    
    Write a highly contextual cold outreach email. It must sound completely human, 
    demonstrate clear knowledge of what they offer, and point out how my service solves 
    a potential challenge they face. Do not include generic marketing jargon.
    """

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        return f"Client Initialization Failed: {str(e)}"

    for model_name in models_to_try:
        try:
            print(f"🧠 Attempting AI generation using primary engine: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text
            
        except Exception as e:
            # Catch 503 or temporary unavailability to fall back
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"⚠️ {model_name} is currently overloaded. Automatically shifting to fallback channel...")
                continue 
            else:
                # If it's any other error, surface it cleanly
                return f"AI Generation Failed: {str(e)}"
                
    return "AI Generation Failed: All Google Gemini server clusters are currently experiencing high demand. Please wait 10 seconds and click generate again."