from datetime import datetime

import hashlib

def generate_registration_id(name, email):
    timestamp = str(int(datetime.utcnow().timestamp()))
    hash_input = f"{name} {email} {timestamp}"
    unique_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:6]
    return f"REG-{unique_hash.upper()}"

def set_generate_registration_id(self, registration_id):
    self.registration_id = registration_id