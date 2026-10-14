# Warehouse Asset Maintenance Registry — Final Deliverables

## Included
- `maintenance_system.py` — cleaned implementation.
- `issues.md` — issue table and fixes, with line references to the original source.
- `reflection.md` — four reflection answers. The uploaded ZIP did not contain the separate lab handout, so these use standard reflection themes.
- `analysis_reports/` — placeholder reports will be generated if Pylint, Bandit, and Flake8 are installed; see commands below.

## Run
```bash
python maintenance_system.py
```

## Generate tool reports
Install the tools and run from this directory:
```bash
python -m pip install pylint bandit flake8
pylint maintenance_system.py > analysis_reports/pylint_report.txt
bandit -r maintenance_system.py > analysis_reports/bandit_report.txt
flake8 maintenance_system.py > analysis_reports/flake8_report.txt
```

Review the reports and rerun the program with both valid and invalid inputs. The reports should be generated in the target environment; no tool output is claimed here because the tools were not available in the current environment.
