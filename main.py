from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
PYTHON_ROOT = PROJECT_ROOT / "python"

if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from src.bank_system import BankSystem


def main():
    bank_system = BankSystem()
    bank_system.run()


if __name__ == "__main__":
    main()