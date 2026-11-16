import anthropic
import time
import os
from concurrent.futures import ThreadPoolExecutor

client = anthropic.Anthropic()

USER_PROMPT = "Research: how is AI changing software testing? Cover the tools, the risks, the pilot results and the costs."
MAX_ITERATIONS = 20
MAX_REFINEMENTS = 2
COORDINATOR_PROMPT = "Split a reaseach topic into independent pieces and delegate each piece with the delegate tool. Put all independent delegate calls in the same response. Do not answer from your own knowledge"
TOOLS = [
    {
        "name":"delegate",
        "description":"delegate a task to a subagent. Two subagents exist. One looks up answers to a question via a search stub, the other searches  documents specified by the user for specific information",
        "input_schema":{
            "type":"object",
            "properties":{
                "agent":{"type":"string","enum":["search","document"],"description":"use 'search' for general background on AI testing tools and risks, use 'document' for internal fact such as pilot results and costs"},
                "task":{"type":"string","description":"The search query or the question"},
                "document":{"type":"string","description":f"the file name inside 'docs' folder. This property is required when 'agent' == 'document'. Available files: {os.listdir("docs")}"}
            },
            "required":["agent","task"]
        }
    }
]

def search_stub(query):
    facts = {"tools":"AI testing tools generate test cases automatically from code or requirements. Many tools also repair broken tests after the user interface changes. Popular categories include test generation assistants, visual testing tools and self-healing test frameworks.", "risks":"AI-generated tests can look convincing while checking the wrong behaviour. Generated tests are sometimes flaky and need review by a person. Sending source code to external AI services can create data protection and confidentiality concerns.","defect": "Industry surveys report that AI-assisted testing tools typically find 10 to 20 percent more defects before release, mainly edge cases that manual test writers miss. Results vary widely and depend on the quality of the existing test suite.", "training": "Teams adopting AI testing tools usually spend two to four weeks on onboarding. Typical extra costs are staff training, integration with existing build pipelines and ongoing review of generated tests."}
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
        return f"ERROR: Response content is empty. Stop reason {response.stop_reason}"
    return response.content[0].text

def run_delegation(args):
    if args["agent"] == "search":
        return search_subagent(args["task"])
    elif args["agent"] == "document":
        return document_subagent(args["task"], args.get("document"))

def coordinator(messages):
    return client.messages.create(model="code", max_tokens=10000, system=COORDINATOR_PROMPT, tools=TOOLS, messages=messages)

def run_agent(question):
    messages=[{"role":"user","content":question}]
    result = coordinator(messages)
    messages.append({"role":"assistant","content":result.content})
    result = run_tool_loop(messages, result)
    for attempt in range(MAX_REFINEMENTS):
        if result.stop_reason != "end_turn" or not result.content:
            break
        report = result.content[0].text
        gaps = check_coverage(report)
        if gaps.startswith("ERROR:"):
            print(gaps)
            break
        print("Coverage check:", gaps)
        if gaps.strip() == "NONE":
            break
        print(f"--- Refinement {attempt +1} ---")
        messages.append({"role":"user","content":f"The following gaps have been found: {gaps} \n Delegate one targeted query per gap!Then write the complete updated report! If an internal document does not contain the information, do not ask the same document again; ask the search agent for general industry information instead."})
        result = coordinator(messages)
        messages.append({"role":"assistant","content":result.content})
        result = run_tool_loop(messages, result)
    print(f"Stop reason: {result.stop_reason}")
    if result.stop_reason != "end_turn":
        return ("Limit of iterations reached. Please try a differnt prompt.")
    return result.content[0].text

def check_coverage(report):
    return run_subagent(
        f"RULES: Check the report created by the assistance against the users prompt. Checklist criterias are tools; risks; pilot results (coverage, time saved, defect detection); costs (licence and training).\n\n" 
        f"USER PROMPT: {USER_PROMPT}.\n\n" 
        f"REPORT: {report}\n\n"
        "YOUR OUPUT: list every area the report doesn't cover with concrete facts, one per line, each phrased as a short search question. Only the four listed areas may be reported. Do not add areas of your own. An area counts as covered only if the report states at least one concrete fact (a number or a specific finding) for EACH item listed in its parentheses. For pilot results that means coverage, time saved and defect detection. For costs that means licence and training. If any item is missing, the whole area is not covered, and your question should name the missing item. Judge each area as covered or not covered, and report only the not-covered ones. If everything is covered, answer exactly: NONE."
    )

def run_tool_loop(messages, result):
    iterations = int(0)
    print(f"Coordinator reply: Number of tool_use requests: {len([r for r in result.content if r.type == "tool_use"])}")
    while result.stop_reason == "tool_use" and iterations < MAX_ITERATIONS:
        tool_results = {"role":"user","content":[]}
        blocks = list(i for i in result.content if i.type == "tool_use")
        with ThreadPoolExecutor() as pool:
            t0 = time.perf_counter()
            outputs = list(pool.map(run_delegation, [b.input for b in blocks]))
            for b, o in zip (blocks, outputs):
                tool_results["content"].append({
                    "type":"tool_result",
                    "tool_use_id":b.id,
                    "content":o
                })
                print("\n-- Tool request --", b.id, b.name, b.input)
                print("\n-- Tool output --", o)
            print(f"-- Tool round: {iterations +1} terminated: {len(blocks)} delegations in {time.perf_counter()-t0:.3}s --")
        messages.append(tool_results)
        result = coordinator(messages)
        messages.append({"role":"assistant","content":result.content})
        iterations = iterations + 1
    return result

print(run_agent(USER_PROMPT))


JOBS = [
    {'agent': 'search', 'task': 'How is AI changing software testing? What AI-powered testing tools exist (e.g., test generation, self-healing tests, AI test automation platforms) and what do they do?'},
    {'agent': 'search', 'task': 'What are the risks and challenges of using AI in software testing (e.g., false confidence, test bias, hallucinated tests, security and data privacy concerns, over-reliance)?'},
    {'agent': 'document', 'document': 'cost_notes.txt', 'task': 'What are the licence costs for the AI software testing tools under evaluation? Extract any pricing figures, per-seat or per-tool costs.'},
    {'agent': 'document', 'document': 'testing_report.txt', 'task': 'What were the results of the internal pilot of AI in software testing? Extract all metrics, outcomes, successes and problems reported.'}
]
def benchmark():
    t0 = time.perf_counter()
    for job in JOBS:
        run_delegation(job)
    print(f"Sequential took {time.perf_counter() -t0:.3f} seconds")
    t1 = time.perf_counter()
    with ThreadPoolExecutor() as pool:
        list(pool.map(run_delegation, JOBS))
    print(f"Thread took {time.perf_counter() -t1:.3f} seconds")

# benchmark()
# benchmark()