# SocialPhantom Troubleshooting Guide

## Common Issues & Solutions

### Email Delivery Problems
**Symptoms**:
- Emails not reaching inbox
- SMTP connection errors
- Authentication failures

**Solutions**:
1. Verify SMTP settings in `config/email_config.json`
2. Test SMTP connection manually:
```bash
python -c "import smtplib; smtplib.SMTP_SSL('smtp.example.com', 465).ehlo()"
```
3. Check spam/junk folders
4. Verify firewall rules allow outbound SMTP

### Website Cloning Failures
**Symptoms**:
- Incomplete page cloning
- Missing assets
- 403 Forbidden errors

**Solutions**:
1. Check target site's robots.txt
2. Verify network connectivity
3. Try different user-agent strings
4. Adjust request throttling in `web_cloner.py`

### Campaign Tracking Issues
**Symptoms**:
- No click tracking data
- Missing campaign statistics
- Incomplete reports

**Solutions**:
1. Verify tracking server is running
2. Check campaign name consistency
3. Inspect browser console for JavaScript errors
4. Validate database connection

## Debugging Techniques

### Log Analysis
- Review `socialphantom.log` for errors
- Enable verbose logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Network Troubleshooting
1. Verify DNS resolution
2. Test connectivity to target services
3. Check proxy settings if applicable

### Performance Optimization
1. Adjust thread counts in `EmailSender` and `WebCloner`
2. Implement request throttling
3. Optimize database queries

## Common Error Messages

### "SMTP Authentication Error"
- Verify username/password
- Check if SMTP server requires app password
- Test credentials with email client

### "Invalid Template Variables"
- Ensure all template placeholders are provided
- Check for typos in variable names
- Validate template file encoding

### "Campaign Not Found"
- Verify campaign exists in `campaigns/` directory
- Check for case sensitivity issues
- Validate campaign configuration file

## Getting Support
For additional help:
1. Check GitHub issues
2. Review API documentation
3. Contact: support@socialphantom.example.com
