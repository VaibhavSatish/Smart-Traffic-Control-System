from datetime import datetime
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = REPOSITORY_ROOT / "results"


def create_run_directory(name):
    """Create and return a uniquely named directory directly under results/."""
    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = RESULTS_ROOT / f"{name}_{timestamp}"
    suffix = 1
    while run_dir.exists():
        run_dir = RESULTS_ROOT / f"{name}_{timestamp}_{suffix}"
        suffix += 1
    run_dir.mkdir()
    return run_dir
