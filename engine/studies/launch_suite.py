import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from engine.studies.orchestrator import TrialOrchestrator

def execute_all_trials():
    runner = TrialOrchestrator()
    experiments = [f"exp{i}" for i in range(1, 10)]
    for exp in experiments:
        print(f"Executing {exp}...")
        res = runner.execute_trial(exp)
        print(f"Completed {exp}: {res['title']}")

if __name__ == "__main__":
    execute_all_trials()

