# Week 4 — Day 1

## Task(s) Assigned
What is Generative AI? 
Generative AI vs traditional ML 
What is an LLM? 
Large Language Models 
Tokens 
Tokenization 
Context window 
Parameters 
Inference 
Temperature 
System/user/assistant messages 
Prompt engineering 
Zero-shot prompting 
Few-shot prompting 
Role-based prompting 
Structured outputs 
AI limitations and hallucinations 
Hands-on: 
Work with an LLM API. 
Create multiple prompts for different tasks. 
Compare prompt quality and outputs. 
## What I Did
Firstly, I built my own environment and learned the basics of Generative AI and Large Language Models. I wrote the code to utilize these concepts with the Anthropic Python SDK,I also made a .env whih contains my API Keys to sucure them and prevent any misusage. I wrote a Python script to make an API call, reading my API key from environment variables using python-dotenv. I wrote a reusable call_llm() function that includes a flow to handle the response I would expect from the LLM. I also set up limits for the number of tokens it can return, how warm or cool it should be, and how to keep track of the tokens. I added support for system prompts into the function as well.

I then went through a few prompt engineering techniques and wrote some code to try them out. I created two prompts—one zero-shot and one few-shot with three examples—to see how examples can influence what the model will generate for sentiment classification. I created a system message for role-based prompting, which asked the model to behave as a "terse senior code reviewer" to observe how instructions are supposed to affect the way the model behaves and speaks. I also wrote a prompt to output the information as JSON, in addition to the json.loads() logic to process the expected response, to learn how to process structured data programmatically. Also, I wrote a piece of code that compares temperatures of 0.0 and 1.0 for a creative prompt to investigate, in theory, the impact randomness can have on generation; however, some models use different values. Lastly, I added the functionality to read the number of tokens in the input and output from the API's expected response, where I managed to bridge the theory of LLM interactions with actual code._Summary of what I learned today, in my own words._

## Key Learnings
I Learned that Unlike traditional machine learning which classifies or predicts data, Generative AI generates new content using Large Language Models (LLMs) that process human language by tokenizing it instead of processing whole words. During inference, these models utilize a context window and learned parameters, with settings such as temperature affecting how predictable and varied the outputs will be. Prompt engineering is a crucial aspect of effective interaction, as it influences how the assistant behaves, how it writes, and what it writes. You can use techniques like zero-shot, few-shot, and role-based prompting, or output structured responses to help the model perform well on programmatic or creative tasks. It is important to note that the output of LLM models is not always accurate, often hallucinating information, and when accuracy is a must, it should always be validated; using API tokens to track the usage of these models allows for monitoring and optimization.

## Files in this folder
- `Tasksw4d1.py`  — Contains python code of Anthropic API implementation.
- `.env`— Contains My Api keys for antropic.
