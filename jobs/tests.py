import os
from pathlib import Path
from unittest.mock import patch

from django.test import SimpleTestCase

from placement_system import settings as settings_module


class DatabaseConfigTests(SimpleTestCase):
    def test_get_database_config_defaults_to_sqlite(self):
        config = settings_module.get_database_config(settings_module.BASE_DIR)

        self.assertEqual(config["ENGINE"], "django.db.backends.sqlite3")
        self.assertEqual(config["NAME"], str(settings_module.BASE_DIR / "db.sqlite3"))

    def test_get_database_config_uses_sql_settings_from_environment(self):
        with patch.dict(
            os.environ,
            {
                "DB_ENGINE": "django.db.backends.postgresql",
                "DB_NAME": "placement_db",
                "DB_USER": "placement_user",
                "DB_PASSWORD": "secret123",
                "DB_HOST": "db.example.com",
                "DB_PORT": "5432",
            },
            clear=False,
        ):
            config = settings_module.get_database_config(settings_module.BASE_DIR)

            self.assertEqual(config["ENGINE"], "django.db.backends.postgresql")
            self.assertEqual(config["NAME"], "placement_db")
            self.assertEqual(config["USER"], "placement_user")
            self.assertEqual(config["PASSWORD"], "secret123")
            self.assertEqual(config["HOST"], "db.example.com")
            self.assertEqual(config["PORT"], "5432")
