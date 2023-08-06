import os
import digikey
from pathlib import Path

CLIENT_ID = '293d958a-cc1d-44e6-9a84-742c8ca27b0e'  # Fill this in with your client ID
CLIENT_SECRET = 'sH5wR2pJ0yP7nP8tO7pR8vO3wW1mG3mD6xT2aJ8aV7jX6gW6bR'  # Fill this in with your client secret

os.environ['DIGIKEY_STORAGE_PATH'] = str(Path.cwd())
os.environ['DIGIKEY_CLIENT_ID'] = CLIENT_ID
os.environ['DIGIKEY_CLIENT_SECRET'] = CLIENT_SECRET

result = digikey.search('NE555')
print(result)

result = digikey.part('296-6501-1-ND')
print(result)

print(f'{result.standard_pricing[0].breakquantity}: {result.standard_pricing[0].unitprice}')

for pricebreak in result.standard_pricing:
    print(f'{pricebreak.breakquantity}: {pricebreak.unitprice}')