# Classical Ciphers and Symmetric Key Cryptography
## An Interactive Encryption and Decryption System

A lightweight, beginner-friendly cybersecurity mini-project demonstrating the evolutionary progression from classical historical ciphers to modern authenticated symmetric-key cryptography (**AES-256-GCM**).

---

## 1. Abstract

Information security relies on mathematical principles to preserve confidentiality, integrity, and authenticity. This project provides an interactive, full-stack educational testbed comparing historical pencil-and-paper ciphers with contemporary symmetric standards. Users can observe how substitution and transposition ciphers manipulate text, analyze their inherent structural weaknesses (such as frequency distribution and small key spaces), and contrast them with **AES-256-GCM** (Advanced Encryption Standard in Galois/Counter Mode). Through real-time encryption, decryption, tamper detection, and metadata inspection (nonces, authentication tags), this system delivers an intuitive hands-on learning experience for students and security enthusiasts.

---

## 2. Problem Statement

Beginners in computer science and cybersecurity often struggle to bridge the conceptual gap between elementary classical ciphers (e.g., Caesar and Vigenère) and production-grade modern cryptography. Many introductory tutorials present classical ciphers as standalone toys while treating modern encryption algorithms as opaque black boxes. 

Furthermore, many learners fail to understand why **encryption alone is insufficient** without **integrity verification (tamper resistance)**, and why modern protocols demand **Authenticated Encryption with Associated Data (AEAD)**. There is a need for a unified, transparent, and zero-configuration interactive system that lets students experiment with both paradigms side by side.

---

## 3. Objectives

1. **Demonstrate Classical Ciphers:** Implement and interactively demonstrate Caesar, Monoalphabetic Substitution, Vigenère, and Rail Fence ciphers.
2. **Implement Production Symmetric Cryptography:** Integrate industry-standard **AES-256-GCM** using Python's robust `cryptography` library.
3. **Illustrate Authenticated Encryption (AEAD):** Showcase how a 128-bit authentication tag mathematically detects and rejects any tampering or unauthorized modification.
4. **Demonstrate Nonce Uniqueness:** Enforce fresh, cryptographically secure 96-bit random nonces for every encryption to eliminate ciphertext determinism and prevent nonce-reuse vulnerabilities.
5. **Provide a Comparative Analysis:** Offer a clear comparison matrix contrasting key space, cryptanalytic vulnerabilities, and modern suitability.
6. **Ensure Zero-Friction Setup:** Provide a one-click execution script (`run.bat`) that handles virtual environment creation and dependency installation automatically.

---

## 4. Technologies Used

- **Backend:** Python 3.9+ (Tested on Python 3.13)
- **Web Framework:** Flask 3.x (Lightweight micro-framework, single backend architecture)
- **Cryptographic Engine:** Python `cryptography` library (`cryptography.hazmat.primitives.ciphers.aead.AESGCM`)
- **Frontend:** Vanilla HTML5, CSS3 (Custom Dark Blue & Purple Cyber Design System), Vanilla JavaScript (ES6+ Fetch API)
- **Automated Testing:** Python `unittest` framework

---

## 5. Project Structure

```text
digital_crypto_project/
│
├── app.py                  # Single-file Flask backend with all cipher logic & REST APIs
├── requirements.txt        # Minimal Python dependencies (Flask, cryptography)
├── run.bat                 # One-click Windows startup batch script
├── test_crypto.py          # Comprehensive 20-test automated verification suite
├── README.md               # Complete academic documentation & viva questions
│
├── templates/
│   └── index.html          # Responsive cybersecurity dashboard & workspace UI
│
└── static/
    ├── style.css           # Custom dark cyber theme, glowing accents, responsive grid
    └── script.js           # Client-side dynamic forms, async API calls, clipboard actions
```

---

## 6. Installation Instructions

### Prerequisites
- Windows, macOS, or Linux operating system.
- Python 3.9 or newer installed and added to the system `PATH`.

### Manual Setup (Optional)
If you prefer configuring the environment manually instead of using `run.bat`:

