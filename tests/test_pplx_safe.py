"""Offline wrapper tests: mock uv and the client; never send a search or credentials."""
import importlib.machinery
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/deep-search/scripts/pplx-safe'


class WrapperTests(unittest.TestCase):
    def setUp(self):
        loader = importlib.machinery.SourceFileLoader('pplx_safe_test', str(SCRIPT))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        self.module = importlib.util.module_from_spec(spec)
        loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.module.REAL_HOME = self.root
        self.module.CONFIG = self.root / '.config/perplexity-web'
        self.module.SCRIPT = self.root / 'client.py'
        self.module.SCRIPT.write_text('# never executed\n')

    def call(self, args):
        from io import StringIO
        output = StringIO()
        with patch.object(self.module.sys, 'stderr', output):
            result = self.module.main(['pplx-safe', *args])
        return result, output.getvalue()

    def test_invalid_mode_does_not_run_anything(self):
        for args in (['search', 'q', '--mode'], ['search', 'q', '--mode', '--json'], ['search', 'q', '--mode='], ['search', 'q', '--mode', 'research', '--mode', 'research']):
            with self.subTest(args=args), patch.object(self.module.subprocess, 'run') as run:
                result, error = self.call(args)
                self.assertEqual(result, 2)
                self.assertEqual(json.loads(error)['error'], 'INVALID_ARGUMENT')
                run.assert_not_called()

    def test_missing_client_errors_are_valid_json(self):
        self.module.SCRIPT = self.root / 'missing"client.py'
        result, error = self.call(['search', 'q'])
        self.assertEqual(result, 1)
        self.assertEqual(json.loads(error)['error'], 'NO_PPLX_WEB')

    def test_missing_uv_is_reported_without_traceback(self):
        with patch.object(self.module.shutil, 'which', return_value=None):
            result, error = self.call(['search', 'q'])
        self.assertEqual(result, 1)
        self.assertEqual(json.loads(error)['error'], 'NO_UV')

    def test_private_home_cleanup_and_parent_config_unchanged(self):
        self.module.CONFIG.mkdir(parents=True)
        original = self.module.CONFIG / 'cookies.json'
        original.write_text('{"synthetic": true}')
        os.chmod(original, 0o644)
        homes = []

        def fake_run(cmd, env):
            home = Path(env['HOME'])
            homes.append(home)
            self.assertNotEqual(home, self.root)
            copy = home / '.config/perplexity-web/cookies.json'
            self.assertEqual(copy.read_text(), original.read_text())
            self.assertEqual(copy.stat().st_mode & 0o777, 0o600)
            self.assertEqual(home.stat().st_mode & 0o777, 0o700)
            self.assertEqual(cmd[-2:], ['search', 'query with spaces'])
            copy.write_text('changed only in temporary home')
            return SimpleNamespace(returncode=7)

        with patch.object(self.module.shutil, 'which', return_value='/mock/uv'), patch.object(self.module.subprocess, 'run', side_effect=fake_run):
            result, error = self.call(['search', 'query with spaces'])
        self.assertEqual((result, error), (7, ''))
        self.assertTrue(all(not home.exists() for home in homes))
        self.assertEqual(original.read_text(), '{"synthetic": true}')
        self.assertEqual(original.stat().st_mode & 0o777, 0o644)

    def test_mode_equals_and_passthrough_boundary(self):
        with patch.object(self.module.shutil, 'which', return_value='/mock/uv'), patch.object(self.module.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as run:
            result, error = self.call(['search', 'q', '--mode=research', '--json'])
            self.assertEqual((result, error), (0, ''))
            self.assertEqual(run.call_args.args[0][-4:], ['research', 'search', 'q', '--json'])
            result, error = self.call(['search', '--', '--mode'])
            self.assertEqual((result, error), (0, ''))
            self.assertEqual(run.call_args.args[0][-3:], ['search', '--', '--mode'])

    def test_process_launch_failure_is_reported(self):
        with patch.object(self.module.shutil, 'which', return_value='/mock/uv'), patch.object(self.module.subprocess, 'run', side_effect=OSError('cannot launch')):
            result, error = self.call(['search', 'q'])
        self.assertEqual(result, 1)
        self.assertEqual(json.loads(error)['error'], 'RUN_FAILED')


if __name__ == '__main__':
    unittest.main()
