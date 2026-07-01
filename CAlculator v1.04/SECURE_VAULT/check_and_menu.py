


import subprocess, sys


class check_installations:
    def __init__(self):
        self.pyAesCrypt = self._ensure('pyAesCrypt')
        self.pygame     = self._ensure('pygame')
        self.Document   = self._ensure('docx', 'python-docx').Document

    def _install(self, package):
        proc = subprocess.Popen(
            [sys.executable, "-m", "pip", "install", package],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        for line in proc.stdout:
            print(line, end='')

    def _ensure(self, import_name, pip_name=None):
        try:
            return __import__(import_name)
        except ImportError:
            print("Downloading Resources...")
            self._install(pip_name or import_name)
            return __import__(import_name)

installer = check_installations()

