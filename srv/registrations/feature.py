from datetime import datetime

import hashlib

def generate_registration_id(name, email):
    timestamp = str(int(datetime.utcnow().timestamp()))
    hash_input = f"{name} {email} {timestamp}"
    unique_hash = hashlib.md5(hash_input.encode()).hexdigest()[:6]
    registration_id = f"REG-{unique_hash.upper()}"
    return registration_id

def set_generate_registration_id(self, registration_id):
    self.registration_id = registration_id