from django.test import TestCase

from parser.backend import LogDb
from parser.models import Log


class ParserTestCase(TestCase):

    def test_save_db_new_logs(self):
        LogDb().save_db_new_logs()
        logs = Log.objects.all()
        self.assertEqual(len(logs), 100)
