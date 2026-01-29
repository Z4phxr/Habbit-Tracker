#!/usr/bin/env python3
"""
Generate a secure Django SECRET_KEY
Usage: python generate_secret_key.py
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure random secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key

if __name__ == '__main__':
    secret_key = generate_secret_key()
    print("\n" + "="*60)
    print("Generated Django SECRET_KEY:")
    print("="*60)
    print(secret_key)
    print("="*60)
    print("\nAdd this to your .env file:")
    print(f"DJANGO_SECRET_KEY={secret_key}")
    print("="*60 + "\n")
