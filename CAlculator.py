import subprocess, sys, os, time, getpass, warnings
from getpass import GetPassWarning

warnings.filterwarnings("ignore", category=GetPassWarning)


# ── Auto-install (was 3 identical try/import blocks) ─────────────────────────
def _install(package):
    proc = subprocess.Popen(
        [sys.executable, "-m", "pip", "install", package],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    for line in proc.stdout:
        print(line, end='')

def _ensure(import_name, pip_name=None):
    try:
        return __import__(import_name)
    except ImportError:
        print("Downloading Resources...")
        _install(pip_name or import_name)
        return __import__(import_name)

pyAesCrypt = _ensure('pyAesCrypt')
pygame     = _ensure('pygame')
Document   = _ensure('docx', 'python-docx').Document


# ── SecureVault (was scattered decrypt/encrypt/hide/remove across 3 functions) ─
class SecureVault:
    VAULT  = "Crypted_file.aes"
    TEMP   = "temp.docx"
    BUFFER = 64 * 1024

    def __init__(self):
        self.password = None

    @property
    def exists(self):
        return os.path.exists(self.VAULT)

    # private helpers
    def _safe_remove(self, path):
        """Delete a file safely, raising on PermissionError."""
        if os.path.exists(path):
            try:
                os.remove(path)
            except PermissionError:
                print("File is locked. Close any other apps using it.")
                raise

    def _decrypt(self, dest=None):
        dest = dest or self.TEMP
        pyAesCrypt.decryptFile(self.VAULT, dest, self.password, self.BUFFER)
        return dest

    def _encrypt(self, src):
        """Encrypt src → vault, hide vault, delete src."""
        self._safe_remove(self.VAULT)
        pyAesCrypt.encryptFile(src, self.VAULT, self.password, self.BUFFER)
        os.remove(src)
        os.system(f"attrib +h {self.VAULT}")

    # public API
    def authenticate(self, pw):
        """Return True if pw unlocks the vault."""
        try:
            pyAesCrypt.decryptFile(self.VAULT, self.TEMP, pw, self.BUFFER)
            self.password = pw
            self._safe_remove(self.TEMP)
            return True
        except Exception:
            return False

    def create(self, pw, lines):
        """Create a new vault from a list of text lines."""
        self.password = pw
        doc = Document()
        for line in lines:
            doc.add_paragraph(line)
        doc.save(self.TEMP)
        self._encrypt(self.TEMP)

    def append(self, lines):
        """Add new lines to the existing vault."""
        self._decrypt()
        doc = Document(self.TEMP)
        for line in lines:
            doc.add_paragraph(line)
        doc.save(self.TEMP)
        doc = None
        time.sleep(0.1)
        self._encrypt(self.TEMP)

    def read(self):
        """Return all paragraph texts from vault."""
        self._decrypt()
        paragraphs = [p.text for p in Document(self.TEMP).paragraphs]
        self._safe_remove(self.TEMP)
        return paragraphs

    def export(self, dest="your_data.docx"):
        """Export vault as a readable docx, then re-encrypt."""
        self._decrypt(dest)
        time.sleep(0.1)
        self._encrypt(dest)
        return dest

    def delete(self):
        self._safe_remove(self.VAULT)


# ── MusicPlayer ───────────────────────────────────────────────────────────────
class MusicPlayer:
    TRACK = r"C:\Users\LRP\Downloads\where_winds_meets.mp3"

    def __init__(self):
        self._started = False

    def start(self):
        if self._started:
            return
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.TRACK)
            pygame.mixer.music.play(-1)
            self._started = True
        except Exception:
            print("Music file not found.")

    def pause(self):
        if self._started:
            pygame.mixer.music.pause()

    def resume(self):
        if self._started:
            pygame.mixer.music.unpause()

    def stop(self):
        if self._started:
            pygame.mixer.music.stop()
            pygame.quit()


# ── Shared helper (was duplicated in new_password + write_data) ───────────────
def _collect_lines(prompt="Write. Type 'save' to finish."):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip().lower() == 'save':
            break
        lines.append(line)
    return lines


# ── App state ─────────────────────────────────────────────────────────────────
vault = SecureVault()
music = MusicPlayer()
state = ['first']
a = b = operator_input = None


