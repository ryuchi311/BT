import os
from telethon.sync import TelegramClient

# Try to load .env automatically if python-dotenv is available
try:
    from dotenv import load_dotenv
    # load .env from repository root (one level up from scripts/)
    project_root = os.path.dirname(os.path.dirname(__file__))
    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
except Exception:
    pass

# Read API_ID and API_HASH from env
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')

if not api_id or not api_hash:
    # Diagnostic prints to help users understand what's loaded
    project_root = os.path.dirname(os.path.dirname(__file__))
    dotenv_path = os.path.join(project_root, '.env')
    print('DEBUG: looked for .env at', dotenv_path, '- exists=', os.path.exists(dotenv_path))
    print('ERROR: API_ID and API_HASH must be set in the environment (.env) or environment variables.')
    print('If you have them in a .env file, this script attempted to load it automatically.')
    print('Note: `setx` writes permanent vars but does NOT affect the current PowerShell session until you open a new shell.')
    print('To set them for this session only (immediately), run in PowerShell:')
    print('  $env:API_ID = "<your_api_id>"')
    print('  $env:API_HASH = "<your_api_hash>"')
    print('Or permanently with setx (then restart your shell):')
    print('  setx API_ID "<your_api_id>"')
    print('  setx API_HASH "<your_api_hash>"')
    raise SystemExit(1)

# Print masked values for confirmation
def mask(val):
    if not val:
        return None
    if len(val) <= 6:
        return val[0] + '***'
    return val[:3] + '...' + val[-3:]

print('Loaded API_ID=', mask(api_id))
print('Loaded API_HASH=', mask(api_hash))

# session file location under instance/ so it won't be checked into repo
instance_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
os.makedirs(instance_dir, exist_ok=True)
session_path = os.path.join(instance_dir, 'telethon_session')

print('Using session file:', session_path)
print('Starting Telethon client. You will be prompted for phone and login code on first run.')

client = TelegramClient(session_path, int(api_id), api_hash)
client.start()
print('Sign-in complete. Session saved at', session_path)
client.disconnect()
