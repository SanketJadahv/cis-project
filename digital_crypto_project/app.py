"""
Classical Ciphers and Symmetric Key Cryptography
Interactive Encryption and Decryption System
Author: Sanket Jadhav
Backend: Flask Application (Single-File Architecture)
"""

import os
import base64
import random
import secrets
from flask import Flask, render_template, request, jsonify
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)


# ==========================================
# 1. CLASSICAL CIPHERS IMPLEMENTATION
# ==========================================

def caesar_cipher(text: str, shift: int, mode: str = 'encrypt') -> str:
    """
    Caesar Cipher: Shifts alphabetic characters by a fixed integer key.
    Preserves case and leaves numbers, spaces, and punctuation untouched.
    """
    if mode == 'decrypt':
        shift = -shift
    shift = shift % 26

    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        elif ch.islower():
            result.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        else:
            result.append(ch)
    return "".join(result)


def substitution_cipher(text: str, key: str, mode: str = 'encrypt') -> str:
    """
    Monoalphabetic Substitution Cipher:
    Replaces each of the 26 English letters with a mapped character from a custom 26-letter alphabet.
    """
    key = key.strip().upper()
    if len(key) != 26 or len(set(key)) != 26 or not key.isalpha():
        raise ValueError("Substitution key must contain all 26 distinct English letters (A-Z) without duplicates.")

    std_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    std_lower = "abcdefghijklmnopqrstuvwxyz"
    key_upper = key
    key_lower = key.lower()

    if mode == 'encrypt':
        in_chars = std_upper + std_lower
        out_chars = key_upper + key_lower
    else:
        in_chars = key_upper + key_lower
        out_chars = std_upper + std_lower

    table = str.maketrans(in_chars, out_chars)
    return text.translate(table)


def vigenere_cipher(text: str, key: str, mode: str = 'encrypt') -> str:
    """
    Vigenère Cipher: Polyalphabetic substitution using a keyword.
    Each letter is shifted according to the corresponding letter in the repeated key.
    """
    clean_key = [c.upper() for c in key if c.isalpha()]
    if not clean_key:
        raise ValueError("Vigenère keyword must contain at least one alphabetic letter (A-Z).")

    key_len = len(clean_key)
    result = []
    key_idx = 0

    for ch in text:
        if ch.isalpha():
            shift = ord(clean_key[key_idx % key_len]) - 65
            if mode == 'decrypt':
                shift = -shift
            if ch.isupper():
                result.append(chr((ord(ch) - 65 + shift) % 26 + 65))
            else:
                result.append(chr((ord(ch) - 97 + shift) % 26 + 97))
            key_idx += 1
        else:
            result.append(ch)
    return "".join(result)


def rail_fence_cipher(text: str, rails: int, mode: str = 'encrypt') -> str:
    """
    Rail Fence Cipher: Transposition cipher writing message in a zigzag pattern across N rails.
    Preserves all characters, symbols, and spaces.
    """
    if rails < 2:
        raise ValueError("Rail Fence key (number of rails) must be an integer >= 2.")
    if len(text) <= 1 or rails >= len(text):
        return text

    if mode == 'encrypt':
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1  # 1: moving down, -1: moving up
        for char in text:
            fence[rail].append(char)
            rail += direction
            if rail == rails - 1:
                direction = -1
            elif rail == 0:
                direction = 1
        return "".join("".join(row) for row in fence)
    else:
        # Decryption: reconstruct the zigzag matrix path
        pattern = []
        rail = 0
        direction = 1
        for _ in range(len(text)):
            pattern.append(rail)
            rail += direction
            if rail == rails - 1:
                direction = -1
            elif rail == 0:
                direction = 1

        counts = [pattern.count(r) for r in range(rails)]
        rail_slices = {}
        curr = 0
        for r in range(rails):
            rail_slices[r] = list(text[curr:curr + counts[r]])
            curr += counts[r]

        result = []
        for r in pattern:
            result.append(rail_slices[r].pop(0))
        return "".join(result)


