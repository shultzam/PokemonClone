import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install dependencies.
install('requests')
install('beautifulsoup4')