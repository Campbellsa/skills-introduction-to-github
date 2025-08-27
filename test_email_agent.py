#!/usr/bin/env python3
"""
Simple tests for Email Agent functionality
"""

import unittest
import json
import tempfile
import os
from email_agent import EmailAgent


class TestEmailAgent(unittest.TestCase):
    """Test cases for EmailAgent class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_config = {
            "email": {
                "address": "test@example.com",
                "password": "test_password",
                "imap_server": "imap.example.com",
                "imap_port": 993,
                "smtp_server": "smtp.example.com",
                "smtp_port": 587
            },
            "filters": [
                {
                    "name": "Test Filter",
                    "type": "sender",
                    "criteria": ["test@test.com"],
                    "action": "priority",
                    "folder": "Test"
                },
                {
                    "name": "Marketing Filter",
                    "type": "subject",
                    "criteria": ["promotion", "sale"],
                    "action": "organize",
                    "folder": "Marketing"
                }
            ],
            "auto_responses": [
                {
                    "trigger": "urgent",
                    "response": "Received urgent message",
                    "enabled": True
                }
            ]
        }
        
        # Create temporary config file
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_config, self.temp_config)
        self.temp_config.close()
        
        self.agent = EmailAgent(self.temp_config.name)
    
    def tearDown(self):
        """Clean up test fixtures"""
        os.unlink(self.temp_config.name)
    
    def test_load_config(self):
        """Test configuration loading"""
        self.assertEqual(self.agent.config['email']['address'], 'test@example.com')
        self.assertEqual(len(self.agent.config['filters']), 2)
        self.assertEqual(len(self.agent.config['auto_responses']), 1)
    
    def test_default_config(self):
        """Test default configuration generation"""
        agent = EmailAgent('nonexistent_file.json')
        self.assertIn('email', agent.config)
        self.assertIn('filters', agent.config)
        self.assertIn('auto_responses', agent.config)
    
    def test_filter_matching_sender(self):
        """Test sender filter matching"""
        test_email = {
            'from': 'test@test.com',
            'subject': 'Test Subject',
            'to': 'recipient@example.com'
        }
        
        filter_rule = self.test_config['filters'][0]
        self.assertTrue(self.agent._matches_filter(test_email, filter_rule))
    
    def test_filter_matching_subject(self):
        """Test subject filter matching"""
        test_email = {
            'from': 'sender@example.com',
            'subject': 'Big Sale Promotion Today!',
            'to': 'recipient@example.com'
        }
        
        filter_rule = self.test_config['filters'][1]
        self.assertTrue(self.agent._matches_filter(test_email, filter_rule))
    
    def test_filter_not_matching(self):
        """Test filter not matching"""
        test_email = {
            'from': 'other@example.com',
            'subject': 'Regular Email',
            'to': 'recipient@example.com'
        }
        
        filter_rule = self.test_config['filters'][0]
        self.assertFalse(self.agent._matches_filter(test_email, filter_rule))
    
    def test_apply_filters(self):
        """Test applying filters to email list"""
        test_emails = [
            {
                'id': '1',
                'from': 'test@test.com',
                'subject': 'Important Message',
                'to': 'me@example.com'
            },
            {
                'id': '2',
                'from': 'marketing@store.com',
                'subject': 'Big Sale Today!',
                'to': 'me@example.com'
            },
            {
                'id': '3',
                'from': 'friend@example.com',
                'subject': 'Hi there',
                'to': 'me@example.com'
            }
        ]
        
        categorized = self.agent.apply_filters(test_emails)
        
        # Check that emails are properly categorized
        self.assertIn('Test', categorized)
        self.assertIn('Marketing', categorized)
        self.assertIn('uncategorized', categorized)
        
        self.assertEqual(len(categorized['Test']), 1)
        self.assertEqual(len(categorized['Marketing']), 1)
        self.assertEqual(len(categorized['uncategorized']), 1)


def run_tests():
    """Run all tests"""
    unittest.main()


if __name__ == '__main__':
    run_tests()