# ==========================================
# 2. SYMMETRIC-KEY CRYPTOGRAPHY (AES-256-GCM)
# ==========================================

def aes_gcm_encrypt(plaintext: str, key_hex: str) -> dict:
    """
    AES-256-GCM Authenticated Encryption:
    - 256-bit key (32 bytes from 64 hex characters)
    - 96-bit cryptographically secure random Nonce (12 bytes) generated freshly every time
    - 128-bit Authentication Tag (16 bytes) providing cryptographic integrity
    - Nonce is NEVER reused
    Returns combined Base64 ciphertext containing [12-byte Nonce + Ciphertext + 16-byte Tag]
    """
    try:
        key_bytes = bytes.fromhex(key_hex.strip())
    except (ValueError, TypeError):
        raise ValueError("AES-256 key must be a valid 64-character hexadecimal string.")

    if len(key_bytes) != 32:
        raise ValueError(f"AES-256 key must be exactly 32 bytes (64 hex characters). Received: {len(key_bytes)} bytes.")

    # Fresh 12-byte nonce generated for every single encryption call
    nonce = os.urandom(12)
    aesgcm = AESGCM(key_bytes)

    # In Python cryptography, encrypt() appends the 16-byte authentication tag
    ciphertext_and_tag = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)

    combined = nonce + ciphertext_and_tag
    combined_b64 = base64.b64encode(combined).decode('utf-8')
    tag = ciphertext_and_tag[-16:]
    raw_ciphertext = ciphertext_and_tag[:-16]

    return {
        "ciphertext": combined_b64,
        "nonce_hex": nonce.hex(),
        "tag_hex": tag.hex(),
        "raw_ciphertext_hex": raw_ciphertext.hex()
    }


def aes_gcm_decrypt(combined_ciphertext: str, key_hex: str) -> str:
    """
    AES-256-GCM Decryption & Integrity Verification:
    - Parses 12-byte Nonce, ciphertext payload, and 16-byte Auth Tag.
    - Rejects modified/tampered ciphertext or incorrect key via cryptographic tag verification.
    """
    try:
        key_bytes = bytes.fromhex(key_hex.strip())
    except (ValueError, TypeError):
        raise ValueError("AES-256 key must be a valid 64-character hexadecimal string.")

    if len(key_bytes) != 32:
        raise ValueError(f"AES-256 key must be exactly 32 bytes (64 hex characters). Received: {len(key_bytes)} bytes.")

    combined_str = combined_ciphertext.strip()
    data = None

    # Support Base64 or Hex encoded ciphertext packets
    try:
        data = base64.b64decode(combined_str, validate=True)
    except Exception:
        try:
            data = bytes.fromhex(combined_str)
        except Exception:
            raise ValueError("Invalid ciphertext format: Ciphertext must be valid Base64 or Hexadecimal encoding.")

    if len(data) < 28:
        raise ValueError("Ciphertext data too short: Must include at least 12-byte Nonce and 16-byte Auth Tag.")

    nonce = data[:12]
    ciphertext_and_tag = data[12:]

    aesgcm = AESGCM(key_bytes)
    try:
        plaintext_bytes = aesgcm.decrypt(nonce, ciphertext_and_tag, None)
    except InvalidTag:
        raise ValueError("Decryption Rejected: Authentication tag mismatch! Either the key is incorrect or the ciphertext was modified/tampered with.")

    return plaintext_bytes.decode('utf-8', errors='replace')


# ==========================================
# 3. ALGORITHM COMPARISON & EDUCATIONAL DATA
# ==========================================

