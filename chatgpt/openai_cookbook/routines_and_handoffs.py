from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
import json, inspect

client = OpenAI()

# Customer Service Routine
system_message = (
    "You are a customer support agent for ACME Inc."
    "Always answer in a sentence or less."
    "Follow the following routine with the user:"
    "1. First, ask probing questions and understand the user's problem deeper. \n"
    "- unless the user has already provided a reason. \n"
    "2. Propose a fix (make one up). \n"
    "3. ONLY if not satisfied, offer a refund. \n"
    "4. If accepted, search for the ID and then execute refund."
    ""
)

def look_up_item(search_query):
    """Use to find item ID.
    Search query can be a description or keywords."""
    
# return hard-coded item ID - in reality would be a lookup
    return "item_132612938"

def execute_refund(item_id, reason="not provided"):
    
    print("Summary:", item_id, reason) # lazy summary
    return "success"

def run_full_turn(system_message, messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_message}] + messages,
    )
    message = response.choices[0].message
    messages.append(message)
    
    if message.content: print("Assistant:", message.content)
    
    return message

messages = []
while True:
    user = input("User: ")
    messages.append({"role": "user", "content": user})
    
    run_full_turn(system_message, messages)
    
def function_to_schema(func) -> dict:
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }
    
    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )
        
    paramaters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise ValueError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}
        
    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect.Parameter.empty
    ]
    
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip(),
            "parameters": {
                "type": "object",
                "properties": parameters, 
                "required": required
            },
        },
    }
    
messages = []

tools = [execute_refund, look_up_item]
tool_schemas = [function_to_schema(tool) for tool in tools]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Look up the black boot."}],
    tools= tool_schemas,
)
message = response.choices[0].message

message.tool_calls[0].function

tools_map = {tool.__name__: tool for tool in tools}

def execute_tool_call(tool_call, tools_map):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    
    print(f"Assistant: {name}({args})")
    
# call corresponding function with provided arguments
    return tools_map[name](**args)

for tool_call in message.tool_calls:
    result = execute_tool_call(tool_call, tools_map)
    
    # add result back to conversation
    result_message = {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
    messages.append(result_message)

tools = [execute_refund, look_up_item]

def run_full_turn(agent, messages):
    
    current_agent = agent
    num_init_messages = len(messages)
    messages = messages.copy()
    
    while True:
        
        # turn python functions into tools and save a reverse map
        tool_schemas == [function_to_schema(tool) for tool in current_agent.tools]
        tool_map = {tool.__name__: tool for tool in current_agent.tools}
        
        # === 1. get openai completetion ===
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content" : current_agent.instructions}]
            + messages,
            tools=tool_schemas or None,
        )
        message = response.choices[0].message
        messages.append(message)
        
        if message.content: # print assistant response
            print("{current_agent.name}:", message.content)
            
        if not message.tool_calls: # if finished handling tool calls, break
            break
        
        # === 2. handle tool calls ===
        
        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools, current_agent.name)
            
            if type(result) is Agent: # if agent transfer, update current agent
                current_agent = result
                result = (
                    f"Transferred to {current_agent.name}. Adopt persona immediately"
                )

            # add result back to conversation
            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)
            
    # === 3. return new messages ===
    return Response(agent=current_agent, messages=messages[num_init_messages:])

def execute_tool_call(tool_call, tools, agent_name):
    name = tool_call.function.name
    args = jsn.loads(tool_call.function.arguments)
    
    print(f"{agent_name}:", f"{name}({args})")
    
    # call corresponding function with provided arguments
    return tools[name](**args) # call corresponding function with provided arguments

messages = []
while True:
    user = input("User: ")
    messages.append({"role": "user", "content": user})
    
    new_messages = run_full_turn(system_message, tools, messages)
    messages.extend(new_messages)
    
class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-4o-mini"
    instructions: str = "You are a helpful Agent"
    tools: list = []
    
def execute_refund(item_name):
    return "success"

