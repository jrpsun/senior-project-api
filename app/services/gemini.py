import base64
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

class Gemini:
    def generate(prompt: str):
        load_dotenv()
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

        model = "gemini-2.0-flash"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="application/json",
        )

        all_response = ""

        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                all_response += chunk.text

        try:
            result = json.loads(all_response)
            return result
        except json.JSONDecodeError:
            print("Error decoding JSON:", all_response)
            return None
