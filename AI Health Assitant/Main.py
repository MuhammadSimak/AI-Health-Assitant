from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
import json
import os
from pathlib import Path

# Load environment variables from apikey.env (if present)
load_dotenv(dotenv_path='apikey.env')

# --- Configuration / paths ---
reports_dir = Path("Medical Reports")
# NOTE: keep the filename exactly as in your folder (you provided this name earlier)
medical_report_filename = "Medical Rerort - Michael Johnson - Panic Attack Disorder.txt"
medical_report_path = reports_dir / medical_report_filename

# --- Read the medical report (utf-8) ---
if not medical_report_path.exists():
    raise FileNotFoundError(f"Medical report not found: {medical_report_path.resolve()}\n"
                            "Make sure the file exists and the filename is correct.")

with medical_report_path.open("r", encoding="utf-8") as f:
    medical_report = f.read()

# --- Create agents ---
agents = {
    "Cardiologist": Cardiologist(medical_report),
    "Psychologist": Psychologist(medical_report),
    "Pulmonologist": Pulmonologist(medical_report)
}

# Function to run each agent and get their response (with error handling)
def get_response(agent_name, agent):
    try:
        response = agent.run()
        # ensure a string (avoid None)
        if response is None:
            return agent_name, None, f"{agent_name} returned None"
        return agent_name, response, None
    except Exception as e:
        # return the exception message so we can inspect later
        return agent_name, None, f"Error running {agent_name}: {e}"

# Run the agents concurrently and collect responses
responses = {}
errors = {}
with ThreadPoolExecutor() as executor:
    futures = {executor.submit(get_response, name, agent): name for name, agent in agents.items()}
    for future in as_completed(futures):
        agent_name, response, err = future.result()
        responses[agent_name] = response
        if err:
            errors[agent_name] = err
            print(f"[Warning] {err}")

# If some agent responses are missing, fill with a placeholder so the team agent can still run
for name in agents.keys():
    if name not in responses or responses[name] is None:
        responses[name] = f"(No report returned from {name})"

# --- Create and run the multidisciplinary team agent ---
team_agent = MultidisciplinaryTeam(
    cardiologist_report=responses.get("Cardiologist"),
    psychologist_report=responses.get("Psychologist"),
    pulmonologist_report=responses.get("Pulmonologist")
)

try:
    final_diagnosis = team_agent.run()
except Exception as e:
    print(f"[Error] MultidisciplinaryTeam failed: {e}")
    final_diagnosis = None

# Make sure final_diagnosis is a string and not None
final_diagnosis_str = final_diagnosis if isinstance(final_diagnosis, str) else (str(final_diagnosis) if final_diagnosis is not None else "")

final_diagnosis_text = "### Final Diagnosis:\n\n" + (final_diagnosis_str or "No diagnosis returned (LLM call failed or returned nothing).")

# --- Write output safely with utf-8 ---
txt_output_path = Path("results") / "final_diagnosis.txt"
txt_output_path.parent.mkdir(parents=True, exist_ok=True)

with txt_output_path.open("w", encoding="utf-8") as txt_file:
    txt_file.write(final_diagnosis_text)

print(f"Final diagnosis has been saved to {txt_output_path.resolve()}")

# Optional: also print any agent errors summary
if errors:
    print("\nAgent errors encountered:")
    for k, v in errors.items():
        print(f" - {k}: {v}")



