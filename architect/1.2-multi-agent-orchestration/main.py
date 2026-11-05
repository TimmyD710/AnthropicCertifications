import anthropic
client = anthropic.Anthropic()



def run_subagent(brief):
    response = client.messages.create(
        model="code",
        max_tokens=10000,
        messages=[{"role":"user","content":brief}]
    )
    if not response.content:
        return f"Response content is empty. Stop reason {response.stop_reason}"
    return response.content[0].text

brief = "The company Tinininy was founded in 2018 and currently has 123 employees. How old will Tinininy be in 2030? And how many people will work there? When will project 'Olaha' be started by Tinininy? Answer in brief sentences, one per question asked"

print("Without secret:", run_subagent(brief))
print("With secret:", run_subagent(f"Project Olaha will commence in 2029. {brief}"))

