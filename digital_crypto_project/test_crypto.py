"""
Automated Test Suite for Classical Ciphers & AES-256-GCM
Can be executed with: python test_crypto.py
"""

import unittest
import secrets
from app import (
    caesar_cipher,
    substitution_cipher,
    vigenere_cipher,
    rail_fence_cipher,
    aes_gcm_encrypt,
    aes_gcm_decrypt,
    app
)

class TestClassicalCiphers(unittest.TestCase):

    def setUp(self):
        self.message = "The quick brown fox jumps over the lazy dog! 1234 @#$"

    def test_caesar_cipher_roundtrip(self):
        """Test Caesar cipher encryption and decryption with standard and edge shifts."""
        for shift in [1, 3, 13, 25, 52]:
            encrypted = caesar_cipher(self.message, shift, mode='encrypt')
            decrypted = caesar_cipher(encrypted, shift, mode='decrypt')
            self.assertEqual(decrypted, self.message, f"Caesar failed at shift {shift}")

    def test_caesar_preserves_case_and_symbols(self):
        raw = "Hello, World! 99"
        encrypted = caesar_cipher(raw, 3, mode='encrypt')
        self.assertEqual(encrypted, "Khoor, Zruog! 99")

    def test_substitution_cipher_roundtrip(self):
        """Test Monoalphabetic substitution with a custom key."""
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        encrypted = substitution_cipher(self.message, key, mode='encrypt')
        decrypted = substitution_cipher(encrypted, key, mode='decrypt')
        self.assertEqual(decrypted, self.message)

    def test_substitution_invalid_key(self):
        """Test that invalid keys (duplicates, wrong length) are rejected."""
        with self.assertRaises(ValueError):
            substitution_cipher(self.message, "A" * 26, mode='encrypt')
        with self.assertRaises(ValueError):
            substitution_cipher(self.message, "SHORTKEY", mode='encrypt')

    def test_vigenere_cipher_roundtrip(self):
        """Test Vigenere cipher encryption and decryption."""
        key = "CRYPTOGRAPHY"
        encrypted = vigenere_cipher(self.message, key, mode='encrypt')
        decrypted = vigenere_cipher(encrypted, key, mode='decrypt')
        self.assertEqual(decrypted, self.message)

    def test_vigenere_invalid_key(self):
        """Test that empty or non-alphabetic keys are rejected."""
        with self.assertRaises(ValueError):
            vigenere_cipher(self.message, "12345!@#", mode='encrypt')

    def test_rail_fence_cipher_roundtrip(self):
        """Test Rail Fence transposition cipher with multiple rail counts."""
        for rails in [2, 3, 5, 8]:
            encrypted = rail_fence_cipher(self.message, rails, mode='encrypt')
            decrypted = rail_fence_cipher(encrypted, rails, mode='decrypt')
            self.assertEqual(decrypted, self.message, f"Rail fence failed with {rails} rails")

    def test_rail_fence_invalid_rails(self):
        """Test that rail counts < 2 are rejected."""
        with self.assertRaises(ValueError):
            rail_fence_cipher(self.message, 1, mode='encrypt')