1. Open your terminal or Command Prompt in the `digital_crypto_project` folder:
   ```cmd
   cd digital_crypto_project
   ```

2. Create a virtual environment:
   ```cmd
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - **Windows (Command Prompt):**
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **Windows (PowerShell):**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS:**
     ```bash
     source .venv/bin/activate
     ```

4. Install the required libraries:
   ```cmd
   pip install -r requirements.txt
   ```

---

## 7. How to Run the Project

### Option A: One-Click Execution (Recommended for Windows)
Simply double-click the `run.bat` file in `digital_crypto_project/` (or run it from the root folder).

The batch script will automatically:
1. Verify Python availability.
2. Create the `.venv` virtual environment if it does not exist.
3. Install required packages from `requirements.txt`.
4. Open `http://127.0.0.1:5000` in your default web browser.
5. Start the local Flask web server.

### Option B: Terminal Command
With the virtual environment activated, run:
```cmd
python app.py
```
Then navigate to:
```text
http://127.0.0.1:5000
```

---

## 8. How to Test Encryption and Decryption

### Testing via the Interactive Web Dashboard

#### 1. Caesar Cipher (Shift Substitution)
1. Select **Caesar Cipher** from the dropdown.
2. Enter a shift key (e.g., `3`) or click **Random Shift**.
3. Input plaintext: `Hello World! 2026`.
4. Click **Encrypt Message**. Expected output: `Khoor Zruog! 2026`.
5. Click **Swap In/Out**, then click **Decrypt Ciphertext**. Plaintext is restored.

#### 2. Monoalphabetic Substitution
1. Select **Monoalphabetic Substitution**.
2. Click **Generate Random Alphabet** to produce a 26-letter permutation key.
3. Enter plaintext and click **Encrypt Message**.
4. Click **Swap In/Out** and click **Decrypt Ciphertext** to verify exact round-trip recovery.

#### 3. Vigenère Cipher (Polyalphabetic Substitution)
1. Select **Vigenère Cipher**.
2. Enter keyword: `KEYWORD` (or click **Random Keyword**).
3. Encrypt your message. Notice that identical letters in different positions produce different ciphertext characters.

#### 4. Rail Fence Cipher (Zigzag Transposition)
1. Select **Rail Fence Cipher**.
2. Set rails to `3` (or click **Random Rails**).
3. Input: `WE ARE DISCOVERED FLEE AT ONCE`.
4. Click **Encrypt Message** to view the transposed rows. Decrypt to verify full reconstruction.

#### 5. AES-256-GCM (Authenticated Encryption)
1. Select **AES-256-GCM**.
2. Click **Generate Secure Key** to create a 256-bit (64 hex characters) cryptographic key.
3. Input plaintext: `Top Secret Financial Data`.
4. Click **Encrypt Message**:
   - The output displays a Base64-encoded packet containing `[12-byte Nonce + Ciphertext + 16-byte Auth Tag]`.
   - The **Cryptographic Metadata Inspector** expands below to show the 96-bit Nonce (Hex), 128-bit Authentication Tag (Hex), and Raw Ciphertext (Hex).
5. Click **Encrypt Message** again: Notice the ciphertext changes completely even though the message and key are identical! This proves that a fresh, unique Nonce is used every time.
6. Click **Swap In/Out** and click **Decrypt Ciphertext**. The system validates the authentication tag and recovers the plaintext.

#### 6. Tampering Verification (Integrity Test)
1. Encrypt any message using AES-256-GCM.
2. In the resulting Base64 ciphertext, modify a single character manually (e.g., replace an `A` with an `X`).
3. Click **Decrypt Ciphertext**.
4. **Result:** The system immediately rejects the ciphertext with an error:
   `Decryption Rejected: Authentication tag mismatch! Either the key is incorrect or the ciphertext was modified/tampered with.`

---

### Running the Automated Test Suite

A standalone test suite containing 20 automated unit and integration tests is included. Run it in your terminal:

