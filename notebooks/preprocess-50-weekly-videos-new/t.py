response = client.models.generate_content(
    model='gemini-2.0-flash',
    # config=types.GenerateContentConfig(
    #   system_instruction=system_instruction),
    config={
        'response_mime_type': "application/json",
        'response_schema': response_schema,
        'system_instruction': system_instruction,
        # 'temperature': 0.1

    },
    contents=f"Description: {desc}\n Transcript: {transcript}"
)
