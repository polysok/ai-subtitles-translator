import requests

from app.config import Config


SUCCESS_CODE = 200
config = Config()
def stream_request_llm_server(prompt:str, lang:str) -> str|None:
    """Send request to llm server."""
    url = f"{config.LLM_ENDPOINT}/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization":f"Bearer {config.LLM_APIKEY}"}
    prompt = f"Translate in {lang} the sentences in the following array and respect the original json format: \n" + prompt
    data = {
        "model": config.LLM_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    resp =  requests.post(url, json=data, headers=headers, stream=False)
    if resp.status_code == SUCCESS_CODE:
        return resp.json()['choices'][0]['message']['content']

    print(f"Error during the request: {resp.status_code} - {resp.text}")
    return None