CIPHERS_DATA = {
    "caesar": {
        "name": "Caesar Cipher",
        "category": "Classical (Monoalphabetic Substitution)",
        "key_type": "Integer Shift (0-25)",
        "purpose": "Historic military messaging (Julius Caesar, ~100 BC)",
        "limitations": "Extremely small key space (only 25 possible shifts); easily cracked in milliseconds via brute force or letter frequency analysis.",
        "modern_secure": False,
        "description": "Substitutes each alphabet letter with one shifted by N positions down the alphabet.",
        "default_key": "3"
    },
    "substitution": {
        "name": "Monoalphabetic Substitution",
        "category": "Classical (Simple Substitution)",
        "key_type": "26-Letter Permutation Alphabet",
        "purpose": "Private correspondence in historical diplomacy",
        "limitations": "Preserves natural language letter frequency (e.g., 'E' is the most frequent English letter); easily broken using frequency analysis.",
        "modern_secure": False,
        "description": "Each letter in the standard alphabet is mapped to a unique letter from a custom 26-character alphabet permutation.",
        "default_key": "QWERTYUIOPASDFGHJKLZXCVBNM"
    },
    "vigenere": {
        "name": "Vigenère Cipher",
        "category": "Classical (Polyalphabetic Substitution)",
        "key_type": "Keyword (Alphabetic string)",
        "purpose": "16th-19th century diplomatic encryption ('le chiffre indéchiffrable')",
        "limitations": "Vulnerable to Kasiski examination, Friedman test, and index of coincidence to deduce key length and solve as multiple Caesar ciphers.",
        "modern_secure": False,
        "description": "Uses a repeating keyword to shift letters by different amounts, flattening simple single-letter frequency spikes.",
        "default_key": "CYBERSECURITY"
    },
    "rail_fence": {
        "name": "Rail Fence Cipher",
        "category": "Classical (Transposition Cipher)",
        "key_type": "Number of Rails (Integer >= 2)",
        "purpose": "Civil War tactical communications & telegraphy",
        "limitations": "Rearranges letters without changing them; preserves exact letter frequencies and has very few rail depths, making anagramming easy.",
        "modern_secure": False,
        "description": "Writes the message letters diagonally in a zigzag pattern across multiple rails, then reads them off row by row.",
        "default_key": "3"
    },
    "aes_gcm": {
        "name": "AES-256-GCM",
        "category": "Modern Symmetric Authenticated Encryption (AEAD)",
        "key_type": "256-bit Cryptographic Key (64 Hex chars)",
        "purpose": "Global standard for securing confidential data in TLS 1.3, VPNs, banking, cloud storage, and disk encryption",
        "limitations": "Symmetric key must be securely exchanged beforehand; critical that the 96-bit Nonce is NEVER reused with the same key.",
        "modern_secure": True,
        "description": "Industry-grade Galois/Counter Mode providing high-speed authenticated encryption with mathematical confidentiality, integrity, and authenticity verification.",
        "default_key": ""
    }
}


# ==========================================
# 4. FLASK ROUTES
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/ciphers-info', methods=['GET'])
def get_ciphers_info():
    return jsonify({"success": True, "ciphers": CIPHERS_DATA})


@app.route('/api/generate-key', methods=['GET'])
def generate_key():
    cipher = request.args.get('cipher', '').strip().lower()

    if cipher == 'caesar':
        key = str(random.randint(1, 25))
    elif cipher == 'substitution':
        letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        random.shuffle(letters)
        key = "".join(letters)
    elif cipher == 'vigenere':
        words = ["CIPHER", "SHIELD", "QUANTUM", "SENTINEL", "DEFENSE", "FIREWALL", "ENIGMA", "KEYWORD"]
        key = random.choice(words)
    elif cipher == 'rail_fence':
        key = str(random.randint(3, 6))
    elif cipher == 'aes_gcm':
        # 32 random cryptographically secure bytes = 256 bits = 64 hex characters
        key = secrets.token_hex(32)
    else:
        return jsonify({"success": False, "error": "Unknown cipher specified."}), 400

    return jsonify({"success": True, "cipher": cipher, "key": key})


