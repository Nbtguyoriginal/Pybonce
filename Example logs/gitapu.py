import requests

def get_github_api_version():
    response = requests.get("https://api.github.com")
    
    if response.status_code == 200 and 'X-GitHub-Media-Type' in response.headers:
        media_type = response.headers['X-GitHub-Media-Type']
        version = media_type.split(";")[0].split(".")[-1]
        return version
    else:
        return None

current_version = get_github_api_version()
if current_version:
    print(f"Current GitHub API version: {current_version}")
else:
    print("Failed to retrieve GitHub API version.")
