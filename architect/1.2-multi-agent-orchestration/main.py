import anthropic
import time
import os
client = anthropic.Anthropic()
MAX_ITERATIONS = 20
COORDINATOR_PROMPT = "Split a reaseach topic into independent pieces and delegate each piece with the delegate tool. Put all independent delegate calls in the same response. Do not answer from your own knowledge"
TOOLS = [
    {
        "name":"delegate",
        "description":"delegate a task to a subagent. Two subagents exist. One looks up answers to a question via a search stub, the other searches  documents specified by the user for specific information",
        "input_schema":{
            "type":"object",
            "properties":{
                "agent":{"type":"string","enum":["search","document"]},
                "task":{"type":"string","description":"The search query or the question"},
                "document":{"type":"string","description":"the file name inside docs/"}
            },
            "required":["agent","task"]
        }
    }
]

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
    if not path:
        return "Error: no file name given"
    path = os.path.join("docs", path)
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        return run_subagent(f"Answer this: {question}. Answer using only the following document; if the answer is missing, say so: \n {text}")
    except FileNotFoundError:
        return f"Error: File not found. Available: {os.listdir("docs")}"

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

# t0 = time.perf_counter()
# search_result = search_subagent("AI testing tools and risks")
# print(f"search_subagent took {time.perf_counter() -t0:.3f} seconds")
# document_result = document_subagent("What results did the pilot achieve?", "docs/testing_report.txt")
# print(f"document_subagent took {time.perf_counter() -t0:.3f} seconds")
# print(summary_subagent(search_result, document_result))
# print(f"document_subagent took {time.perf_counter() -t0:.3f} seconds")

def coordinator(messages):
    return client.messages.create(model="code", max_tokens=10000, system=COORDINATOR_PROMPT, tools=TOOLS, messages=messages)

def run_agent(question):
    messages=[{"role":"user","content":question}]
    result = coordinator(messages)
    print(f"Stop reason: {result.stop_reason}")
    print(f"Number of tool_use requests: {len([item for item in result.content if item.type == "tool_use"])}")
    messages.append({"role":"assistant","content":result.content})
    iterations = int(0)
    while result.stop_reason == "tool_use" and iterations < MAX_ITERATIONS:
        tool_results = {"role":"user","content":[]}
        for item in result.content:
            if item.type == "tool_use":
                print("Tool request:", item.id, item.name, item.input)
                if item.input["agent"] == "search":
                    tool_results["content"].append({
                        "type":"tool_result",
                        "tool_use_id":item.id,
                        "content":search_subagent(item.input["task"])
                    })
                elif item.input["agent"] == "document":
                    tool_results["content"].append({
                        "type":"tool_result",
                        "tool_use_id":item.id,
                        "content":document_subagent(item.input["task"], item.input.get("document"))
                    })
        messages.append(tool_results)
        result = coordinator(messages)
        messages.append({"role":"assistant","content":result.content})
        iterations = iterations + 1
    print(result.stop_reason)
    if result.stop_reason != "end_turn":
        return ("Limit of iterations reached. Please try a differnt prompt.")
    return result.content[0].text


print(run_agent("Research: how is AI changing software testing? Cover the tools, the risks, the pilot results and the costs."))
