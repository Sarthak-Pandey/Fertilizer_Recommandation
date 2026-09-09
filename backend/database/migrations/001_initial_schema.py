"""
Migration 001: Initial schema setup for prediction_logs.
"""

import logging
import peewee

logger = logging.getLogger("backend.database.migrations.001")


def apply(database: peewee.Database) -> None:
    """Apply migration to ensure prediction_logs table exists."""
    class PredictionLogSchema(peewee.Model):
        prediction_id = peewee.CharField(primary_key=True)
        request_id = peewee.CharField(null=True, index=True)
        input_features = peewee.TextField()
        predicted_fertilizer = peewee.CharField()
        gate_decision = peewee.CharField(null=True, default="N/A")
        specialist_used = peewee.CharField(null=True)
        confidence = peewee.FloatField(null=True)
        model_version = peewee.CharField(index=True)
        preprocessing_version = peewee.CharField()
        feature_schema_version = peewee.CharField()
        latency_ms = peewee.FloatField(null=True)
        status = peewee.CharField(default="success")
        error_message = peewee.TextField(null=True)
        created_at = peewee.DateTimeField()

        class Meta:
            table_name = "prediction_logs"

    PredictionLogSchema._meta.database = database
    database.create_tables([PredictionLogSchema], safe=True)
    logger.info("migration_001_initial_schema_applied")
