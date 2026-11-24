from app.core.openai_client import openai_client


def generate_response(message: str) -> str:
    response = openai_client.responses.create(
        model="gpt-5.5",
        input=message,
    )

    return response.output_text