@app.route('/api/encrypt', methods=['POST'])
def handle_encrypt():
    data = request.get_json(silent=True) or {}
    cipher = data.get('cipher', '').strip().lower()
    text = data.get('text', '')
    key = data.get('key', '')

    if not text:
        return jsonify({"success": False, "error": "Input message cannot be empty."}), 400

    try:
        if cipher == 'caesar':
            try:
                shift = int(key)
            except ValueError:
                return jsonify({"success": False, "error": "Caesar Cipher requires an integer shift key (e.g., 3)."}), 400
            result = caesar_cipher(text, shift, 'encrypt')
            return jsonify({"success": True, "result": result})

        elif cipher == 'substitution':
            result = substitution_cipher(text, key, 'encrypt')
            return jsonify({"success": True, "result": result})

        elif cipher == 'vigenere':
            result = vigenere_cipher(text, key, 'encrypt')
            return jsonify({"success": True, "result": result})

        elif cipher == 'rail_fence':
            try:
                rails = int(key)
            except ValueError:
                return jsonify({"success": False, "error": "Rail Fence Cipher requires an integer rail count >= 2."}), 400
            result = rail_fence_cipher(text, rails, 'encrypt')
            return jsonify({"success": True, "result": result})

        elif cipher == 'aes_gcm':
            if not key:
                return jsonify({"success": False, "error": "AES-256 requires a 64-character hexadecimal key. Click 'Generate Secure Key' to create one."}), 400
            res = aes_gcm_encrypt(text, key)
            return jsonify({
                "success": True,
                "result": res["ciphertext"],
                "metadata": {
                    "nonce_hex": res["nonce_hex"],
                    "tag_hex": res["tag_hex"],
                    "raw_ciphertext_hex": res["raw_ciphertext_hex"],
                    "algorithm": "AES-256-GCM (NIST SP 800-38D)",
                    "note": "Fresh 96-bit random nonce used. The 16-byte authentication tag guarantees tamper detection."
                }
            })

        else:
            return jsonify({"success": False, "error": f"Unsupported cipher algorithm: '{cipher}'"}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/decrypt', methods=['POST'])
def handle_decrypt():
    data = request.get_json(silent=True) or {}
    cipher = data.get('cipher', '').strip().lower()
    text = data.get('text', '')
    key = data.get('key', '')

    if not text:
        return jsonify({"success": False, "error": "Ciphertext input cannot be empty."}), 400

    try:
        if cipher == 'caesar':
            try:
                shift = int(key)
            except ValueError:
                return jsonify({"success": False, "error": "Caesar Cipher requires an integer shift key (e.g., 3)."}), 400
            result = caesar_cipher(text, shift, 'decrypt')
            return jsonify({"success": True, "result": result})

        elif cipher == 'substitution':
            result = substitution_cipher(text, key, 'decrypt')
            return jsonify({"success": True, "result": result})

        elif cipher == 'vigenere':
            result = vigenere_cipher(text, key, 'decrypt')
            return jsonify({"success": True, "result": result})

        elif cipher == 'rail_fence':
            try:
                rails = int(key)
            except ValueError:
                return jsonify({"success": False, "error": "Rail Fence Cipher requires an integer rail count >= 2."}), 400
            result = rail_fence_cipher(text, rails, 'decrypt')
            return jsonify({"success": True, "result": result})

        elif cipher == 'aes_gcm':
            if not key:
                return jsonify({"success": False, "error": "AES-256 requires the 64-character hexadecimal key used during encryption."}), 400
            result = aes_gcm_decrypt(text, key)
            return jsonify({
                "success": True,
                "result": result,
                "metadata": {
                    "verified": True,
                    "algorithm": "AES-256-GCM",
                    "note": "Authentication tag verified successfully. Data authenticity and integrity are 100% intact."
                }
            })

        else:
            return jsonify({"success": False, "error": f"Unsupported cipher algorithm: '{cipher}'"}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == '__main__':
    print("==================================================================")
    print(" Classical Ciphers & Symmetric Key Cryptography System")
    print(" Running locally at: http://127.0.0.1:5000")
    print(" Press CTRL+C to terminate the server.")
    print("==================================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
