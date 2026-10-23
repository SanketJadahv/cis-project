/**
 * Classical Ciphers & Symmetric Key Cryptography
 * Interactive Frontend Controller
 * Author: Sanket Jadhav
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Element References
    const cipherSelect = document.getElementById('cipher-select');
    const cipherKey = document.getElementById('cipher-key');
    const keyLabel = document.getElementById('key-label');
    const keyHint = document.getElementById('key-hint');
    const btnGenerateKey = document.getElementById('btn-generate-key');
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');
    const charCount = document.getElementById('char-count');
    
    const btnEncrypt = document.getElementById('btn-encrypt');
    const btnDecrypt = document.getElementById('btn-decrypt');
    const btnSwap = document.getElementById('btn-swap');
    const btnCopy = document.getElementById('btn-copy');
    const btnClearAll = document.getElementById('btn-clear-all');
    const btnSampleMsg = document.getElementById('btn-sample-msg');
    
    const statusBox = document.getElementById('status-box');
    const statusMessage = document.getElementById('status-message');
    const outputBadge = document.getElementById('output-badge');
    
    // AES Deep Inspector Elements
    const aesInspector = document.getElementById('aes-inspector');
    const metaNonce = document.getElementById('meta-nonce');
    const metaTag = document.getElementById('meta-tag');
    const metaRaw = document.getElementById('meta-raw');
    const metaIntegrity = document.getElementById('meta-integrity');
    
    // Educational Insight Elements
    const cipherTypeBadge = document.getElementById('cipher-type-badge');
    const detailName = document.getElementById('detail-name');
    const detailDesc = document.getElementById('detail-desc');
    const detailKeyMethod = document.getElementById('detail-key-method');
    const detailPurpose = document.getElementById('detail-purpose');
    const detailLimitations = document.getElementById('detail-limitations');
    const detailSuitability = document.getElementById('detail-suitability');
    const detailSuitabilityBox = document.getElementById('detail-suitability-box');
    
    const toast = document.getElementById('toast');

    // Cache of ciphers metadata
    let ciphersData = {};

    // Sample messages for quick testing
    const sampleMessages = [
        "Confidential Strategy: Project Quantum Shield launches tomorrow at 0600 UTC.",
        "The quick brown fox jumps over the lazy dog! 1234567890",
        "Cryptography ensures both confidentiality and mathematical integrity.",
        "Security must reside entirely in the secrecy of the key, not the algorithm."
    ];
    let sampleIdx = 0;

    // ==========================================
    // 1. INITIALIZATION & METADATA LOADING
    // ==========================================
    async function init() {
        try {
            const res = await fetch('/api/ciphers-info');
            const data = await res.json();
            if (data.success) {
                ciphersData = data.ciphers;
            }
        } catch (err) {
            console.warn('Could not pre-fetch ciphers info:', err);
        }

        // Initialize key for default cipher (AES-256-GCM)
        handleCipherChange();
        fetchGeneratedKey();
    }

    // ==========================================
    // 2. CIPHER CONFIGURATION & UI UPDATES
    // ==========================================
    function handleCipherChange() {
        const selected = cipherSelect.value;
        hideStatus();

        if (selected === 'aes_gcm') {
            keyLabel.innerHTML = '<strong>2. AES-256 Key (256-bit Hex)</strong>';
            cipherKey.placeholder = '64-character hexadecimal key (e.g. 32 bytes)';
            keyHint.innerText = 'AES-256 requires exactly 64 hexadecimal characters. Click "Generate Secure Key" for a fresh key.';
            btnGenerateKey.innerHTML = '&#x26A1; Generate Secure Key';
            btnGenerateKey.style.display = 'inline-block';
        } else if (selected === 'caesar') {
            keyLabel.innerHTML = '<strong>2. Caesar Shift Key (Integer)</strong>';
            cipherKey.placeholder = 'e.g. 3 (or any integer 1 to 25)';
            keyHint.innerText = 'An integer specifying the number of alphabet positions to shift letters.';
            btnGenerateKey.innerHTML = '&#x26A1; Random Shift';
            btnGenerateKey.style.display = 'inline-block';
            if (!cipherKey.value || cipherKey.value.length > 5) cipherKey.value = '3';
        } else if (selected === 'substitution') {
            keyLabel.innerHTML = '<strong>2. Substitution Alphabet (26 Letters)</strong>';
            cipherKey.placeholder = '26 distinct letters (e.g. QWERTYUIOPASDFGHJKLZXCVBNM)';
            keyHint.innerText = 'Custom 26-character alphabet permutation (A-Z with no duplicates).';
            btnGenerateKey.innerHTML = '&#x26A1; Generate Random Alphabet';
            btnGenerateKey.style.display = 'inline-block';
            if (!cipherKey.value || cipherKey.value.length !== 26) cipherKey.value = 'QWERTYUIOPASDFGHJKLZXCVBNM';
        } else if (selected === 'vigenere') {
            keyLabel.innerHTML = '<strong>2. Vigen&egrave;re Keyword (String)</strong>';
            cipherKey.placeholder = 'e.g. SECRET or KEYWORD';
            keyHint.innerText = 'An alphabetic word repeated across message letters to determine individual shifts.';
            btnGenerateKey.innerHTML = '&#x26A1; Random Keyword';
            btnGenerateKey.style.display = 'inline-block';
            if (!cipherKey.value || cipherKey.value.length > 20) cipherKey.value = 'CYBERSECURITY';
        } else if (selected === 'rail_fence') {
            keyLabel.innerHTML = '<strong>2. Rail Fence Depth (Rails &ge; 2)</strong>';
            cipherKey.placeholder = 'e.g. 3 (number of rails)';
            keyHint.innerText = 'An integer &ge; 2 determining the zigzag transposition depth across rows.';
            btnGenerateKey.innerHTML = '&#x26A1; Random Rails';
            btnGenerateKey.style.display = 'inline-block';
            if (!cipherKey.value || isNaN(cipherKey.value)) cipherKey.value = '3';
        }

        updateEducationalCard(selected);
    }

    function updateEducationalCard(cipherKey) {
        const info = ciphersData[cipherKey];
        if (!info) return;

        detailName.innerText = info.name;
        detailDesc.innerText = info.description;
        detailKeyMethod.innerText = info.key_type;
        detailPurpose.innerText = info.purpose;
        detailLimitations.innerText = info.limitations;

        if (info.modern_secure) {
            cipherTypeBadge.innerText = 'Modern Authenticated AEAD';
            cipherTypeBadge.className = 'badge-tag tag-modern';
            detailSuitability.innerHTML = '&#x2714; YES &mdash; Production Ready Standard';
            detailSuitability.className = 'text-success font-bold';
            detailSuitabilityBox.style.borderColor = 'rgba(16, 185, 129, 0.4)';
        } else {
            cipherTypeBadge.innerText = 'Classical (Educational Only)';
            cipherTypeBadge.className = 'badge-tag tag-classical';
            detailSuitability.innerHTML = '&#x2716; NO &mdash; Cryptographically Insecure Today';
            detailSuitability.className = 'text-danger font-bold';
            detailSuitabilityBox.style.borderColor = 'rgba(239, 68, 68, 0.4)';
        }
    }

    // ==========================================
    // 3. KEY GENERATOR TRIGGER
    // ==========================================
    async function fetchGeneratedKey() {
        const selected = cipherSelect.value;
        try {
            const res = await fetch(`/api/generate-key?cipher=${encodeURIComponent(selected)}`);
            const data = await res.json();
            if (data.success && data.key) {
                cipherKey.value = data.key;
                showToast(`Generated fresh key for ${selected.toUpperCase()}`);
            }
        } catch (err) {
            showStatus('Error generating key: ' + err.message, 'error');
        }
    }

    // ==========================================
    // 4. ENCRYPT OPERATION
    // ==========================================
    async function performEncrypt() {
        hideStatus();
        const text = inputText.value.trim();
        const key = cipherKey.value.trim();
        const cipher = cipherSelect.value;

        if (!text) {
            showStatus('Please enter a message to encrypt.', 'error');
            inputText.focus();
            return;
        }

        if (!key) {
            showStatus('Please provide an encryption key.', 'error');
            cipherKey.focus();
            return;
        }

        btnEncrypt.disabled = true;
        btnEncrypt.innerHTML = 'Encrypting...';

        try {
            const res = await fetch('/api/encrypt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cipher, text, key })
            });
            const data = await res.json();

            if (!res.ok || !data.success) {
                throw new Error(data.error || 'Encryption failed.');
            }

            outputText.value = data.result;
            outputBadge.innerText = 'Encrypted (' + cipher.toUpperCase() + ')';
            outputBadge.className = 'badge-mini badge-success';

            // Handle AES Metadata
            if (cipher === 'aes_gcm' && data.metadata) {
                metaNonce.innerText = data.metadata.nonce_hex;
                metaTag.innerText = data.metadata.tag_hex;
                metaRaw.innerText = data.metadata.raw_ciphertext_hex;
                metaIntegrity.innerHTML = '&#x2714; Authenticated Encryption Verified (Fresh 96-bit Nonce)';
                metaIntegrity.className = 'meta-value text-success';
                aesInspector.classList.remove('hidden');
            } else {
                aesInspector.classList.add('hidden');
            }

            showStatus('Encryption completed successfully!', 'success');
        } catch (err) {
            showStatus(err.message, 'error');
            outputBadge.innerText = 'Encryption Error';
            outputBadge.className = 'badge-mini badge-danger';
        } finally {
            btnEncrypt.disabled = false;
            btnEncrypt.innerHTML = '<span class="btn-icon">&#x1F512;</span> Encrypt Message';
        }
    }

    // ==========================================
    // 5. DECRYPT OPERATION
    // ==========================================
    async function performDecrypt() {
        hideStatus();
        const text = inputText.value.trim();
        const key = cipherKey.value.trim();
        const cipher = cipherSelect.value;

        if (!text) {
            showStatus('Please enter ciphertext in the message input box to decrypt.', 'error');
            inputText.focus();
            return;
        }

        if (!key) {
            showStatus('Please provide the decryption key.', 'error');
            cipherKey.focus();
            return;
        }

        btnDecrypt.disabled = true;
        btnDecrypt.innerHTML = 'Decrypting...';

        try {
            const res = await fetch('/api/decrypt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cipher, text, key })
            });
            const data = await res.json();

            if (!res.ok || !data.success) {
                throw new Error(data.error || 'Decryption failed.');
            }

            outputText.value = data.result;
            outputBadge.innerText = 'Decrypted (' + cipher.toUpperCase() + ')';
            outputBadge.className = 'badge-mini badge-success';

            if (cipher === 'aes_gcm') {
                metaIntegrity.innerHTML = '&#x2714; Decryption Integrity Verified: Auth Tag Matched Perfectly';
                metaIntegrity.className = 'meta-value text-success';
                aesInspector.classList.remove('hidden');
            } else {
                aesInspector.classList.add('hidden');
            }

            showStatus('Decryption successful! Plaintext recovered.', 'success');
        } catch (err) {
            showStatus(err.message, 'error');
            outputBadge.innerText = 'Decryption Failed';
            outputBadge.className = 'badge-mini badge-danger';
            if (cipher === 'aes_gcm') {
                metaIntegrity.innerHTML = '&#x2716; Integrity Failure: Tag mismatch or wrong key!';
                metaIntegrity.className = 'meta-value text-danger';
                aesInspector.classList.remove('hidden');
            }
        } finally {
            btnDecrypt.disabled = false;
            btnDecrypt.innerHTML = '<span class="btn-icon">&#x1F513;</span> Decrypt Ciphertext';
        }
    }

    // ==========================================
    // 6. UTILITY ACTIONS (SWAP, COPY, CLEAR, SAMPLE)
    // ==========================================
    function swapInputOutput() {
        const out = outputText.value;
        if (!out) {
            showToast('No output to swap into input.');
            return;
        }
        inputText.value = out;
        outputText.value = '';
        updateCharCount();
        outputBadge.innerText = 'Swapped';
        outputBadge.className = 'badge-mini badge-idle';
        showToast('Output moved to Input field for reverse decryption testing.');
    }

    function copyResultToClipboard() {
        const val = outputText.value;
        if (!val) {
            showToast('Nothing to copy yet!');
            return;
        }
        navigator.clipboard.writeText(val).then(() => {
            showToast('Result copied to clipboard!');
        }).catch(() => {
            // Fallback for older browsers
            outputText.select();
            document.execCommand('copy');
            showToast('Copied to clipboard!');
        });
    }

    function clearAll() {
        inputText.value = '';
        outputText.value = '';
        updateCharCount();
        hideStatus();
        aesInspector.classList.add('hidden');
        outputBadge.innerText = 'Awaiting Input';
        outputBadge.className = 'badge-mini badge-idle';
        showToast('Workspace cleared.');
    }

    function loadSampleMessage() {
        inputText.value = sampleMessages[sampleIdx % sampleMessages.length];
        sampleIdx++;
        updateCharCount();
        hideStatus();
        showToast('Sample message loaded.');
    }

    function updateCharCount() {
        const count = inputText.value.length;
        charCount.innerText = `${count} char${count === 1 ? '' : 's'}`;
    }

    function showStatus(msg, type) {
        statusMessage.innerText = msg;
        statusBox.className = `status-box ${type}`;
        statusBox.classList.remove('hidden');
    }

    function hideStatus() {
        statusBox.classList.add('hidden');
    }

    function showToast(msg) {
        toast.innerText = msg;
        toast.classList.remove('hidden');
        setTimeout(() => {
            toast.classList.add('hidden');
        }, 2500);
    }

    // ==========================================
    // 7. EVENT LISTENERS
    // ==========================================
    cipherSelect.addEventListener('change', handleCipherChange);
    btnGenerateKey.addEventListener('click', fetchGeneratedKey);
    btnEncrypt.addEventListener('click', performEncrypt);
    btnDecrypt.addEventListener('click', performDecrypt);
    btnSwap.addEventListener('click', swapInputOutput);
    btnCopy.addEventListener('click', copyResultToClipboard);
    btnClearAll.addEventListener('click', clearAll);
    btnSampleMsg.addEventListener('click', loadSampleMessage);
    inputText.addEventListener('input', updateCharCount);

    // Initialize the app
    init();
});
