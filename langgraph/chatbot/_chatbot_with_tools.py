# from typing import TypedDict, Annotated
# from langgraph.graph import add_messages, StateGraph, END
# from langchain_groq import ChatGroq
# from langchain_core.messages import AIMessage, HumanMessage
# from dotenv import load_dotenv
# # from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain_tavily import TavilySearchResults
# from langgraph.prebuilt import ToolNode

# load_dotenv()

# class BasicChatBot(TypedDict):
#     messages: Annotated[list, add_messages]

# search_tool = TavilySearchResults(max_results=2)
# tools = [search_tool]

# llm = ChatGroq(model="llama-3.1-8b-instant")

# llm_with_tools = llm.bind_tools(tools=tools)

# def chatbot(state: BasicChatBot):
#     return {
#         "messages": [llm_with_tools.invoke(state["messages"])], 
#     }

# def tools_router(state: BasicChatBot):
#     last_message = state["messages"][-1]

#     if(hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0):
#         return "tool_node"
#     else: 
#         return END
    

# tool_node = ToolNode(tools=tools)

# graph = StateGraph(BasicChatBot)

# graph.add_node("chatbot", chatbot)
# graph.add_node("tool_node", tool_node)
# graph.set_entry_point("chatbot")

# graph.add_conditional_edges("chatbot", tools_router)
# graph.add_edge("tool_node", "chatbot")

# app = graph.compile()

# while True: 
#     user_input = input("User: ")
#     if(user_input in ["exit", "end"]):
#         break
#     else: 
#         result = app.invoke({
#             "messages": [HumanMessage(content=user_input)]
#         })

#         print(result)

from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.prebuilt import ToolNode
# from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch  # ✅ Correct class name



from dotenv import load_dotenv

load_dotenv()

# Step 1: Define State
class BasicChatBot(TypedDict):
    messages: Annotated[list, add_messages]

# Step 2: Define Tool (with correct name)
# search_tool = TavilySearchResults(max_results=2)
search_tool = TavilySearch(max_results=2)
search_tool.name = "brave_search"  # LLM hallucinates this name
tools = [search_tool]

# Step 3: Setup Groq LLM and bind tools
llm = ChatGroq(model="llama-3.1-8b-instant")
llm_with_tools = llm.bind_tools(tools=tools)  # ✅ no system_message here

# Step 4: Node that calls the LLM
def chatbot(state: BasicChatBot) -> BasicChatBot:
    response = llm_with_tools.invoke(state["messages"])
    return {
        "messages": state["messages"] + [response],
    }

# Step 5: Router to decide tool use
def tools_router(state: BasicChatBot) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0:
        return "tool_node"
    else:
        return END

# Step 6: ToolNode for actual tool execution
tool_node = ToolNode(tools=tools)

# Step 7: Create LangGraph
graph = StateGraph(BasicChatBot)
graph.add_node("chatbot", chatbot)
graph.add_node("tool_node", tool_node)
graph.set_entry_point("chatbot")
graph.add_conditional_edges("chatbot", tools_router)
graph.add_edge("tool_node", "chatbot")

# print(graph.draw_mermaid())#


app = graph.compile()

# Step 8: Run Chat Loop
messages = []

print("🤖 AI Chatbot with Tools (type 'exit' to quit)")
while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "end", "quit"]:
        break

    messages.append(HumanMessage(content=user_input))
    result = app.invoke({"messages": messages})
    messages = result["messages"]

    last_ai = next((msg for msg in reversed(messages) if isinstance(msg, AIMessage)), None)
    if last_ai:
        print("AI:", last_ai.content)
# Step 9: Save the graph to a file
graph.save_graph_to_file("chatbot_with_tools.groq")