"""
Security Utilities Module
Educational implementation of encryption for log protection
"""

import base64
import hashlib
import os
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class LogEncryptor:
    """
    Handles encryption and decryption of log files for educational purposes.
    Demonstrates how encryption can protect sensitive logged data.
    """
    
    def __init__(self, password: Optional[str] = None):
        """
        Initialize the encryptor with a key derived from password.
        
        Args:
            password: Optional password for encryption key derivation.
                     If not provided, uses environment variable or default.
        """
        if password is None:
            # For educational purposes, use environment variable or default
            # In production, this should be securely managed
            password = os.environ.get('KEYLOG_MASTER_KEY', 'educational_demo_key_2025')
        
        # Salt for key derivation - in production, use random per-session salt
        salt = b'keylogger_educational_salt'
        
        # Key derivation function
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        # Generate encryption key
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)
        
        # Log initialization (without exposing sensitive info)
        import logging
        logging.getLogger(__name__).info("LogEncryptor initialized")
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext string data.
        
        Args:
            plaintext: String data to encrypt
            
        Returns:
            Base64-encoded encrypted string
        """
        encrypted_bytes = self.cipher.encrypt(plaintext.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt encrypted string data.
        
        Args:
            ciphertext: Encrypted string to decrypt
            
        Returns:
            Decrypted plaintext string
        """
        decrypted_bytes = self.cipher.decrypt(ciphertext.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')


class SecurityAwarenessContent:
    """
    Provides educational security awareness content about keyloggers.
    """
    
    @staticmethod
    def get_comprehensive_guide() -> str:
        """
        Returns comprehensive educational content about keyloggers.
        """
        return """
SECURITY AWARENESS GUIDE: UNDERSTANDING KEYLOGGERS
==================================================

1. HOW REAL ATTACKERS USE KEYLOGGERS
------------------------------------
Attackers employ keyloggers through various methods:

a) Distribution Vectors:
   - Phishing emails with malicious attachments
   - Compromised software downloads and fake updates
   - Drive-by downloads from malicious websites
   - Physical access to target devices
   - Exploiting software vulnerabilities

b) Data Collection Methods:
   - Credential harvesting for banking and email accounts
   - Corporate espionage to steal intellectual property
   - Surveillance of user communications
   - Collecting personal information for identity theft
   - Capturing cryptocurrency wallet credentials

c) Advanced Techniques:
   - Memory-only keyloggers that leave no disk traces
   - Kernel-level rootkits that bypass security software
   - Form-grabbing before HTTPS encryption
   - Clipboard monitoring for copied passwords
   - Screenshot capture at login moments

2. RISKS AND IMPACTS
--------------------
Keyloggers pose significant risks at multiple levels:

Individual Level:
   - Financial loss through unauthorized transactions
   - Identity theft leading to credit damage
   - Privacy violation of personal communications
   - Reputation damage from social media compromise
   - Emotional distress from privacy invasion

Organizational Level:
   - Data breaches exposing customer information
   - Intellectual property theft and competitive disadvantage
   - Regulatory compliance violations (GDPR, HIPAA, PCI-DSS)
   - Financial penalties and legal liability
   - Operational disruption and recovery costs
   - Loss of customer trust and brand damage

3. DETECTION TECHNIQUES
-----------------------
Organizations and individuals can detect keyloggers through:

Technical Detection:
   a) Process Monitoring:
      - Check running processes for suspicious names
      - Analyze process behavior for keyboard hooks
      - Monitor for unauthorized child processes
   
   b) Network Analysis:
      - Inspect outbound connections for unusual destinations
      - Detect encrypted traffic to unknown servers
      - Monitor DNS queries for suspicious domains
      - Analyze network traffic patterns and volumes
   
   c) System Integrity:
      - Verify system file signatures and hashes
      - Check Windows registry for autorun entries
      - Monitor startup folders and scheduled tasks
      - Detect unauthorized kernel modules
   
   d) Behavioral Analysis:
      - Watch for unexpected CPU or memory spikes
      - Monitor unusual disk activity
      - Detect unexpected network connections
      - Analyze application behavior patterns

Tools for Detection:
   - Antivirus and Anti-malware software
   - Endpoint Detection and Response (EDR) solutions
   - Network Intrusion Detection Systems (NIDS)
   - Security Information and Event Management (SIEM)
   - Process Explorer and Autoruns (Sysinternals)
   - Wireshark for network traffic analysis

4. PREVENTION METHODS
---------------------
Protecting against keyloggers requires defense-in-depth:

Technical Controls:
   a) Endpoint Protection:
      - Deploy modern antivirus with behavioral detection
      - Implement application whitelisting
      - Use host-based intrusion prevention systems
      - Enable Windows Defender or equivalent
   
   b) Network Security:
      - Implement network segmentation
      - Use DNS filtering for malicious domains
      - Deploy web proxies with content filtering
      - Monitor for command and control traffic
   
   c) Authentication:
      - Use password managers to avoid typing
      - Enable multi-factor authentication everywhere
      - Implement biometric authentication where possible
      - Use hardware security keys for critical systems
   
   d) System Hardening:
      - Keep operating systems and applications updated
      - Remove unnecessary software and services
      - Apply principle of least privilege
      - Use standard user accounts for daily work

Administrative Controls:
   - Security awareness training for all users
   - Regular security audits and assessments
   - Incident response plan development
   - Vendor risk management
   - Security policy enforcement

Physical Controls:
   - Secure physical access to devices
   - Use privacy screens in public spaces
   - Implement clean desk policies
   - Regular hardware inspection for physical keyloggers

5. BEST PRACTICES SUMMARY
-------------------------
To protect against keylogger threats:

1. Never download software from untrusted sources
2. Keep all software updated with security patches
3. Use a password manager to avoid typing credentials
4. Enable multi-factor authentication for all accounts
5. Monitor system processes and network connections regularly
6. Deploy and maintain endpoint protection software
7. Practice safe browsing habits and email hygiene
8. Use virtual keyboards for highly sensitive inputs
9. Implement application whitelisting
10. Regular security awareness training for all users

6. LEGAL AND ETHICAL CONSIDERATIONS
-----------------------------------
Keyloggers exist in a legally complex space:
   - Installing without consent is illegal in most jurisdictions
   - Even for employee monitoring, explicit policies and consent required
   - Educational use should be limited to controlled environments
   - Always obtain written permission before testing on any system
   - Violations can result in criminal charges and civil liability

REMEMBER: This tool is for educational purposes only. Understanding how
keyloggers work helps defend against them. Use this knowledge ethically
to protect, not to harm.
        """