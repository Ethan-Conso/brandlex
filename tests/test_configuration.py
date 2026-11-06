"""Configuration parsing never executes or rewrites the secret file."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.configuration import load_environment, session_secret


class ConfigurationTests(unittest.TestCase):
    def test_env_quotes_comments_precedence_and_no_execution(self):
        source = ('# local settings\nexport DEEPSEEK_MODEL="local-model"\n'
                  "DEEPSEEK_API_KEY='literal#key'\nDEEPSEEK_BASE_URL=https://api.deepseek.com # comment\n"
                  'BRANDLEX_ADMIN_PASSWORD="literal$(whoami)`pwd`\\ntext"\n'
                  'HOME=/untrusted\nBAD LINE\nBRANDLEX_SECRET_KEY="unclosed\n')
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"DEEPSEEK_MODEL": "process-model"}, clear=True):
            path = Path(directory) / ".env"
            path.write_text(source)
            load_environment(path)
            self.assertEqual(os.environ["DEEPSEEK_MODEL"], "process-model")
            self.assertEqual(os.environ["DEEPSEEK_API_KEY"], "literal#key")
            self.assertEqual(os.environ["DEEPSEEK_BASE_URL"], "https://api.deepseek.com")
            self.assertEqual(os.environ["BRANDLEX_ADMIN_PASSWORD"], "literal$(whoami)`pwd`\ntext")
            self.assertNotIn("HOME", os.environ)
            self.assertNotIn("BRANDLEX_SECRET_KEY", os.environ)
            self.assertEqual(path.read_text(), source)

    def test_missing_file_is_not_created(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            load_environment(path)
            self.assertFalse(path.exists())

    def test_known_sample_or_short_session_key_is_not_used(self):
        for value in (None, "", "short", "brandlex-production-secret-key-2026"):
            key = session_secret(value)
            self.assertGreaterEqual(len(key), 64)
            self.assertNotEqual(key, value)
        secure = "sample-random-test-only-" + "a" * 40
        self.assertEqual(session_secret(secure), secure)


if __name__ == "__main__":
    unittest.main()
