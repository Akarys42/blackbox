import datetime
from pathlib import Path

from blackbox.handlers.databases._base import BlackboxDatabase
from blackbox.utils import run_command
from blackbox.utils.logger import log


class Postgres(BlackboxDatabase):
    """A Database handler that will do a pg_dumpall for Postgres, backing up all tables."""

    required_fields = ("username", "password", "host", "port")

    def backup(self) -> Path:
        """Dump all the data to a file and then return the filepath."""
        date = datetime.date.today().strftime("%d_%m_%Y")
        backup_path = Path.home() / f"postgres_blackbox_{date}.sql"

        # Run the backup, and store the outcome.
        self.success, self.output = run_command(
            f"pg_dumpall --file={backup_path}",
            PGUSER=self.config["user"],
            PGPASSWORD=self.config["password"],
            PGHOST=self.config["host"],
            PGPORT=self.config["port"],
        )
        log.debug(self.output)

        # Return the path to the backup file
        return backup_path
