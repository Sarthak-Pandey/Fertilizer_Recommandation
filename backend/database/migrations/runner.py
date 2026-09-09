"""
Migration runner for Peewee ORM database schema evolution.
"""

import importlib.util
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import peewee

from backend.database.db import db as default_db

logger = logging.getLogger("backend.database.migrations.runner")


class SchemaMigration(peewee.Model):
    """Tracks applied schema migrations."""
    version = peewee.CharField(primary_key=True)
    applied_at = peewee.DateTimeField(default=lambda: datetime.now(timezone.utc))

    class Meta:
        database = default_db
        table_name = "schema_migrations"


def run_migrations(target_db: Optional[peewee.Database] = None) -> list[str]:
    """
    Discover and execute pending migrations sequentially against the target database.
    Returns list of newly applied migration versions.
    Raises RuntimeError on migration failure to prevent unsafe startup.
    """
    from backend.database.db import db as default_db

    database = target_db or default_db

    if database.is_closed():
        database.connect(reuse_if_open=True)

    SchemaMigration._meta.database = database
    database.create_tables([SchemaMigration], safe=True)

    migrations_dir = Path(__file__).parent
    migration_files = sorted(
        [
            f for f in migrations_dir.glob("*.py")
            if f.name[0].isdigit() and not f.name.startswith("__")
        ],
        key=lambda p: p.name,
    )

    applied_versions = {
        m.version for m in SchemaMigration.select(SchemaMigration.version)
    }

    newly_applied = []

    for filepath in migration_files:
        version = filepath.stem
        if version in applied_versions:
            continue

        logger.info("applying_migration version=%s", version)

        # Dynamic import of migration script
        spec = importlib.util.spec_from_file_location(
            f"backend.database.migrations.{version}", filepath
        )
        if spec is None or spec.loader is None:
            err_msg = f"Failed to load migration spec for {filepath.name}"
            logger.error(err_msg)
            raise RuntimeError(err_msg)

        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            if not hasattr(mod, "apply"):
                raise AttributeError(f"Migration {version} does not define an apply(db) function")

            with database.transaction():
                mod.apply(database)
                SchemaMigration.create(
                    version=version,
                    applied_at=datetime.now(timezone.utc),
                )
            newly_applied.append(version)
            logger.info("migration_success version=%s", version)
        except Exception as e:
            logger.error("migration_failed version=%s error=%s", version, str(e))
            raise RuntimeError(f"Database migration '{version}' failed: {e}") from e

    return newly_applied
