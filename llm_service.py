import os
import json
from anthropic import AsyncAnthropic

# Configure the Anthropic client with the API key from the .env file
try:
    client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
except KeyError:
    raise Exception("ANTHROPIC_API_KEY not found. Please set it in your .env file.")


async def get_llm_analysis(user_symptom_text: str) -> dict:
    """
    Builds the advanced prompt and gets a structured JSON response from the Anthropic Claude model.
    """
    # The system prompt sets the context and rules for the AI
    system_prompt = """
    You are an AI Medical Information Assistant. Your purpose is strictly educational. Your primary function is to analyze a user's described symptoms and provide a list of potential conditions and safe, responsible next steps.

    You MUST follow these rules:
    1. Analyze the user's symptoms provided in the prompt.
    2. Identify 3-5 possible conditions. For each, provide a brief description and a likelihood (e.g., 'Possible', 'Less Likely'). Do NOT present this as a definitive diagnosis.
    3. Recommend clear next steps, categorized into one of three levels: 'Self-Care', 'Consult a Doctor', or 'Seek Immediate Medical Attention'.
    4. You MUST include a prominent safety disclaimer.
    5. If symptoms mention chest pain, difficulty breathing, severe headache, or confusion, the primary recommendation MUST be 'Seek Immediate Medical Attention'.
    6. Your entire output MUST be a single, valid JSON object and nothing else. Do not wrap it in markdown or add any introductory text.
    
    The JSON object must strictly adhere to this format:
    {
      "potential_conditions": [
        {"name": "string", "description": "string", "likelihood": "string"}
      ],
      "recommended_next_steps": {
        "urgency_level": "string",
        "steps": ["string"]
      },
      "safety_disclaimer": "IMPORTANT: This is not a medical diagnosis. This information is for educational purposes only. Please consult a qualified healthcare professional for any health concerns."
    }
    """

    try:
        # Send the request to the Claude API
        message = await client.messages.create(
            model="claude-3-haiku-20240307",  # Haiku is fast and cost-effective
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Here are my symptoms: {user_symptom_text}"
                }
            ]
        )
        
        # The response is inside the 'content' block
        raw_response_text = message.content[0].text
        
        try:
            # Parse the JSON string from the response
            llm_output = json.loads(raw_response_text)
            return llm_output
        except json.JSONDecodeError:
            print(f"--- FAILED TO DECODE JSON ---\nRaw Response: {raw_response_text}\n-----------------------------")
            raise ValueError("The AI model returned a response that was not in the expected JSON format.")

    except Exception as e:
        print(f"An unexpected error occurred with the Anthropic API: {e}")
        raise ValueError("An unexpected error occurred while communicating with the AI model.")

