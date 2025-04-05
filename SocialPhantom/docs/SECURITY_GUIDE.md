# SocialPhantom Security Best Practices Guide

## Ethical Usage Policy
1. **Explicit Consent Required**: Always obtain written permission before testing
2. **Scope Definition**: Clearly define testing boundaries in writing
3. **Data Handling**: Never collect or store real user credentials
4. **Legal Compliance**: Adhere to all applicable laws (GDPR, CFAA, etc.)

## Secure Deployment
### Environment Configuration
- Use dedicated testing infrastructure
- Isolate network segments for testing
- Implement strict access controls
- Enable full logging and monitoring

### Credential Management
- Use unique, disposable test accounts
- Never reuse production credentials
- Rotate API keys and SMTP passwords regularly
- Store secrets in environment variables (never in code)

## Testing Guidelines
### Email Campaigns
#### Phishing:
- Clearly mark test emails with "[SECURITY TEST]" prefix
- Include opt-out instructions in all communications
- Limit test frequency to avoid spam filters
- Monitor for unintended propagation

#### BEC (Business Email Compromise):
- Use obvious test amounts (e.g., $123,456.78)
- Only use test bank account numbers
- Clearly indicate spoofed sender addresses are simulations
- Include multiple verification steps for wire transfers
- Implement secondary confirmation for sensitive actions

### Website Cloning
- Respect robots.txt directives
- Avoid overloading target servers
- Never clone financial or government sites without explicit authorization
- Include visible "TESTING ONLY" watermarks on cloned pages

## Incident Response
1. **Immediate Termination**: Stop all testing if unintended access occurs
2. **Documentation**: Record all actions taken during the incident
3. **Notification**: Inform affected parties immediately
4. **Remediation**: Assist with mitigation efforts

## Audit & Compliance
- Maintain detailed testing logs including:
  - All BEC simulation parameters
  - Wire transfer test details
  - Spoofed sender information
- Conduct regular tool reviews with legal counsel
- Perform penetration tests on the tester
- Document all security controls
- Retain signed consent forms for BEC tests

## Disclaimers
```plaintext
THIS TOOL IS PROVIDED FOR AUTHORIZED SECURITY TESTING ONLY. 
UNAUTHORIZED USE MAY VIOLATE LOCAL AND INTERNATIONAL LAWS. 
USERS ASSUME ALL LEGAL LIABILITY FOR IMPROPER USE.
