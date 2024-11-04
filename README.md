ACME Inc. Customer Support Bot
Overview
This project implements Openai's example customer support bot for ACME Inc. using OpenAI's GPT-4 API. The bot is designed to assist users with various inquiries, including sales, refunds, and issues related to products. It utilizes multiple agents, each with specific roles and instructions to handle customer interactions effectively.

Features
Multi-Agent System: The bot consists of different agents, including:

Triage Agent: Directs users to the appropriate department based on their inquiries.
Sales Agent: Assists users with product inquiries and order placement.
Refund Agent: Handles refund requests and processes them.
Issues and Repairs Agent: Addresses user issues and proposes solutions.
Tool Integration: The bot can execute functions such as looking up items, placing orders, and processing refunds.

Dynamic Interaction: The bot engages users by asking probing questions to better understand their needs.

Requirements
Python 3.7 or higher
OpenAI Python client library
Pydantic library
Installation
Clone the repository:

bash
Insert Code
Edit
Copy code
git clone <repository-url>
cd <repository-directory>
Install the required packages:

bash
Insert Code
Edit
Copy code
pip install openai pydantic
Set up your OpenAI API key as an environment variable:

bash
Insert Code
Edit
Copy code
export OPENAI_API_KEY='your-api-key'
Usage
To run the customer support bot, execute the following command:

bash
Insert Code
Edit
Copy code
python routines_and_handoffs.py
The bot will prompt you for input. You can interact with it by typing your queries related to sales, refunds, or any issues with products.

Functionality
Agents
Triage Agent: Introduces itself and gathers information to direct the customer to the right department.
Sales Agent: Engages users in conversation to sell products and process orders.
Refund Agent: Assists users with refund requests and executes them if necessary.
Issues and Repairs Agent: Addresses user issues and proposes fixes.
Tool Functions
look_up_item(search_query): Finds the item ID based on the user's query.
execute_refund(item_id, reason): Processes a refund for the specified item ID.
place_order(item_name): Places an order for the specified item.
Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contact
For any questions or inquiries, please contact [dcarter7279@gmail.com].