class TestAES256GCM(unittest.TestCase):

    def setUp(self):
        self.message = "Top Secret: Cryptographic Keys & Sensitive Financial Data."
        self.key_hex = secrets.token_hex(32)  # 256 bits

    def test_aes_encryption_and_decryption(self):
        """Test normal AES-256-GCM encryption and successful decryption."""
        res = aes_gcm_encrypt(self.message, self.key_hex)
        ciphertext = res["ciphertext"]
        decrypted = aes_gcm_decrypt(ciphertext, self.key_hex)
        self.assertEqual(decrypted, self.message)

    def test_aes_fresh_nonce_per_encryption(self):
        """Ensure two encryptions of the same plaintext produce different nonces and ciphertexts."""
        res1 = aes_gcm_encrypt(self.message, self.key_hex)
        res2 = aes_gcm_encrypt(self.message, self.key_hex)
        self.assertNotEqual(res1["nonce_hex"], res2["nonce_hex"], "Nonce must never be reused")
        self.assertNotEqual(res1["ciphertext"], res2["ciphertext"], "Ciphertexts must differ due to unique nonces")

    def test_aes_tampered_ciphertext_rejected(self):
        """Ensure tampered ciphertext triggers authentication tag mismatch."""
        res = aes_gcm_encrypt(self.message, self.key_hex)
        b64 = list(res["ciphertext"])
        # Alter a single character in the base64 ciphertext
        b64[10] = 'X' if b64[10] != 'X' else 'Y'
        tampered = "".join(b64)

        with self.assertRaises(ValueError) as ctx:
            aes_gcm_decrypt(tampered, self.key_hex)
        self.assertIn("Authentication tag mismatch", str(ctx.exception))

    def test_aes_incorrect_key_rejected(self):
        """Ensure decryption with an incorrect key triggers authentication tag mismatch."""
        res = aes_gcm_encrypt(self.message, self.key_hex)
        wrong_key = secrets.token_hex(32)

        with self.assertRaises(ValueError) as ctx:
            aes_gcm_decrypt(res["ciphertext"], wrong_key)
        self.assertIn("Authentication tag mismatch", str(ctx.exception))

    def test_aes_invalid_key_length(self):
        """Ensure keys with invalid length or non-hex characters are rejected."""
        short_key = secrets.token_hex(16)  # only 128-bit
        with self.assertRaises(ValueError):
            aes_gcm_encrypt(self.message, short_key)


class TestFlaskEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        """Test that homepage loads with HTTP 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api_encrypt_caesar(self):
        """Test /api/encrypt with Caesar cipher."""
        payload = {"cipher": "caesar", "text": "HELLO", "key": "3"}
        response = self.client.post('/api/encrypt', json=payload)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["result"], "KHOOR")

    def test_api_decrypt_caesar(self):
        """Test /api/decrypt with Caesar cipher."""
        payload = {"cipher": "caesar", "text": "KHOOR", "key": "3"}
        response = self.client.post('/api/decrypt', json=payload)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["result"], "HELLO")

    def test_api_empty_text_validation(self):
        """Test that empty text returns HTTP 400."""
        payload = {"cipher": "caesar", "text": "", "key": "3"}
        response = self.client.post('/api/encrypt', json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("cannot be empty", data["error"])

    def test_api_generate_key(self):
        """Test /api/generate-key endpoint for all ciphers."""
        for c in ['caesar', 'substitution', 'vigenere', 'rail_fence', 'aes_gcm']:
            response = self.client.get(f'/api/generate-key?cipher={c}')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data["success"])
            self.assertIn("key", data)

    def test_api_aes_gcm_encrypt_decrypt(self):
        """Test AES-256-GCM through Flask API endpoints."""
        key = secrets.token_hex(32)
        secret_msg = "Top Secret College Project 2026!"
        
        # Encrypt
        enc_resp = self.client.post('/api/encrypt', json={"cipher": "aes_gcm", "text": secret_msg, "key": key})
        self.assertEqual(enc_resp.status_code, 200)
        enc_data = enc_resp.get_json()
        self.assertTrue(enc_data["success"])
        ciphertext = enc_data["result"]
        
        # Decrypt
        dec_resp = self.client.post('/api/decrypt', json={"cipher": "aes_gcm", "text": ciphertext, "key": key})
        self.assertEqual(dec_resp.status_code, 200)
        dec_data = dec_resp.get_json()
        self.assertTrue(dec_data["success"])
        self.assertEqual(dec_data["result"], secret_msg)

    def test_api_aes_gcm_tampered_rejected(self):
        """Test that tampered AES-256-GCM ciphertext is rejected via API."""
        key = secrets.token_hex(32)
        enc_resp = self.client.post('/api/encrypt', json={"cipher": "aes_gcm", "text": "Authenticate me!", "key": key})
        enc_data = enc_resp.get_json()
        b64 = list(enc_data["result"])
        b64[5] = 'Z' if b64[5] != 'Z' else 'Y'
        tampered = "".join(b64)
        
        dec_resp = self.client.post('/api/decrypt', json={"cipher": "aes_gcm", "text": tampered, "key": key})
        self.assertEqual(dec_resp.status_code, 400)
        dec_data = dec_resp.get_json()
        self.assertFalse(dec_data["success"])
        self.assertIn("Authentication tag mismatch", dec_data["error"])


if __name__ == '__main__':
    print("================================================================")
    print(" Running Cryptography Project Test Suite")
    print("================================================================")
    unittest.main(verbosity=2)