refund_agent = Agent(
    name="Refund Agent",
    instructions="You are a refund agent. Help the user with refunds.",
    tools=[execute_refund],
)

def transfer_to_refunds():
    return refund_agent

def place_order(item_name):
    return "success"

sales_assistant = Agent(
    name="Sales Assistant",
    instructions="You are a sales assistant. Sell the user a product.",
    tools=[place_order],
)

messages = []
user_query = "Please an order for a black boot."
print("User:", user_query)
messages.append({"role": "user", "content": user_query})

response = run_full_turn(sales_assistant, messages) # sales assistant
messages.extend(response)

user_query = "Actually, I want a refund." # implitly refers to the last item
print("User:", user_query)
messages.append({"role": "user", "content": user_query})
response = run_full_turn(refund_agent, messages) # refund agent

class Response(BaseModel):
    agent: Optional[Agent]
    messages: list 
    
def escalate_to_human(summary):
    """Only call this if explicitly asked to."""
    print("Escalating to human agent...")
    print("\n=== Escalation Report ===")
    print(f"Summary: {summary}")
    print("=========================\n")
    exit()


def transfer_to_sales_agent():
    """User for anything sales or buying related."""
    return sales_agent


def transfer_to_issues_and_repairs():
    """User for issues, repairs, or refunds."""
    return issues_and_repairs_agent


def transfer_back_to_triage():
    """Call this if the user brings up a topic outside of your purview,
    including escalating to human."""
    return triage_agent


triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a customer service bot for ACME Inc. "
        "Introduce yourself. Always be very brief. "
        "Gather information to direct the customer to the right department. "
        "But make your questions subtle and natural."
    ),
    tools=[transfer_to_sales_agent, transfer_to_issues_and_repairs, escalate_to_human],
)


def execute_order(product, price: int):
    """Price should be in USD."""
    print("\n\n=== Order Summary ===")
    print(f"Product: {product}")
    print(f"Price: ${price}")
    print("=================\n")
    confirm = input("Confirm order? y/n: ").strip().lower()
    if confirm == "y":
        print("Order execution successful!")
        return "Success"
    else:
        print("Order cancelled!")
        return "User cancelled order."


sales_agent = Agent(
    name="Sales Agent",
    instructions=(
        "You are a sales agent for ACME Inc."
        "Always answer in a sentence or less."
        "Follow the following routine with the user:"
        "1. Ask them about any problems in their life related to catching roadrunners.\n"
        "2. Casually mention one of ACME's crazy made-up products can help.\n"
        " - Don't mention price.\n"
        "3. Once the user is bought in, drop a ridiculous price.\n"
        "4. Only after everything, and if the user says yes, "
        "tell them a crazy caveat and execute their order.\n"
        ""
    ),
    tools=[execute_order, transfer_back_to_triage],
)


def look_up_item(search_query):
    """Use to find item ID.
    Search query can be a description or keywords."""
    item_id = "item_132612938"
    print("Found item:", item_id)
    return item_id


def execute_refund(item_id, reason="not provided"):
    print("\n\n=== Refund Summary ===")
    print(f"Item ID: {item_id}")
    print(f"Reason: {reason}")
    print("=================\n")
    print("Refund execution successful!")
    return "success"


issues_and_repairs_agent = Agent(
    name="Issues and Repairs Agent",
    instructions=(
        "You are a customer support agent for ACME Inc."
        "Always answer in a sentence or less."
        "Follow the following routine with the user:"
        "1. First, ask probing questions and understand the user's problem deeper.\n"
        " - unless the user has already provided a reason.\n"
        "2. Propose a fix (make one up).\n"
        "3. ONLY if not satesfied, offer a refund.\n"
        "4. If accepted, search for the ID and then execute refund."
        ""
    ),
    tools=[execute_refund, look_up_item, transfer_back_to_triage],
)

agent = triage_agent
messages = []

while True:
    user = input("User: ")
    messages.append({"role": "user", "content": user})

    response = run_full_turn(agent, messages)
    agent = response.agent
    messages.extend(response.messages)