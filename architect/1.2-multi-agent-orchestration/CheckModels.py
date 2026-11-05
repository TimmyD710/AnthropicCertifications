import anthropic
client = anthropic.Anthropic()

for item in client.models.list():
    try:
        response = client.messages.create(
            model=item.id,
            max_tokens=100,
            messages=[{"role":"user","content":"Who are you?"}]
        )
        print(item.model_dump(),":",response.content[0].text, "\n\n\n")
    except anthropic.APIStatusError:
        print("Error for:", item.model_dump())