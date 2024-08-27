from fastapi import FastAPI, Request, HTTPException
import httpx
import os
import subprocess

app = FastAPI()

GITHUB_TOKEN = ""  # Replace with your GitHub Personal Access Token
GITHUB_API_URL = "https://api.github.com"

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()

    # Ensure it's a pull request event
    if payload.get("action") == "opened" and "pull_request" in payload:
        pr_number = payload["pull_request"]["number"]
        repo_full_name = payload["repository"]["full_name"]
        clone_url = payload["repository"]["clone_url"]

        # Clone the repo and checkout the PR branch
        repo_path = os.path.join("/app/repos", repo_full_name)
        os.makedirs(repo_path, exist_ok=True)
        subprocess.run(["git", "clone", clone_url, repo_path])
        
        # Checkout the PR branch
        branch_name = f"pr/{pr_number}"
        subprocess.run(["git", "fetch", "origin", f"pull/{pr_number}/head:{branch_name}"], cwd=repo_path)
        subprocess.run(["git", "checkout", branch_name], cwd=repo_path)

        # Your code is now in /app/repos/{repo_full_name}
        print(f"Repository cloned and checked out to PR branch: {repo_path}")
    
    return {"status": "ok"}
