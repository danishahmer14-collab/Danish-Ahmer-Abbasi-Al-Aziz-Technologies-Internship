# Week 1 — Day 4

## Task(s) Assigned
Working with files 
 CSV files 
 JSON 
 Exception handling 
 Logging basics 
 Environment variables 
 .env 
 API requests 
 HTTP basics 
 requests 
 Introduction to NumPy 
 Arrays 
 Vectorized operations 
 Basic numerical operations 
Hands-on: 
 Read and process CSV/JSON data. 
 Consume a public API using Python. 
 Perform basic numerical operations using NumPy. 

## What I Did
First I created my own Enviroment then learned to create a textfile read write and append text file then i learned to write and read a csv file then I learned to covert python dictionary into json string then make python object of json string and manipulate(read/write) data in json file using python then I revised the concept of Day for Exeption Handling its useful to prevent our application from crashing due to minor error logging is used to check what actions made the error or application to crash then we can apply try eccept init to prevent it. .envfile is used to store secret apli keys or password outside the code so that they accidently dont get commited on github or anyother means to read .env file python needs dotenv module which is installed by pip install python-dotenv load_dotenv() to load variables from .env file I added .env file to your gitignore then I reseached about HTTP basics which include GET to retrieve data
POST to send/create data PUT/PATCH to update data DELETE to remove data then for Api's i leanred request.get to use an opensource wheather Api and made a console based wheather forecast app then i practiced numpy library through code arrays in numpy vectorized operations and basic numerical operations 

## Key Learnings
I learned creating a textfile,csvfile,Jsonfile and manipulating(reading/writing/editing) it I was familiar with concept of numpy Exeption handling and logging basics which i revised then i Learned about .env file how to read it using python importance of protecting APi's and password data security then i learned about Httpt Requests and API Integration I intregrated an APi to make a wheather forecast console based application  

## Files in this folder
Files.py contains Basic file handling: writing, reading, and appending text, csvfiles.py contains Writing and reading CSV data, Json.py consists of Converting Python data to/from JSON using `json.dumps()`, `json.loads()`, `json.dump()`, `json.load()` , ExpHandling.py contains Exception handling using try/except/else/finally , LoggingBasics.py has Logging basics , read_env.py contains Reading environment variables from a `.env` file using `python-dotenv`, for securely storing secrets like API keys. numpy.py contains Introduction to NumPy: creating arrays, vectorized operations, and basic numerical operations (sum, mean, max, min, std). WheatherApi.py  Consuming a public weather API (Open-Meteo) using the requests library, with error handling for failed requests. student.csv has Sample CSV data file used for testing csvfiles.py, notes.txt has Sample text file used for testing `Files.py`
