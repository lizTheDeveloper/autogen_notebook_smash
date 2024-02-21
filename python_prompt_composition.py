environmental_context = "You are on a debian system, with tools like nmap, netcat, and curl installed. You have access to a python3 interpreter."

tasks = [
    "Run an nmap scan on the target machine.",
    "Use netcat to connect to the target machine on port 80.",
    "Use curl to download the index page of the target machine."
]
task_str = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])

prompt = f"""{environmental_context}
{task_str}
"""

print(prompt)