```cmd
python test_crypto.py
```

**Expected Test Output:**
```text
test_aes_encryption_and_decryption ... ok
test_aes_fresh_nonce_per_encryption ... ok
test_aes_incorrect_key_rejected ... ok
test_aes_invalid_key_length ... ok
test_aes_tampered_ciphertext_rejected ... ok
test_caesar_cipher_roundtrip ... ok
test_caesar_preserves_case_and_symbols ... ok
test_rail_fence_cipher_roundtrip ... ok
test_rail_fence_invalid_rails ... ok
test_substitution_cipher_roundtrip ... ok
test_substitution_invalid_key ... ok
test_vigenere_cipher_roundtrip ... ok
test_vigenere_invalid_key ... ok
test_api_aes_gcm_encrypt_decrypt ... ok
test_api_aes_gcm_tampered_rejected ... ok
test_api_decrypt_caesar ... ok
test_api_empty_text_validation ... ok
test_api_encrypt_caesar ... ok
test_api_generate_key ... ok
test_home_page ... ok

----------------------------------------------------------------------
Ran 20 tests in 0.025s

OK
```

---

## 9. Comparative Analysis Matrix

| Algorithm Name | Encryption Type | Key Method | Main Purpose | Security Limitations | Suitable for Sensitive Data Today? |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Caesar Cipher** | Classical Substitution | Single Integer Shift (0–25) | Military communication (~100 BC) | Trivial key space ($25$ shifts); broken in milliseconds via brute force or letter frequency analysis. | **NO (Insecure)** |
| **Monoalphabetic Substitution** | Classical Substitution | 26-Letter Permutation Alphabet | Diplomatic correspondence | Preserves language letter frequency (e.g., 'E', 'T', 'A'); easily broken using statistical cryptanalysis. | **NO (Insecure)** |
| **Vigenère Cipher** | Polyalphabetic Substitution | Repeating Keyword String | 16th–19th century state secrets | Vulnerable to Kasiski examination and Friedman test to deduce key length, then solved as parallel Caesar ciphers. | **NO (Insecure)** |
| **Rail Fence Cipher** | Classical Transposition | Rail Depth (Integer $\ge 2$) | Civil War field telegraphy | Does not alter characters; preserves exact unigram/bigram letter counts. Small rail counts easily reconstructed. | **NO (Insecure)** |
| **AES-256-GCM** | Modern Authenticated (AEAD) | 256-bit Key + 96-bit Random Nonce | TLS 1.3, HTTPS, VPNs, banking, cloud storage | Symmetric key must be securely exchanged beforehand; Nonce must **never** be reused with the same key. | **YES (Industry Standard)** |

---

## 10. Expected Outcomes

- **Theoretical Clarity:** Students understand the distinction between substitution ciphers (which alter character identities) and transposition ciphers (which alter character positions).
- **Practical Awareness:** Users recognize why classical ciphers provide zero practical security against modern computing power.
- **AEAD Competency:** Students understand the role of nonces and authentication tags in protecting against active man-in-the-middle bit-flipping attacks.
- **Operational Experience:** Hands-on demonstration of symmetric key generation, ciphertext transmission, and error handling.

---

## 11. Limitations

1. **Symmetric Key Distribution Problem:** Like all symmetric algorithms, AES-256 requires sender and receiver to share the key in advance over a secure channel. (Asymmetric systems like RSA or ECC are typically used in practice to exchange symmetric keys).
2. **Classical ASCII Focus:** Classical ciphers are configured primarily for standard Latin alphabetic characters ($A$–$Z$). Non-alphabetic characters (digits, punctuation, spaces) are passed through intact to preserve readability.
3. **In-Memory Volatility:** For safety and privacy as an academic demonstration, ciphertexts and generated keys are not stored in any external database or disk file.

---

## 12. Conclusion

This project successfully bridges the historical foundations of cryptography with modern cryptographic standards. While classical algorithms (Caesar, Substitution, Vigenère, Rail Fence) played pivotal roles in historical cryptology and remain excellent didactic tools, they fall completely short against modern computational cryptanalysis. 

