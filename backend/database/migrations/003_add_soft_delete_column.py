"""
Migration 003: Add is_deleted and deleted_at columns to prediction_logs table.
"""

import logging
import peewee
from playhouse.migrate import migrate, SqliteMigrator, PostgresqlMigrator

logger = logging.getLogger("backend.database.migrations.003")


def apply(database: peewee.Database) -> None:
    """Add is_deleted and deleted_at columns to prediction_logs table."""
    is_deleted_field = peewee.BooleanField(default=False, index=True)
    deleted_at_field = peewee.DateTimeField(null=True)

    if isinstance(database, peewee.SqliteDatabase):
        migrator = SqliteMigrator(database)
        try:
            migrate(
                migrator.add_column("prediction_logs", "is_deleted", is_deleted_field),
            )
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                logger.info("Column is_deleted already exists in prediction_logs.")
            else:
                raise

        try:
            migrate(
                migrator.add_column("prediction_logs", "deleted_at", deleted_at_field),
            )
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                logger.info("Column deleted_at already exists in prediction_logs.")
            else:
                raise

    elif isinstance(database, peewee.PostgresqlDatabase):
        migrator = PostgresqlMigrator(database)
        try:
            migrate(
                migrator.add_column("prediction_logs", "is_deleted", is_deleted_field),
            )
        except Exception as e:
            logger.info("Postgres add_column is_deleted handled: %s", e)

        try:
            migrate(
                migrator.add_column("prediction_logs", "deleted_at", deleted_at_field),
            )
        except Exception as e:
            logger.info("Postgres add_column deleted_at handled: %s", e)

    logger.info("migration_003_add_soft_delete_columns_applied")
