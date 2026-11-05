import anthropic
client = anthropic.Anthropic()

response = client.messages.create(
    model="code",
    max_tokens=100,
    messages=[{"role":"user","content":"Who are you?"}]
)
print(response.content[0].text)