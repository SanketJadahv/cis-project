"""
Script to generate a comprehensive, professional Academic Project Report PDF
for explaining 'Classical Ciphers and Symmetric Key Cryptography' to a teacher/evaluator.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and display total page numbers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress header and footer on cover page
            return
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Running Header
        self.drawString(54, 755, "College Mini-Project Report | Classical Ciphers & Symmetric Cryptography")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 748, 558, 748)
        
        # Running Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 38, page_str)
        self.drawString(54, 38, "Candidate: Sanket Jadhav | Teacher Presentation Guide")
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def build_pdf(filename="Project_Explanation_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#0F172A")    # Deep Navy
    SECONDARY = colors.HexColor("#4338CA")  # Rich Indigo
    ACCENT = colors.HexColor("#0284C7")     # Cyan Blue
    DARK_TEXT = colors.HexColor("#1E293B")
    LIGHT_BG = colors.HexColor("#F8FAFC")
    BORDER_COL = colors.HexColor("#E2E8F0")
    CALLOUT_BG = colors.HexColor("#EEF2F6")
    VIVA_BG = colors.HexColor("#F5F3FF")
    VIVA_BORDER = colors.HexColor("#7C3AED")
    
    # Typography Styles
    styles.add(ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=PRIMARY,
        alignment=1, # Center
        spaceAfter=15
    ))
    
    styles.add(ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        alignment=1,
        spaceAfter=25
    ))
    
    styles.add(ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=DARK_TEXT,
        alignment=1
    ))
    
    styles.add(ParagraphStyle(
        'DocHeading1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'DocHeading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        'DocBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155")
    ))

    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=DARK_TEXT
    ))

    styles.add(ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=DARK_TEXT
    ))

    styles.add(ParagraphStyle(
        'TableCellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    ))

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    badge_data = [[Paragraph("<font color='#4338CA'><b>ACADEMIC MINI-PROJECT COMPREHENSIVE EXPLANATION REPORT</b></font>", styles['CoverMeta'])]]
    badge_tab = Table(badge_data, colWidths=[480])
    badge_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C7D2FE")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(badge_tab)
    story.append(Spacer(1, 25))

    story.append(Paragraph("Classical Ciphers &amp; Symmetric Key Cryptography", styles['CoverTitle']))
    story.append(Paragraph("An Interactive Encryption, Decryption, and Security Verification System", styles['CoverSubtitle']))
    
    story.append(HRFlowable(width="80%", thickness=1.5, color=SECONDARY, spaceBefore=5, spaceAfter=25))
    
    intro_box = [
        [Paragraph("<b>Document Purpose:</b> This document is designed specifically for college project evaluations, seminars, and lab vivas. It provides a complete, from-scratch explanation of the system architecture, mathematical foundations of classical and modern ciphers, code implementation, step-by-step teacher demonstration workflow, and 15 curated viva questions with model answers.", styles['DocBody'])]
    ]
    intro_tab = Table(intro_box, colWidths=[480])
    intro_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(intro_tab)
    story.append(Spacer(1, 40))

    meta_table_data = [
        [Paragraph("<b>Student / Candidate:</b>", styles['TableCellBold']), Paragraph("Sanket Jadhav", styles['TableCell'])],
        [Paragraph("<b>Course / Subject:</b>", styles['TableCellBold']), Paragraph("Cybersecurity / Cryptography &amp; Network Security Lab", styles['TableCell'])],
        [Paragraph("<b>Core Technologies:</b>", styles['TableCellBold']), Paragraph("Python 3, Flask, Cryptography (PyCA), HTML5, CSS3, JavaScript", styles['TableCell'])],
        [Paragraph("<b>Key Security Primitive:</b>", styles['TableCellBold']), Paragraph("AES-256-GCM (Authenticated Encryption with Associated Data)", styles['TableCell'])],
        [Paragraph("<b>Project Repository:</b>", styles['TableCellBold']), Paragraph("digital_crypto_project (Zero-dependency virtual environment)", styles['TableCell'])],
        [Paragraph("<b>Evaluation Date:</b>", styles['TableCellBold']), Paragraph("Academic Year 2026", styles['TableCell'])]
    ]
    meta_tab = Table(meta_table_data, colWidths=[150, 330])
    meta_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_tab)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY & OBJECTIVES
    # =========================================================================
    story.append(Paragraph("1. Executive Summary &amp; Objectives", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=PRIMARY, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "<b>What is this project?</b><br/>"
        "This project is a lightweight, full-stack educational cryptography laboratory. "
        "It visually and programmatically bridges the evolutionary gap between historical pencil-and-paper ciphers "
        "(Caesar, Monoalphabetic Substitution, Vigenère, and Rail Fence) and modern enterprise-grade symmetric cryptography "
        "(<b>AES-256-GCM</b>).", styles['DocBody']
    ))
    
    story.append(Paragraph(
        "<b>Key Objectives to state to your teacher:</b>", styles['DocBodyBold']
    ))
    objectives = [
        "<b>1. Algorithmic Demonstration:</b> Provide hands-on implementation of both classical substitution (character identity change) and transposition (character position change) ciphers.",
        "<b>2. Production Cryptography:</b> Showcase how contemporary web and cloud systems protect data using <b>AES-256-GCM</b> with 256-bit keys.",
        "<b>3. The AEAD Concept (Confidentiality + Integrity):</b> Prove experimentally why encryption alone is insufficient without message authentication. Show how a 128-bit authentication tag detects bit-flipping attacks instantly.",
        "<b>4. Nonce Uniqueness:</b> Demonstrate why a fresh 96-bit random nonce is mandatory for every encryption call to prevent ciphertext determinism.",
        "<b>5. Zero Setup Friction:</b> Provide automated single-click deployment via <code>run.bat</code> without manual virtual environment configuration."
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", styles['DocBody']))

    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 2: SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("2. System Architecture &amp; File Structure", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=PRIMARY, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "The project follows a clean, single-backend, separation-of-concerns architecture designed intentionally "
        "without heavyweight frameworks to keep it simple, verifiable, and easy to explain during a viva.", styles['DocBody']
    ))

    arch_data = [
        [Paragraph("File / Module", styles['TableCellHeader']), Paragraph("Role in Architecture", styles['TableCellHeader']), Paragraph("Key Cryptographic Functions", styles['TableCellHeader'])],
        [
            Paragraph("<b>app.py</b>", styles['TableCellBold']),
            Paragraph("Flask web server and REST API controller", styles['TableCell']),
            Paragraph("<code>caesar_cipher</code>, <code>substitution_cipher</code>, <code>vigenere_cipher</code>, <code>rail_fence_cipher</code>, <code>aes_gcm_encrypt</code>, <code>aes_gcm_decrypt</code>", styles['TableCell'])
        ],
        [
            Paragraph("<b>templates/index.html</b>", styles['TableCellBold']),
            Paragraph("Responsive user interface", styles['TableCell']),
            Paragraph("Workspace forms, dynamic key generator, AES metadata inspector, side-by-side comparison matrix", styles['TableCell'])
        ],
        [
            Paragraph("<b>static/style.css</b>", styles['TableCellBold']),
            Paragraph("Cybersecurity UI styling", styles['TableCell']),
            Paragraph("Dark blue & purple theme, responsive grid, code tags, glassmorphism cards", styles['TableCell'])
        ],
        [
            Paragraph("<b>static/script.js</b>", styles['TableCellBold']),
            Paragraph("Client-side interactivity", styles['TableCell']),
            Paragraph("Asynchronous <code>fetch()</code> API requests, real-time key generation, clipboard copying, input/output swapping", styles['TableCell'])
        ],
        [
            Paragraph("<b>test_crypto.py</b>", styles['TableCellBold']),
            Paragraph("Automated verification suite", styles['TableCell']),
            Paragraph("20 unit & integration tests covering round-trips, tampering detection, wrong key rejection, and API validation", styles['TableCell'])
        ],
        [
            Paragraph("<b>run.bat</b>", styles['TableCellBold']),
            Paragraph("One-click execution script", styles['TableCell']),
            Paragraph("Checks Python, creates <code>.venv</code>, installs dependencies, launches browser at <code>127.0.0.1:5000</code>", styles['TableCell'])
        ]
    ]
    arch_tab = Table(arch_data, colWidths=[120, 150, 210])
    arch_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(arch_tab)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: CLASSICAL CIPHERS IN-DEPTH
    # =========================================================================
    story.append(Paragraph("3. Classical Ciphers Explained from Scratch", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "Classical ciphers are divided into two fundamental families: <b>Substitution Ciphers</b> (which swap character identities) "
        "and <b>Transposition Ciphers</b> (which rearrange character order).", styles['DocBody']
    ))

    # 3.1 Caesar
    story.append(Paragraph("3.1 Caesar Cipher (Monoalphabetic Shift Substitution)", styles['DocHeading2']))
    story.append(Paragraph(
        "• <b>Mechanism:</b> Shifts each letter in the message by a fixed integer key <i>k</i> positions along the alphabet.<br/>"
        "• <b>Mathematical Formula:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Encryption: <code>E(x) = (x + k) mod 26</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Decryption: <code>D(c) = (c - k) mod 26</code><br/>"
        "• <b>Security Vulnerability:</b> There are only 25 possible shifts in English. A modern computer or even a human with pencil "
        "and paper can break this in milliseconds using brute-force search across all 25 keys.", styles['DocBody']
    ))

    # 3.2 Substitution
    story.append(Paragraph("3.2 Monoalphabetic Substitution Cipher (Permutation)", styles['DocHeading2']))
    story.append(Paragraph(
        "• <b>Mechanism:</b> Maps each letter of the alphabet to a unique letter in a randomly shuffled 26-letter substitution alphabet.<br/>"
        "• <b>Key Space:</b> <code>26! &approx; 4.03 &times; 10^26</code> possible permutations. Although brute force is mathematically infeasible, "
        "it is trivial to break.<br/>"
        "• <b>Security Vulnerability:</b> <i>Frequency Analysis</i>. The cipher preserves natural language letter frequency distributions. "
        "In English, 'E' (~12.7%), 'T' (~9.1%), and 'A' (~8.2%) appear most frequently. By tallying letter frequencies in ciphertext, "
        "the mapping is easily discovered without knowing the key.", styles['DocBody']
    ))

    # 3.3 Vigenere
    story.append(Paragraph("3.3 Vigenère Cipher (Polyalphabetic Substitution)", styles['DocHeading2']))
    story.append(Paragraph(
        "• <b>Mechanism:</b> Shifts letters using a repeating keyword string. If the key is 'KEY', the 1st letter shifts by K (10), "
        "2nd by E (4), 3rd by Y (24), 4th by K (10), and so forth.<br/>"
        "• <b>Historical Significance:</b> Known for over 300 years as <i>'le chiffre indéchiffrable'</i> (the unbreakable cipher) "
        "because it flattens simple single-letter frequency spikes.<br/>"
        "• <b>Security Vulnerability:</b> Broken by Friedrich Kasiski (1863) using the <b>Kasiski Examination</b>. Repeated phrases in "
        "plaintext encrypted with the same key segment produce identical ciphertext fragments. Finding the greatest common divisor (GCD) "
        "of distances between repeats reveals the keyword length <i>L</i>. Once <i>L</i> is known, it becomes <i>L</i> separate Caesar ciphers.", styles['DocBody']
    ))

    # 3.4 Rail Fence
    story.append(Paragraph("3.4 Rail Fence Cipher (Zigzag Transposition)", styles['DocHeading2']))
    story.append(Paragraph(
        "• <b>Mechanism:</b> Plaintext is written diagonally along a zigzag pattern across <i>N</i> parallel rails (depth), "
        "then read off horizontally row by row.<br/>"
        "• <b>Key:</b> Number of rails <i>N</i> (where <i>N &ge; 2</i>).<br/>"
        "• <b>Security Vulnerability:</b> Characters are never changed, only shuffled. All letter frequencies (unigrams, bigrams) "
        "remain 100% identical. An attacker can reconstruct the message by testing small rail depths (2 to 10) in seconds.", styles['DocBody']
    ))

    callout_box = [
        [Paragraph("<b>Teacher Note / Viva Tip:</b> Make sure to emphasize to your teacher: <i>'Classical ciphers are strictly educational stepping stones. None of them provide confidentiality against modern cryptanalysis, and none of them provide any integrity checking.'</i>", styles['CalloutText'])]
    ]
    callout_tab = Table(callout_box, colWidths=[480])
    callout_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CALLOUT_BG),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94A3B8")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 4))
    story.append(callout_tab)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: MODERN SYMMETRIC CRYPTOGRAPHY (AES-256-GCM)
    # =========================================================================
    story.append(Paragraph("4. Modern Symmetric Cryptography: AES-256-GCM", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "In modern systems (TLS 1.3, HTTPS, SSH, signal protocols, disk encryption), <b>AES-256-GCM</b> is the gold standard. "
        "This project implements AES-256-GCM using the audited <code>cryptography</code> library.", styles['DocBody']
    ))

    aes_pillars = [
        ("1. 256-bit Key Space", "A 256-bit key represents 2^256 (~1.15 x 10^77) possible keys. Even if all supercomputers on Earth checked 1 trillion keys per second, it would take billions of times the age of the universe to crack it by brute force. It is quantum-resistant against Grover's algorithm with an effective 128-bit post-quantum security margin."),
        ("2. Fresh 96-bit Nonce (IV)", "A Nonce ('Number used ONCE') is a 12-byte random value. In our implementation, <code>os.urandom(12)</code> generates a fresh nonce for EVERY encryption. Even if you encrypt the word 'HELLO' 100 times with the same key, every single ciphertext is completely distinct. Nonce reuse in GCM is fatal and must be avoided."),
        ("3. 128-bit Authentication Tag (AEAD)", "Encryption provides Confidentiality (secrecy). However, classical encryption does not prevent an attacker in the middle from flipping bits in transit. GCM computes a 16-byte Galois GHASH authentication tag. If even 1 bit of ciphertext is modified, tag verification fails and decryption aborts immediately.")
    ]

    for title, desc in aes_pillars:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", styles['DocBody']))

    story.append(Spacer(1, 6))

    # Code Explanation snippet
    story.append(Paragraph("Backend Implementation Walkthrough (from <code>app.py</code>):", styles['DocBodyBold']))
    
    code_text = (
        "# 1. Encryption with Fresh Nonce & Tag Generation\n"
        "nonce = os.urandom(12)  # 96-bit fresh cryptographically secure nonce\n"
        "aesgcm = AESGCM(key_bytes)  # 256-bit key (32 bytes)\n"
        "ciphertext_and_tag = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)\n"
        "combined = nonce + ciphertext_and_tag  # Packaged as Base64\n"
        "\n"
        "# 2. Decryption & Tag Verification (Tamper Detection)\n"
        "nonce = data[:12]\n"
        "ciphertext_and_tag = data[12:]\n"
        "try:\n"
        "    plaintext_bytes = aesgcm.decrypt(nonce, ciphertext_and_tag, None)\n"
        "except InvalidTag:\n"
        "    # Rejects tampered data or wrong keys immediately!\n"
        "    raise ValueError('Authentication tag mismatch! Key wrong or data tampered.')"
    )
    
    code_tab = Table([[Paragraph(code_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), styles['CodeSnippet'])]], colWidths=[480])
    code_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(code_tab)

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: COMPARISON MATRIX
    # =========================================================================
    story.append(Paragraph("5. Classical vs. Modern Comparison Matrix", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    comp_data = [
        [Paragraph("Algorithm", styles['TableCellHeader']), Paragraph("Encryption Type", styles['TableCellHeader']), Paragraph("Key Method", styles['TableCellHeader']), Paragraph("Security Limitation", styles['TableCellHeader']), Paragraph("Modern Safe?", styles['TableCellHeader'])],
        [
            Paragraph("<b>Caesar</b>", styles['TableCellBold']),
            Paragraph("Classical Shift", styles['TableCell']),
            Paragraph("1 Integer (0-25)", styles['TableCell']),
            Paragraph("Brute force in 25 tries; letter frequency.", styles['TableCell']),
            Paragraph("<font color='#DC2626'><b>NO</b></font>", styles['TableCell'])
        ],
        [
            Paragraph("<b>Substitution</b>", styles['TableCellBold']),
            Paragraph("Monoalphabetic", styles['TableCell']),
            Paragraph("26-Letter alphabet", styles['TableCell']),
            Paragraph("Vulnerable to letter frequency analysis.", styles['TableCell']),
            Paragraph("<font color='#DC2626'><b>NO</b></font>", styles['TableCell'])
        ],
        [
            Paragraph("<b>Vigenère</b>", styles['TableCellBold']),
            Paragraph("Polyalphabetic", styles['TableCell']),
            Paragraph("Repeating keyword", styles['TableCell']),
            Paragraph("Broken via Kasiski test and Friedman index.", styles['TableCell']),
            Paragraph("<font color='#DC2626'><b>NO</b></font>", styles['TableCell'])
        ],
        [
            Paragraph("<b>Rail Fence</b>", styles['TableCellBold']),
            Paragraph("Transposition", styles['TableCell']),
            Paragraph("Rail count depth", styles['TableCell']),
            Paragraph("Letters unaltered; anagramming & depth guessing.", styles['TableCell']),
            Paragraph("<font color='#DC2626'><b>NO</b></font>", styles['TableCell'])
        ],
        [
            Paragraph("<b>AES-256-GCM</b>", styles['TableCellBold']),
            Paragraph("Modern AEAD", styles['TableCell']),
            Paragraph("256-bit key + 96-bit Nonce", styles['TableCell']),
            Paragraph("Key must be kept secret; Nonce never reused.", styles['TableCell']),
            Paragraph("<font color='#16A34A'><b>YES (Standard)</b></font>", styles['TableCell'])
        ]
    ]
    comp_tab = Table(comp_data, colWidths=[75, 85, 95, 160, 65])
    comp_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (4,1), (4,-1), 'CENTER'),
    ]))
    story.append(comp_tab)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: HOW TO EXPLAIN THIS TO YOUR TEACHER (DEMO SCRIPT)
    # =========================================================================
    story.append(Paragraph("6. Step-by-Step Teacher Demonstration Guide", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "Follow this exact 5-step walkthrough when presenting the project in front of your teacher or external examiner:", styles['DocBody']
    ))

    demo_steps = [
        ("Step 1: Introduction (30 seconds)",
         "State clearly: <i>'Good morning, respected teacher. My project is titled <b>Classical Ciphers and Symmetric Key Cryptography</b>. The goal is to demonstrate how cryptography evolved from ancient pencil-and-paper ciphers like Caesar and Vigenère to modern authenticated symmetric encryption like AES-256-GCM.'</i>"),
        
        ("Step 2: Demonstrate Caesar & Substitution (1 minute)",
         "Select <b>Caesar Cipher</b>, type <code>Hello World!</code>, set shift key to <code>3</code>, and click <b>Encrypt</b> (output: <code>Khoor Zruog!</code>). Explain: <i>'Notice that every character shifts by 3. This is monoalphabetic substitution. Its weakness is that letter frequencies remain unchanged, making it vulnerable to statistical analysis.'</i>"),
         
        ("Step 3: Demonstrate Rail Fence Transposition (1 minute)",
         "Select <b>Rail Fence Cipher</b> with 3 rails and encrypt. Explain: <i>'Unlike Caesar which substitutes letters, Rail Fence transposes their positions along a zigzag path. The characters themselves never change.'</i>"),
         
        ("Step 4: Demonstrate AES-256-GCM & Fresh Nonce (2 minutes)",
         "Select <b>AES-256-GCM</b>. Click <b>Generate Secure Key</b> (64 hex chars = 256 bits). Enter a message and click <b>Encrypt</b>. Point to the <b>Cryptographic Metadata Inspector</b> below the output box showing the <b>96-bit Nonce</b>, <b>128-bit Auth Tag</b>, and <b>Ciphertext</b>. Click <b>Encrypt again</b> with the same message and key. Show your teacher that the ciphertext changes completely! Explain: <i>'Because we generate a fresh 96-bit cryptographically secure random nonce each time, identical plaintexts never yield the same ciphertext.'</i>"),
         
        ("Step 5: The Showstopper: Tamper Detection (1 minute)",
         "Click <b>Swap In/Out</b> so the ciphertext moves to the input box. Manually edit <b>just one character</b> of the Base64 ciphertext. Click <b>Decrypt</b>. Show your teacher the error message: <code>Authentication tag mismatch!</code> Explain: <i>'This demonstrates AEAD. Modern cryptography does not just hide data; it guarantees integrity. If a man-in-the-middle attacker tampers with even one bit, the Galois tag verification fails and the data is safely rejected.'</i>")
    ]

    for step_title, step_desc in demo_steps:
        box_data = [
            [Paragraph(f"<b>{step_title}</b>", styles['TableCellBold'])],
            [Paragraph(step_desc, styles['TableCell'])]
        ]
        box_tab = Table(box_data, colWidths=[480])
        box_tab.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
            ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(box_tab)
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 7: VIVA QUESTIONS & MODEL ANSWERS (15 QUESTIONS)
    # =========================================================================
    story.append(Paragraph("7. Comprehensive Viva Questions &amp; Answers", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    viva_qa = [
        ("Q1: What is the fundamental difference between substitution and transposition?",
         "<b>Answer:</b> Substitution replaces plaintext letters with other letters or symbols, changing their identity. Transposition rearranges the order of the letters without changing the letters themselves."),
        
        ("Q2: What is Kerckhoffs's Principle, and does AES follow it?",
         "<b>Answer:</b> Kerckhoffs's Principle states that a cryptographic system must remain secure even if everything about the system (algorithms, source code, hardware) is public knowledge; only the key must remain secret. AES is completely public and standardized by NIST, yet mathematically secure."),
        
        ("Q3: Why does frequency analysis break monoalphabetic substitution so easily?",
         "<b>Answer:</b> In any natural language, letter distributions are non-uniform (in English, 'E' is ~12.7%, 'T' is ~9.1%). Monoalphabetic substitution uses a fixed 1-to-1 mapping, so the ciphertext preserves these exact statistical peaks."),
         
        ("Q4: How was the Vigenère cipher broken if it flattens single-letter frequencies?",
         "<b>Answer:</b> Via the Kasiski Examination and Friedman test. Repeating patterns in ciphertext reveal common factors of distance, which exposes the keyword length L. Once L is known, the ciphertext is split into L separate Caesar ciphers and solved."),
         
        ("Q5: What are the three standard key lengths of AES?",
         "<b>Answer:</b> 128 bits (10 rounds), 192 bits (12 rounds), and 256 bits (14 rounds). Our project uses AES-256."),
         
        ("Q6: What is AEAD, and why is it superior to basic encryption modes like CBC or ECB?",
         "<b>Answer:</b> AEAD stands for Authenticated Encryption with Associated Data. Basic modes (like ECB/CBC) only provide confidentiality and are vulnerable to padding oracle and bit-flipping attacks. AEAD provides simultaneous confidentiality and tamper-proof authentication."),
         
        ("Q7: What does GCM stand for in AES-GCM?",
         "<b>Answer:</b> Galois/Counter Mode. It combines Counter mode (CTR) for high-speed streaming encryption with Galois field GHASH multiplication to compute a 128-bit authentication tag."),
         
        ("Q8: Why is Nonce reuse catastrophic in AES-GCM?",
         "<b>Answer:</b> If the same Nonce and Key are used to encrypt two different messages, the XOR of the two plaintexts is revealed directly. Furthermore, the Galois hash key (H) can be recovered, allowing attackers to forge arbitrary authentication tags."),
         
        ("Q9: What happens when tampered ciphertext is submitted to AES-GCM decryption?",
         "<b>Answer:</b> The receiver computes the GHASH over the received ciphertext. Even a 1-bit alteration causes a completely different hash output. The authentication tag verification fails, raising an InvalidTag exception, and the ciphertext is rejected without decoding."),
         
        ("Q10: What is the difference between symmetric and asymmetric cryptography?",
         "<b>Answer:</b> Symmetric cryptography (e.g., AES) uses the same secret key for both encryption and decryption. Asymmetric cryptography (e.g., RSA, ECC) uses a mathematically linked key pair: a public key for encryption and a private key for decryption."),
         
        ("Q11: How is the symmetric key safely exchanged in real-world protocols?",
         "<b>Answer:</b> Real-world protocols like TLS 1.3 use asymmetric cryptography (e.g., Elliptic Curve Diffie-Hellman Ephemeral - ECDHE) to securely agree upon a shared symmetric key, which is then used with AES-256-GCM for bulk data encryption."),
         
        ("Q12: Why did you use Python's 'cryptography' library instead of implementing AES manually?",
         "<b>Answer:</b> Modern cryptography requires constant-time hardware-accelerated primitives (AES-NI) to prevent cache and timing side-channel attacks. Implementing AES manually in Python is vulnerable to timing attacks and is unsafe for production."),
         
        ("Q13: How many automated tests does your project have, and what do they verify?",
         "<b>Answer:</b> We built a suite of 20 automated unit and integration tests in <code>test_crypto.py</code> that verify round-trip accuracy, non-alpha preservation, invalid key rejection, nonce uniqueness, and API tampering detection."),
         
        ("Q14: What is the key size used in your Caesar cipher and Rail Fence cipher?",
         "<b>Answer:</b> Caesar uses an integer shift between 1 and 25. Rail Fence uses an integer rail count N >= 2."),
         
        ("Q15: What is the single biggest takeaway of this project?",
         "<b>Answer:</b> Classical ciphers are valuable educational history, but real-world security requires modern authenticated primitives (like AES-256-GCM) that provide both mathematical confidentiality and cryptographic tamper resistance.")
    ]

    for q, a in viva_qa:
        q_box = [
            [Paragraph(f"<font color='#4338CA'><b>{q}</b></font>", styles['DocBodyBold'])],
            [Paragraph(a, styles['DocBody'])]
        ]
        q_tab = Table(q_box, colWidths=[480])
        q_tab.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), VIVA_BG),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#DDD6FE")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(q_tab)
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Academic Project Report PDF generated: {filename}")

if __name__ == "__main__":
    build_pdf("Project_Explanation_Report.pdf")
    build_pdf(os.path.join("digital_crypto_project", "Project_Explanation_Report.pdf"))
