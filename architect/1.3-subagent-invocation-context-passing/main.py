import anthropic

client = anthropic.Anthropic()
response = client.messages.create(model="code", max_tokens=200, messages=[{"role":"user","content":"Name one color"}])

print(response.content[0].text)