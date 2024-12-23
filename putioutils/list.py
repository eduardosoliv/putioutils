"""List files from Put.io account in a formatted table with size and creation time."""

import os
from datetime import datetime
from dotenv import load_dotenv
from prettytable import PrettyTable
import putiopy
import humanize
import pytz


def run():
    """Fetch and display Put.io files in a formatted table with file sizes and creation times."""
    load_dotenv()
    oauth_token = os.getenv("OAUTH_TOKEN")

    client = putiopy.Client(oauth_token)

    # list files
    files = client.File.list(sort_by="DATE_DESC")

    table = PrettyTable()
    table.field_names = ["Name", "Size", "Created at"]

    for file in files:
        size_unit = "MB"
        size = file.size / 1024 / 1024
        if size > 1024:
            size = size / 1024
            size_unit = "GB"

        now = datetime.now(pytz.timezone("UTC"))
        created_at = file.created_at.replace(tzinfo=pytz.timezone("UTC"))

        table.add_row(
            [
                file.name,
                f"{size:.1f} {size_unit}",
                humanize.naturaltime(now - created_at),
            ]
        )

    print(table)
