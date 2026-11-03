"""Tests locaux de l'activation des dépôts avec subscription-manager simulé."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = """---
- name: Tester les tâches de dépôts avec une commande simulée
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    fpga_repos: []
    fpga_exclusive_repos: false
  environment:
    PATH: "{{ lookup('env', 'TEST_SUBSCRIPTION_BIN') }}:{{ lookup('env', 'PATH') }}"
    TEST_SUBSCRIPTION_STATE: "{{ lookup('env', 'TEST_SUBSCRIPTION_STATE') }}"
    TEST_SUBSCRIPTION_LOG: "{{ lookup('env', 'TEST_SUBSCRIPTION_LOG') }}"
  tasks:
    - name: Exécuter uniquement les tâches de gestion des dépôts
      ansible.builtin.import_tasks: "{{ lookup('env', 'TEST_REPOSITORY_TASKS') }}"
"""


@unittest.skipUnless(shutil.which("ansible-playbook"), "ansible-playbook est requis")
class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fpga-repos-test-")
        self.addCleanup(self.temp.cleanup)
        directory = Path(self.temp.name)
        self.state = directory / "state.json"
        self.log = directory / "calls.jsonl"
        self.playbook = directory / "test.yml"
        self.state.write_text(json.dumps({
            "available": ["lab-base", "lab-extra", "lab-extra-testing"],
            "enabled": ["lab-base", "lab-extra-testing"],
        }), encoding="utf-8")
        self.playbook.write_text(PLAYBOOK, encoding="utf-8")
        bin_dir = directory / "bin"
        bin_dir.mkdir()
        fake = bin_dir / "subscription-manager"
        shutil.copyfile(ROOT / "tests/mocks/subscription-manager", fake)
        fake.chmod(0o755)
        self.env = os.environ.copy()
        self.env.update({
            "TEST_SUBSCRIPTION_BIN": str(bin_dir),
            "TEST_SUBSCRIPTION_STATE": str(self.state),
            "TEST_SUBSCRIPTION_LOG": str(self.log),
            "TEST_REPOSITORY_TASKS": str(ROOT / "roles/role_fpga_workstation/tasks/00_repositories.yml"),
            "ANSIBLE_NOCOLOR": "1",
            "ANSIBLE_LOCAL_TEMP": str(directory / "ansible-tmp"),
            "ANSIBLE_RETRY_FILES_ENABLED": "false",
        })

    def run_play(self, repos, *, check=False, exclusive=False, expected=0):
        args = ["ansible-playbook", "-i", "localhost,", str(self.playbook), "-e", json.dumps({
            "ansible_python_interpreter": sys.executable,
            "fpga_repos": repos,
            "fpga_exclusive_repos": exclusive,
        })]
        if check:
            args.append("--check")
        result = subprocess.run(args, cwd=ROOT, env=self.env, capture_output=True,
                                text=True, timeout=60)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def enabled(self):
        return set(json.loads(self.state.read_text(encoding="utf-8"))["enabled"])

    def calls(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def test_check_n_active_rien(self):
        before = self.enabled()
        output = self.run_play(["lab-base", "lab-extra"], check=True)
        self.assertEqual(self.enabled(), before)
        self.assertIn("lab-extra", output)
        self.assertFalse(any("--enable=" in str(call) for call in self.calls()))

    def test_nom_exact_et_seconde_execution_idempotente(self):
        self.run_play(["lab-base", "lab-extra"])
        self.assertEqual(self.enabled(), {"lab-base", "lab-extra", "lab-extra-testing"})
        self.assertEqual(self.calls().count(["repos", "--enable=lab-extra"]), 1)
        output = self.run_play(["lab-base", "lab-extra"])
        self.assertEqual(self.calls().count(["repos", "--enable=lab-extra"]), 1)
        self.assertIn("changed=0", output)

    def test_depot_inconnu_arrete_avant_modification(self):
        before = self.enabled()
        output = self.run_play(["lab-extra", "lab-absent"], expected=2)
        self.assertIn("lab-absent", output)
        self.assertEqual(self.enabled(), before)
        self.assertFalse(any("--enable=" in str(call) for call in self.calls()))

    def test_liste_vide_interdite_en_mode_exclusif(self):
        self.run_play([], exclusive=True, expected=2)
        self.assertEqual(self.calls(), [])


if __name__ == "__main__":
    unittest.main()
