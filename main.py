from fastapi import FastAPI
import uvicorn
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.llm.groq import Groq
from dotenv import load_dotenv
import json
import os
import requests
load_dotenv()
app = FastAPI()

@app.get("/find-cve")
async def find_vulnerabilities(software: str, version: str):
    assistant = Assistant(
        llm=Groq(model="llama3-groq-70b-8192-tool-use-preview"),
        tools=[DuckDuckGo()],
        description="You are a cybersecurity research expert and your job is to research and find out any vulnerabilties in that software version in a specific JSON format. Double check if the vulnerabilities specifically exist for that software version only",
        instructions=[
            "Provide the response strictly in the following JSON format without any pretext or disclaimer",
            """Required Output format: {"software":"software-name","version":"version-number","vulnerabilities":[{"cveid":"cve-id-of-vulnerability","reference":"url"}]} """,
            "Add more vulnerabilities as needed but in a JSON format",
            "ONLY Respond back with json. Nothing extra."
        ],
        debug_mode=False
    )
    
    # Generate response
    output = assistant.run(f"{software} {version} Vulnerability List", stream=False)
    # print(f"Agent Raw Response: {output}")

    # Convert the string to a Python dictionary
    response = json.loads(output)

    # Now clean_response is a proper dictionary
    # print(json.dumps(response, indent=4))

    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
