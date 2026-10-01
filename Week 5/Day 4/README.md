# Week 5 — Day 4

## Task(s) Assigned
What is an AI Agent? 
AI Engineering 
Agent vs chatbot 
Tool-using agents 
Function/tool calling 
Agent planning 
External tools 
APIs as tools 
Database tools 
Web/search tool concepts 
Agent safety and limitations 
Building AI APIs with FastAPI 
Request/response models 
API endpoints 
Environment variables 
API documentation 
Basic deployment concepts 
Hands-on: 
Build a FastAPI endpoint for an AI application. 
Create an AI agent capable of calling at least one external tool. 

## What I Did
Firstly I created my own Enviroment then I started by studying the theory behind AI agents, including how they differ from chatbots, how tool calling works, how agents plan their steps in a loop, and what safety limits they need. After that I set up my project in VS Code by creating a Python virtual environment and installing the required packages (fastapi, uvicorn, groq, httpx and python-dotenv) from a requirements.txt file. I stored my Groq API key and model name (openai/gpt-oss-120b) in a .env file and loaded them with python-dotenv so that no secret is written directly in the code.

For the hands-on part, I built two tools in tools.py. The first is a weather tool that works as an external API tool and fetches live weather data for any city from the Open-Meteo API. The second is a database tool that searches a SQLite products table using safe parameters like category and maximum price instead of raw SQL. Then I wrote the agent loop in agent.py using the Groq API. The loop sends the user message and tool descriptions to the model, runs any tool the model asks for, sends the result back, and repeats until the model gives a final answer, with a maximum of five steps as a safety limit.

Finally, I built the FastAPI application in main.py with Pydantic request and response models, a /health endpoint, and a /chat endpoint that calls the agent and returns a clear error if something fails. I ran into a small problem because my files were saved with capital letters and Python imports are case-sensitive, so I renamed them to lowercase. I then started the server with uvicorn and tested it using the automatically generated Swagger documentation at /docs. When I sent the message "What's the weather in Lahore?", I received a 200 response containing the live temperature and humidity, with "get_weather" listed in tools_used. This confirmed that the agent successfully called the external tool.

## Key Learnings
The main thing I learned today is that an AI agent is much more than a chatbot. A chatbot only replies with text based on its training data, while an agent uses a language model to decide what to do, calls tools to fetch live data or take actions, checks the results, and keeps going until the goal is complete. I also learned that in tool calling the model never runs code itself. It only asks for a tool by name with arguments, and my own code executes the function and returns the result. This keeps me in control of what the agent can actually do, and it means the tool names and descriptions must be written clearly so the model can choose the right one.

I also learned about the risks and limits of agents. They can hallucinate, pick the wrong tool, get stuck in loops, and cost more than a single model call. To handle this, I used a step limit, input validation with Pydantic, tool errors returned as data instead of crashing, and narrow parameters for the database tool instead of letting the model write SQL. For risky actions in a real product, a human approval step would also be needed.

On the API side, I learned that FastAPI makes it easy to build AI services because Pydantic validates the input automatically, endpoints are simple Python functions, and the interactive documentation is generated for free. I also understood why secrets belong in environment variables and should never be committed to git. Deploying the app is basically running uvicorn on a server while setting the API key in the platform's environment settings. Lastly, I noticed that different providers use slightly different tool-calling formats, but the core idea of the agent loop stays the same.

## Files in this folder
- `main.py` — FastAPI application with the /health and /chat endpoints and the request/response models.
- `agent.py` — the agent loop that talks to the Groq model, handles tool calls and returns the final answer.
- `tools.py` — the weather API tool, the product database tool, their schemas, and the tool dispatcher.
- `requirements.txt` — list of Python packages needed to run the project.
