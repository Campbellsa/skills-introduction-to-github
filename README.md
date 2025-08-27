<div align="center">

# 📧 Email Inbox Agent

<img src="https://octodex.github.com/images/welcometocat.png" height="200px" />

### 🤖 Intelligent Email Filtering and Automated Response System 🤖

## ✨ Features

- **Smart Email Filtering**: Automatically categorize emails by sender, subject, or domain
- **Automated Responses**: Send intelligent auto-replies based on email content
- **Multiple Filter Types**: Support for sender, subject, and domain-based filtering
- **Configurable Rules**: Easy JSON-based configuration for filters and responses
- **CLI Interface**: Command-line tool for easy automation and scripting
- **Dry Run Mode**: Test filters without sending actual responses
- **Logging**: Comprehensive logging for monitoring and debugging

## 🚀 Quick Start

1. **Install Python 3.7+** (no external dependencies required)

2. **Generate configuration**:
   ```bash
   python3 email_cli.py config
   ```

3. **Configure your email settings** in `email_config.json`:
   ```json
   {
     "email": {
       "address": "your-email@gmail.com",
       "password": "your-app-password",
       "imap_server": "imap.gmail.com",
       "smtp_server": "smtp.gmail.com"
     }
   }
   ```

4. **Test connection**:
   ```bash
   python3 email_cli.py test
   ```

5. **Run the agent**:
   ```bash
   python3 email_cli.py run --dry-run
   ```

## 📖 Usage

### Command Line Interface

```bash
# Run with dry-run (no auto-responses sent)
python3 email_cli.py run --dry-run

# Process specific folder
python3 email_cli.py run --folder "INBOX" --limit 100

# Test email connection
python3 email_cli.py test

# Generate sample configuration
python3 email_cli.py config
```

### Python API

```python
from email_agent import EmailAgent

# Initialize agent
agent = EmailAgent('email_config.json')

# Run filtering and auto-responses
agent.run_agent()

# Clean up
agent.disconnect()
```

## ⚙️ Configuration

The agent uses a JSON configuration file with three main sections:

### Email Settings
```json
{
  "email": {
    "address": "your-email@example.com",
    "password": "your-app-password",
    "imap_server": "imap.gmail.com",
    "imap_port": 993,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
  }
}
```

### Filter Rules
```json
{
  "filters": [
    {
      "name": "Important Senders",
      "type": "sender",
      "criteria": ["boss@company.com", "client@important.com"],
      "action": "priority",
      "folder": "Important"
    }
  ]
}
```

### Auto-Response Rules
```json
{
  "auto_responses": [
    {
      "trigger": "out of office",
      "response": "Thank you for your email. I am currently out of office.",
      "enabled": false
    }
  ]
}
```

## 🧪 Testing

Run the test suite to validate functionality:

```bash
python3 test_email_agent.py
```

## 🔒 Security Notes

- Use app-specific passwords for Gmail accounts
- Never commit email credentials to version control
- Consider using environment variables for sensitive configuration
- Test with dry-run mode before enabling auto-responses

## 📝 Examples

### Marketing Email Filter
```json
{
  "name": "Marketing",
  "type": "subject", 
  "criteria": ["unsubscribe", "promotion", "sale", "deal"],
  "action": "organize",
  "folder": "Marketing"
}
```

### Domain-based Social Media Filter
```json
{
  "name": "Social Media",
  "type": "sender_domain",
  "criteria": ["facebook.com", "twitter.com", "linkedin.com"],
  "action": "organize", 
  "folder": "Social"
}
```

### Out of Office Auto-Response
```json
{
  "trigger": "urgent",
  "response": "I have received your urgent message and will prioritize a response.",
  "enabled": true
}
```

## 🎯 Built with GitHub Skills

This email agent was built as part of the GitHub Skills learning experience!

[![](https://img.shields.io/badge/Return%20to%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/Campbellsa/skills-introduction-to-github/issues/1)
[![GitHub Skills](https://img.shields.io/badge/Explore%20GitHub%20Skills-000000?style=for-the-badge&logo=github&logoColor=white)](https://learn.github.com/skills))

## 🚀 Share Your Success!

**Show off your new email automation skills!**

<a href="https://twitter.com/intent/tweet?text=I%20just%20built%20an%20Email%20Inbox%20Agent%20with%20automated%20filtering%20and%20responses!%20%F0%9F%93%A7%F0%9F%A4%96%0A%0Ahttps%3A%2F%2Fgithub.com%2FCampbellsa%2Fskills-introduction-to-github%0A%0A%23EmailAutomation%20%23Python%20%23GitHubSkills" target="_blank" rel="noopener noreferrer">
  <img src="https://img.shields.io/badge/Share%20on%20X-1da1f2?style=for-the-badge&logo=x&logoColor=white" alt="Share on X" />
</a>
<a href="https://bsky.app/intent/compose?text=I%20just%20built%20an%20Email%20Inbox%20Agent%20with%20automated%20filtering%20and%20responses!%20%F0%9F%93%A7%F0%9F%A4%96%0A%0Ahttps%3A%2F%2Fgithub.com%2FCampbellsa%2Fskills-introduction-to-github%0A%0A%23EmailAutomation%20%23Python%20%23GitHubSkills" target="_blank" rel="noopener noreferrer">
  <img src="https://img.shields.io/badge/Share%20on%20Bluesky-0085ff?style=for-the-badge&logo=bluesky&logoColor=white" alt="Share on Bluesky" />
</a>
<a href="https://www.linkedin.com/feed/?shareActive=true&text=I%20just%20built%20an%20Email%20Inbox%20Agent%20with%20automated%20filtering%20and%20responses!%20%F0%9F%93%A7%F0%9F%A4%96%0A%0Ahttps%3A%2F%2Fgithub.com%2FCampbellsa%2Fskills-introduction-to-github%0A%0A%23EmailAutomation%20%23Python%20%23GitHubSkills" target="_blank" rel="noopener noreferrer">
  <img src="https://img.shields.io/badge/Share%20on%20LinkedIn-0077b5?style=for-the-badge&logo=linkedin&logoColor=white" alt="Share on LinkedIn" />
</a>

</div>

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