In contrast, **AES-256-GCM** represents the state of the art in symmetric cryptography, delivering both mathematical confidentiality and cryptographic authenticity (AEAD). Through this interactive web platform and automated test suite, complex cryptographic principles are made accessible, demonstrable, and verifiable.

---

## 13. Viva Questions with Short Answers

### Q1: What is the primary difference between a substitution cipher and a transposition cipher?
> **Answer:** A **substitution cipher** replaces plaintext letters with other letters or symbols (changing their identity), whereas a **transposition cipher** rearranges the positions of the plaintext letters without changing the letters themselves.

### Q2: Why is the Caesar cipher considered completely insecure today?
> **Answer:** The Caesar cipher has a key space of only 25 possible shifts in the English alphabet. An attacker can test all 25 keys in a fraction of a millisecond via brute-force attack or determine the shift instantly using letter frequency analysis.

### Q3: What is frequency analysis, and why does it break monoalphabetic substitution ciphers?
> **Answer:** In natural languages, certain letters appear more frequently than others (e.g., 'E' is ~12.7% of English text). A monoalphabetic cipher replaces each letter with a fixed substitute, preserving this frequency signature. An attacker maps the most frequent ciphertext letters to English frequency tables to decrypt the message without knowing the key.

### Q4: How does the Vigenère cipher improve upon simple substitution?
> **Answer:** Vigenère is a *polyalphabetic* cipher. It uses a repeating keyword, meaning the same plaintext letter is encrypted into different ciphertext letters depending on its position in the message, flattening single-letter frequency spikes.

### Q5: How was the Vigenère cipher eventually broken?
> **Answer:** Using the **Kasiski examination** (identifying repeated sequences of ciphertext to find common factors of distances between repeats) and the **Friedman test** (Index of Coincidence) to determine the keyword length $L$. Once $L$ is known, the ciphertext is broken down into $L$ independent Caesar ciphers and solved via frequency analysis.

### Q6: What does AES stand for, and what are its standard key sizes?
> **Answer:** AES stands for **Advanced Encryption Standard** (originally the Rijndael cipher, standardized by NIST in 2001). Its standard key sizes are **128 bits**, **192 bits**, and **256 bits**.

### Q7: What does "GCM" stand for in AES-256-GCM, and what makes it special?
> **Answer:** GCM stands for **Galois/Counter Mode**. It is an **AEAD** (Authenticated Encryption with Associated Data) mode that provides both **confidentiality** (encryption via Counter mode) and **integrity/authenticity** (using a Galois universal hash function to compute a 128-bit authentication tag) in a single high-speed pass.

### Q8: What is a Nonce (or IV), and why must it never be reused in AES-GCM?
> **Answer:** A Nonce (*Number used ONCE*) is an arbitrary 96-bit number that ensures encrypting the same plaintext twice produces different ciphertexts. In AES-GCM, reusing a nonce with the same key catastrophically compromises the authentication key, allowing an attacker to forge messages and recover plaintext.

### Q9: What happens if an attacker modifies just 1 bit of an AES-GCM ciphertext in transit?
> **Answer:** During decryption, the receiver computes the authentication tag over the received ciphertext. Because of the cryptographic hash properties, even a single bit flip produces a completely different tag. The authentication tag verification fails, raising an `InvalidTag` exception and causing the system to reject the message immediately.

### Q10: What is Kerckhoffs's Principle?
> **Answer:** Kerckhoffs's Principle states that a cryptosystem should be secure even if everything about the system (including the algorithm source code) is public knowledge. The only element that must remain secret is the cryptographic key. Modern ciphers like AES-256 strictly follow this principle.

---

### Project Metadata
- **Project Name:** Classical Ciphers & Symmetric Key Cryptography
- **Developer:** Sanket Jadhav
- **Course / Track:** Computer Science & Cybersecurity Mini-Project
- **Academic Year:** 2026
