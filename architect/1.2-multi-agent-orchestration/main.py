import anthropic
import time
client = anthropic.Anthropic()

def search_stub(query):
    facts = {"tools":"AI testing tools generate test cases automatically from code or requirements. Many tools also repair broken tests after the user interface changes. Popular categories include test generation assistants, visual testing tools and self-healing test frameworks.", "risks":"AI-generated tests can look convincing while checking the wrong behaviour. Generated tests are sometimes flaky and need review by a person. Sending source code to external AI services can create data protection and confidentiality concerns."}
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
