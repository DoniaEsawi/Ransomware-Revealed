import openai

openai.api_key = "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"


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": "Why should DevOps engineer learn kubernetes?"},
        ]
)

result = ''
for choice in response.choices:
    result += choice.message.content

print(result)