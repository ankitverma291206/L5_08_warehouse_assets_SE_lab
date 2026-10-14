"""Track warehouse assets and their scheduled maintenance."""

import json
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

SERVICE_INTERVAL_DAYS = 90
DATE_FORMAT = "%Y-%m-%d"
assets: dict[str, dict[str, str]] = {}


def register_asset(asset_id: str, machine_type: str) -> None:
    """Register an asset using today's date as its last service date."""
    if not asset_id.strip():
        raise ValueError("Asset ID must not be empty.")
    if asset_id in assets:
        raise ValueError(f"Asset {asset_id!r} is already registered.")
    assets[asset_id] = {
        "type": machine_type,
        "last_service": date.today().strftime(DATE_FORMAT),
    }
    print(f"Registered {asset_id} - total registered assets: {len(assets)}")


def update_service_date(asset_id: str, service_date: str) -> bool:
    """Update an asset's service date; return False for invalid input."""
    if asset_id not in assets:
        print(f"Could not update {asset_id!r}: asset is not registered.")
        return False
    try:
        parsed_date = datetime.strptime(service_date, DATE_FORMAT).date()
    except ValueError:
        print(f"Could not update {asset_id!r}: use YYYY-MM-DD for the date.")
        return False
    if parsed_date > date.today():
        print(f"Could not update {asset_id!r}: service date cannot be in the future.")
        return False
    assets[asset_id]["last_service"] = parsed_date.strftime(DATE_FORMAT)
    return True


def due_for_inspection(as_of: date | None = None) -> list[str]:
    """Return asset IDs whose last service was more than the interval ago."""
    reference_date = as_of or date.today()
    due_assets = []
    for asset_id, asset in assets.items():
        last_service = datetime.strptime(asset["last_service"], DATE_FORMAT).date()
        if reference_date - last_service > timedelta(days=SERVICE_INTERVAL_DAYS):
            due_assets.append(asset_id)
    return due_assets


def change_interval(days: int) -> None:
    """Set the service interval to a positive number of days."""
    global SERVICE_INTERVAL_DAYS
    if days <= 0:
        raise ValueError("Service interval must be a positive number of days.")
    SERVICE_INTERVAL_DAYS = days


def export_service_report(file: str | Path = "maintenance.json") -> None:
    """Write the current asset registry to a JSON report."""
    report_path = Path(file)
    with report_path.open("w", encoding="utf-8") as report_file:
        json.dump(assets, report_file, indent=2)
    print(f"Report written to {report_path}")


def write_scratch_copy() -> Path:
    """Create a uniquely named temporary JSON copy and return its path."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", prefix="maintenance-", encoding="utf-8", delete=False
    ) as scratch_file:
        json.dump(assets, scratch_file, indent=2)
        scratch_path = Path(scratch_file.name)
    print(f"Scratch copy at {scratch_path}")
    return scratch_path


def print_alerts() -> None:
    """Print an alert for each asset overdue for inspection."""
    for asset_id in due_for_inspection():
        print(f"ALERT: inspection overdue for {asset_id} ({assets[asset_id]['type']})")


def main() -> None:
    """Run a small demonstration of the maintenance registry."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("PJ-03", "Pallet Jack")
    register_asset("CR-02", "Crane")
    update_service_date("FL-01", "2025-01-15")
    change_interval(90)
    service_date = input("Last service date for CV-07 (YYYY-MM-DD, Enter to skip): ").strip()
    if service_date:
        update_service_date("CV-07", service_date)
    print_alerts()
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":
    main()
