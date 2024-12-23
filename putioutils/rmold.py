"""Delete old files from Put.io account."""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from prettytable import PrettyTable
import putiopy
import humanize
import pytz
import click

DELETE_STATUS_SUCCESS = "OK"

@click.command()
@click.argument("days", type=int, required=True)
@click.option(
    "--dry-run", is_flag=True, help="Simulate deletion without actually deleting files."
)
def run(days: int, dry_run: bool = False):
    """Delete old files from Put.io account."""
    if dry_run:
        print("\nINFO: Dry run mode enabled. No files will be deleted.")

    load_dotenv()
    oauth_token: str = os.getenv("OAUTH_TOKEN", "")

    client = putiopy.Client(oauth_token)

    files = client.File.list(sort_by="DATE_ASC")

    table = PrettyTable()
    table.field_names = ["ID", "Name", "Size", "Created at", "To delete", "Deleted?"]

    for file in files:
        now = datetime.now(pytz.timezone("UTC"))
        created_at = file.created_at.replace(tzinfo=pytz.timezone("UTC"))  # type: ignore
        to_delete = now - created_at > timedelta(days=days)

        action = ""
        if to_delete:
            if dry_run:
                action = "dry run"
            else:
                result = client.File.delete(file)
                action = (
                    "DONE" if result["status"] == DELETE_STATUS_SUCCESS else "FAILED"
                )

        table.add_row(
            [
                file.id,
                file.name,
                humanize.naturalsize(file.size, binary=True),  # type: ignore
                humanize.naturaltime(now - created_at),
                "X" if to_delete else "",
                action,
            ]
        )

    print(table)


if __name__ == "__main__":
    run()  # pylint: disable=no-value-for-parameter