# ── State handlers ────────────────────────────────────────────────────────────
def first():
    global a
    val = input("Enter first number: ").strip().lower()
    if val == '#':
        state[0] = 'enter_password' if vault.exists else 'new_password'
        return
    try:
        a = float(val)
        state[0] = 'op'
    except ValueError:
        print("Please enter a numerical value!")

def op():
    global operator_input
    val = input("Enter operator: ").strip()
    if val in ('+', '-', '*', '/'):
        operator_input = val
        state[0] = 'second'
    else:
        print("Enter valid operator (+, -, *, /)!")

def second():
    global b
    val = input("Enter second number: ").strip()
    try:
        b = float(val)
        state[0] = 'result'
    except ValueError:
        print("Please enter a numerical value!")

def result():
    if operator_input == '/' and b == 0:
        print("Division by zero ... Not allowed! ABORTING !!!")
        state[0] = 'first'
        return
    res = {'+': a + b, '-': a - b, '*': a * b, '/': a / b}[operator_input]
    print("Result:", res)
    state[0] = 'choice'

def choice():
    val = input("Continue? [Y/n]: ").strip().lower()
    if val == 'n':
        state[0] = 'exit'
    elif val in ('y', ''):
        state[0] = 'first'
    # else: stay in choice, ask again

def new_password():
    p1 = input("Enter new password: ").strip()
    if len(p1) < 4:
        print("Password must be at least 4 characters long!")
        state[0] = 'first'
        return
    p2 = input("Confirm password: ").strip()
    if p1 != p2:
        print("Passwords don't match!")
        state[0] = 'first'
        return
    lines = _collect_lines("Give input. Type 'save' when done.")
    vault.create(p1, lines)
    print("Encrypted and saved.")
    state[0] = 'menu'

def enter_password():
    pw = getpass.getpass("Enter password: ")
    if vault.authenticate(pw):
        state[0] = 'menu'
    else:
        print("Wrong password or corrupt file.")
        state[0] = 'first'

def menu():
    music.start()
    print("1. Write More\n2. Read Content\n3. Settings")
    ch = input("Choice [1/2/3]: ").strip()
    if   ch == '1': write_data()
    elif ch == '2': read_data()
    elif ch == '3': settings()
    else:
        print("!")
        state[0] = 'first'

def write_data():
    lines = _collect_lines("Write data. Type 'save' to finish.")
    try:
        vault.append(lines)
        print("Appended and saved.")
    except Exception as e:
        print("Error:", e)
    finally:
        state[0] = 'first'

def read_data():
    for line in vault.read():
        print(line)
    state[0] = 'first'

def settings():
    print("1. Music\n2. Export Data\n3. Delete Everything\n4. About")
    ch = input("Choice [1/2/3/4]: ").strip()
    if ch == '1':
        on_off = input("1. On\n2. Off\n[1 or 2]: ").strip()
        if on_off == '1': music.resume()
        elif on_off == '2': music.pause()
    elif ch == '2':
        if getpass.getpass("Password: ") == vault.password:
            try:
                out = vault.export()
                print(f"Exported as '{out}'. Delete manually after reading.")
            except Exception as e:
                print("Error during export:", e)
        else:
            print("Incorrect password.")
    elif ch == '3':
        if getpass.getpass("Confirm delete password: ") == vault.password:
            vault.delete()
            print("Data deleted.")
            music.pause()
            state[0] = 'first'
            return
    elif ch == '4':
        print(
            "CAlculator is a Python program to save data privately and securely.\n"
            "Additional Features:\n"
            "  - User password cannot be hacked unless leaked by the user.\n"
            "  - Bugs fixed; no chance of error flow."
        )
        state[0] = 'menu'
        return
    else:
        print("!")
    state[0] = 'first'


# ── Main loop (dict dispatch replaces match/case) ─────────────────────────────
STATES = {
    'first':          first,
    'op':             op,
    'second':         second,
    'result':         result,
    'choice':         choice,
    'new_password':   new_password,
    'enter_password': enter_password,
    'menu':           menu,
}

print("Welcome to Calculator v1.03")
print("Enter # to start")

while True:
    if state[0] == 'exit':
        print("Thanks for visit")
        music.stop()
        break
    STATES[state[0]]()

time.sleep(0.49)
print("\n" * 3)
print("CAlculator v1.03")
print("Project by: Nikhil Nehra")
