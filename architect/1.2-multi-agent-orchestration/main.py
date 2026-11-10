import anthropic
import time
client = anthropic.Anthropic()

def search_stub(query):
    facts = {"ai testing tools":"AI testing tools are created to evaluate performance, quality and speed. These tools are included in benchmark testing.", "gardening hoe":"Exists to yeet that shit. Some people yeet it further than others. Not to be mixed up with the term 'hoe' often used as an insult to women.", "security risks":"Risks to a system or software or physical structures such as buildings", "risk of bad breath":"E.g. if you dont brush your teeth you have the risk of having bad breath."}
    found = []
    for key in facts:
        if key in query.lower():
            found.append(facts[key])
    if not found:
        return "No results found"
    return " ".join(found)

def search_subagent(query):
    search_results = search_stub(query)
    return run_subagent(f"Your task is to summarise the results below into bullet points; use only the text below; if the results say 'No results found', say so. \n{search_results}")

def document_subagent(question, path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return run_subagent(f"Answer this: {question}. Answer using only the following document; if the answer is missing, say so: \n {text}")

def summary_subagent(answer1, answer2):
    return run_subagent(f"Summarize {answer1} and {answer2}")

def run_subagent(brief):
    response = client.messages.create(
        model="code",
        max_tokens=10000,
        messages=[{"role":"user","content":brief}]
    )
    if not response.content:
        return f"Response content is empty. Stop reason {response.stop_reason}"
    return response.content[0].text

t0 = time.perf_counter()
search_result = search_subagent("AI testing tools and risks")
print(f"search_subagent took {time.perf_counter() -t0:.3f} seconds")
document_result = document_subagent("What results did the pilot achieve?", "docs/testing_report.txt")
print(f"document_subagent took {time.perf_counter() -t0:.3f} seconds")
print(summary_subagent(search_result, document_result))
print(f"document_subagent took {time.perf_counter() -t0:.3f} seconds")
