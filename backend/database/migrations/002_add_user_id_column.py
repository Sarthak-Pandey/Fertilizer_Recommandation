"""
Migration 002: Add user_id column to prediction_logs table.
"""

import logging
import peewee
from playhouse.migrate import migrate, SqliteMigrator, PostgresqlMigrator

logger = logging.getLogger("backend.database.migrations.002")


def apply(database: peewee.Database) -> None:
    """Add user_id column to prediction_logs table."""
    user_id_field = peewee.CharField(null=True, index=True)

    if isinstance(database, peewee.SqliteDatabase):
        migrator = SqliteMigrator(database)
        try:
            migrate(
                migrator.add_column("prediction_logs", "user_id", user_id_field),
            )
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                logger.info("Column user_id already exists in prediction_logs.")
            else:
                raise
    elif isinstance(database, peewee.PostgresqlDatabase):
        migrator = PostgresqlMigrator(database)
        try:
            migrate(
                migrator.add_column("prediction_logs", "user_id", user_id_field),
            )
        except Exception as e:
            logger.info("Postgres add_column user_id handled: %s", e)

    logger.info("migration_002_add_user_id_column_applied")
