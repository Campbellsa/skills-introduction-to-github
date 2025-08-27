#!/usr/bin/env python3
"""
Command Line Interface for Email Agent
"""

import argparse
import sys
import json
from email_agent import EmailAgent


def main():
    parser = argparse.ArgumentParser(description='Email Inbox Agent - Filter and automate email responses')
    parser.add_argument('--config', '-c', default='email_config.json', 
                       help='Path to configuration file (default: email_config.json)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                       help='Run without sending auto-responses')
    parser.add_argument('--folder', '-f', default='INBOX',
                       help='Email folder to process (default: INBOX)')
    parser.add_argument('--limit', '-l', type=int, default=50,
                       help='Limit number of emails to process (default: 50)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run the email agent')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test email connection')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Generate sample configuration')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    if args.command == 'config':
        generate_config()
        return
    
    # Initialize agent
    try:
        agent = EmailAgent(args.config)
    except Exception as e:
        print(f"Error initializing email agent: {e}")
        return 1
    
    try:
        if args.command == 'test':
            test_connection(agent)
        elif args.command == 'run':
            run_agent(agent, args)
    finally:
        agent.disconnect()


def generate_config():
    """Generate a sample configuration file"""
    config = {
        "email": {
            "address": "your-email@example.com",
            "password": "your-app-password",
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
            }
        ],
        "auto_responses": [
            {
                "trigger": "out of office",
                "response": "Thank you for your email. I am currently out of office.",
                "enabled": False
            }
        ]
    }
    
    with open('email_config_sample.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Sample configuration generated as 'email_config_sample.json'")
    print("Please copy this to 'email_config.json' and update with your settings")


def test_connection(agent):
    """Test email server connections"""
    print("Testing IMAP connection...")
    if agent.connect_imap():
        print("✓ IMAP connection successful")
    else:
        print("✗ IMAP connection failed")
        return
    
    print("Testing SMTP connection...")
    if agent.connect_smtp():
        print("✓ SMTP connection successful")
    else:
        print("✗ SMTP connection failed")
    
    print("Connection test completed")


def run_agent(agent, args):
    """Run the email agent with specified parameters"""
    print(f"Processing emails from folder: {args.folder}")
    print(f"Limit: {args.limit} emails")
    
    if args.dry_run:
        print("DRY RUN MODE - No auto-responses will be sent")
        # Disable auto-responses for dry run
        for response in agent.config['auto_responses']:
            response['enabled'] = False
    
    agent.run_agent()


if __name__ == "__main__":
    sys.exit(main())