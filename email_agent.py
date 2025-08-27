#!/usr/bin/env python3
"""
Email Inbox Agent - Filter and sort email inbox with automated responses
"""

import imaplib
import smtplib
import email
import json
import re
from typing import List, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EmailAgent:
    """Email agent for filtering inbox and sending automated responses"""
    
    def __init__(self, config_file: str = 'email_config.json'):
        """Initialize the email agent with configuration"""
        self.config = self._load_config(config_file)
        self.imap_connection = None
        self.smtp_connection = None
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load email configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found. Using default configuration.")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration template"""
        return {
            "email": {
                "address": "",
                "password": "",
                "imap_server": "imap.gmail.com",
                "imap_port": 993,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587
            },
            "filters": [
                {
                    "name": "Important Senders",
                    "type": "sender",
                    "criteria": ["boss@company.com", "important@client.com"],
                    "action": "priority",
                    "folder": "Important"
                },
                {
                    "name": "Marketing",
                    "type": "subject",
                    "criteria": ["unsubscribe", "promotion", "marketing"],
                    "action": "auto_delete",
                    "folder": "Marketing"
                },
                {
                    "name": "Social Media",
                    "type": "sender_domain",
                    "criteria": ["facebook.com", "twitter.com", "linkedin.com"],
                    "action": "organize",
                    "folder": "Social"
                }
            ],
            "auto_responses": [
                {
                    "trigger": "out of office",
                    "response": "Thank you for your email. I am currently out of office and will respond when I return.",
                    "enabled": False
                },
                {
                    "trigger": "meeting request",
                    "response": "I have received your meeting request and will review it shortly.",
                    "enabled": False
                }
            ]
        }
    
    def connect_imap(self) -> bool:
        """Connect to IMAP server"""
        try:
            self.imap_connection = imaplib.IMAP4_SSL(
                self.config['email']['imap_server'],
                self.config['email']['imap_port']
            )
            self.imap_connection.login(
                self.config['email']['address'],
                self.config['email']['password']
            )
            logger.info("Successfully connected to IMAP server")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to IMAP server: {e}")
            return False
    
    def connect_smtp(self) -> bool:
        """Connect to SMTP server"""
        try:
            self.smtp_connection = smtplib.SMTP(
                self.config['email']['smtp_server'],
                self.config['email']['smtp_port']
            )
            self.smtp_connection.starttls()
            self.smtp_connection.login(
                self.config['email']['address'],
                self.config['email']['password']
            )
            logger.info("Successfully connected to SMTP server")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            return False
    
    def get_emails(self, folder: str = 'INBOX', limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve emails from specified folder"""
        if not self.imap_connection:
            if not self.connect_imap():
                return []
        
        try:
            self.imap_connection.select(folder)
            typ, message_ids = self.imap_connection.search(None, 'ALL')
            
            emails = []
            for msg_id in message_ids[0].split()[-limit:]:  # Get latest emails
                typ, msg_data = self.imap_connection.fetch(msg_id, '(RFC822)')
                email_message = email.message_from_bytes(msg_data[0][1])
                
                emails.append({
                    'id': msg_id.decode(),
                    'from': email_message.get('From', ''),
                    'to': email_message.get('To', ''),
                    'subject': email_message.get('Subject', ''),
                    'date': email_message.get('Date', ''),
                    'message': email_message
                })
            
            logger.info(f"Retrieved {len(emails)} emails from {folder}")
            return emails
        
        except Exception as e:
            logger.error(f"Failed to retrieve emails: {e}")
            return []
    
    def apply_filters(self, emails: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Apply filters to categorize emails"""
        categorized = {"uncategorized": []}
        
        for email_item in emails:
            categorized_flag = False
            
            for filter_rule in self.config['filters']:
                if self._matches_filter(email_item, filter_rule):
                    folder = filter_rule.get('folder', 'filtered')
                    if folder not in categorized:
                        categorized[folder] = []
                    categorized[folder].append(email_item)
                    categorized_flag = True
                    logger.info(f"Email '{email_item['subject']}' categorized as '{folder}'")
                    break
            
            if not categorized_flag:
                categorized["uncategorized"].append(email_item)
        
        return categorized
    
    def _matches_filter(self, email_item: Dict[str, Any], filter_rule: Dict[str, Any]) -> bool:
        """Check if email matches filter criteria"""
        filter_type = filter_rule.get('type', '')
        criteria = filter_rule.get('criteria', [])
        
        if filter_type == 'sender':
            return any(criterion.lower() in email_item['from'].lower() for criterion in criteria)
        
        elif filter_type == 'subject':
            return any(criterion.lower() in email_item['subject'].lower() for criterion in criteria)
        
        elif filter_type == 'sender_domain':
            sender_email = email_item['from']
            sender_domain = sender_email.split('@')[-1].replace('>', '') if '@' in sender_email else ''
            return any(criterion.lower() in sender_domain.lower() for criterion in criteria)
        
        return False
    
    def send_auto_response(self, original_email: Dict[str, Any], response_text: str):
        """Send automated response to an email"""
        if not self.smtp_connection:
            if not self.connect_smtp():
                return False
        
        try:
            # Create response email
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['address']
            msg['To'] = original_email['from']
            msg['Subject'] = f"Re: {original_email['subject']}"
            
            msg.attach(MIMEText(response_text, 'plain'))
            
            # Send email
            self.smtp_connection.send_message(msg)
            logger.info(f"Auto-response sent to {original_email['from']}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send auto-response: {e}")
            return False
    
    def process_auto_responses(self, emails: List[Dict[str, Any]]):
        """Process emails for automated responses"""
        for email_item in emails:
            for auto_response in self.config['auto_responses']:
                if auto_response.get('enabled', False):
                    trigger = auto_response['trigger'].lower()
                    subject = email_item['subject'].lower()
                    
                    if trigger in subject:
                        self.send_auto_response(email_item, auto_response['response'])
                        break
    
    def run_agent(self):
        """Main method to run the email agent"""
        logger.info("Starting Email Agent...")
        
        # Get emails
        emails = self.get_emails()
        if not emails:
            logger.info("No emails retrieved")
            return
        
        # Apply filters
        categorized_emails = self.apply_filters(emails)
        
        # Display results
        for category, email_list in categorized_emails.items():
            logger.info(f"{category}: {len(email_list)} emails")
        
        # Process auto-responses
        self.process_auto_responses(emails)
        
        logger.info("Email Agent processing completed")
    
    def disconnect(self):
        """Close connections"""
        if self.imap_connection:
            self.imap_connection.close()
            self.imap_connection.logout()
        
        if self.smtp_connection:
            self.smtp_connection.quit()


if __name__ == "__main__":
    agent = EmailAgent()
    try:
        agent.run_agent()
    finally:
        agent.disconnect()