import anthropic
client = anthropic.Anthropic()
MAX_ITERATIONS = 20
TOOLS = [
    {
        "name":"calculator",
        "description":"Returns the solution to a mathematical equation without variables. Use when user asks to solve a mathematical expression",
        "input_schema":{
            "type":"object",
            "properties":{
                "expression":{"type":"string","description":"Expression like an Addition, Subtraction, Multiplikation or devision etc. or a mix of multiple expressions, e.g 123 + 456 * 789."}
            },
            "required":["expression"]
       }
    },
    {
        "name":"search_stub",
        "description":"Returns the list of web search results after inputing a query. Use when user aks to search the web.",
        "input_schema":{
            "type":"object",
            "properties":{
                "query":{"type":"string","description":"A String that can be stated as a question or just as one or multiple keywords, e.g. 'What year was Obama born?' or 'Obama Date of Birth'"}
            },
            "required":["query"]
        }
    }
]

def calculator(expression):
    return f"Result is: {str(eval(expression))}"

def search_stub(query):
    return f"No results could be found in the web for '{query}'"

def run_tool(name, tool_input):
    if name == "calculator":
        return calculator(tool_input["expression"])
    elif name == "search_stub":
        return search_stub(tool_input["query"])
    return f"Unknown tool {name}"

def llm_call(messages):
    result = client.messages.create(
                model="code", 
                max_tokens=1000,
                tools=TOOLS,
                messages=messages
            )
    
    return result

def run_agent(question):
    
    messages=[{"role":"user", "content":question}]
    result = llm_call(messages)
    messages.append({"role":"assistant", "content":result.content})
    iterations = int(0)

    while result.stop_reason == "tool_use" and iterations < MAX_ITERATIONS:
        tool_results = {"role":"user", "content":[]}
        for item in result.content:
            if item.type == "tool_use":
                print("Tool request:", item.id, item.name, item.input)
                tool_results["content"].append(
                    {
                        "type":"tool_result",
                        "tool_use_id":item.id,
                        "content":run_tool(item.name, item.input)
                    }                    
                )
        messages.append(tool_results)
        result = llm_call(messages)
        messages.append({"role":"assistant", "content":result.content})
        iterations = iterations + 1
    print(result.stop_reason)
    if result.stop_reason != "end_turn":
        return ("Limit of iterations reached. Please try a differnt prompt.")
    return result.content[0].text


# print(run_agent("What is 123 * 45? Then search the web for 'cats'."))
# print(run_agent("Search the web for the latest news about electric cars."))
print(run_agent("What is (17 + 5) * 3?"))
print(run_agent("Hello, who are you in one sentence?"))
print(run_agent("Calculate 99 * 99, then use the search tool to look up 'Python'."))