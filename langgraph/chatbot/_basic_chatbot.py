# from typing import TypedDict, Annotated
# from langgraph.graph import add_messages, StateGraph, END
# from langchain_groq import ChatGroq
# from langchain_core.messages import AIMessage, HumanMessage
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatGroq(model="llama-3.1-8b-instant")

# class BasicChatState(TypedDict):
#     messages: Annotated[list, add_messages]

# def chatbot(state: BasicChatState):
#     return {
#         "messages": [llm.invoke(state["messages"])]
#     }

# graph = StateGraph(BasicChatState)

# graph.add_node("chatbot", chatbot)
# graph.set_entry_point("chatbot")
# graph.add_edge("chatbot", END)

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


from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

# Define the chat state
class BasicChatState(TypedDict):
    messages: list

# Node function that adds LLM response to messages
def chatbot(state: BasicChatState) -> BasicChatState:
    response = llm.invoke(state["messages"])
    return {
        "messages": state["messages"] + [response]
    }

# Define the LangGraph
graph = StateGraph(BasicChatState)
graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)

# Compile the app
app = graph.compile()

# Run the chatbot loop
messages = []

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "end"]:
        break

    messages.append(HumanMessage(content=user_input))

    result = app.invoke({"messages": messages})
    messages = result["messages"]

    # Get latest AI response
    latest_ai_message = next((msg for msg in reversed(messages) if isinstance(msg, AIMessage)), None)
    if latest_ai_message:
        print("AI:", latest_ai_message.content)
