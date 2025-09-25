# Security Guidelines

This document outlines security best practices for using and contributing to the Proposal Generator.

## API Key Protection

### **CRITICAL: Never Commit API Keys**

OpenAI API keys are sensitive credentials that must never be committed to version control.

### **Best Practices for API Key Management**

1. **Use Environment Variables (Recommended)**
   ```bash
   export OPENAI_API_KEY='sk-your-key-here'
   ```

2. **Use .env Files (Local Development)**
   ```bash
   # Create .env file in project root
   echo "OPENAI_API_KEY=sk-your-key-here" > .env
   ```

3. **Production Deployment**
   - Use secure environment variable management
   - Consider using secrets management services (AWS Secrets Manager, Azure Key Vault, etc.)
   - Never hardcode keys in source code
   - Rotate keys regularly

### **Key Security Features**

The project includes multiple layers of protection:

1. **.gitignore Protection**
   ```
   # API Keys and secrets
   .env
   .env.*
   *.key
   *sk-proj-*
   *openai*key*
   secrets.json
   config.json
   ```

2. **Runtime Validation**
   - API keys are validated before use
   - Clear error messages when keys are missing
   - No key logging or exposure in error messages

3. **Pattern Detection**
   - Git hooks can detect common key patterns
   - Automated scanning for exposed credentials

## Emergency Response

### **If You Accidentally Commit an API Key**

1. **Immediately revoke the key**
   - Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Delete the exposed key immediately

2. **Generate a new key**
   - Create a replacement key
   - Update your local environment

3. **Clean Git history (if needed)**
   ```bash
   # Remove from recent commit
   git filter-branch --index-filter 'git rm --cached --ignore-unmatch .env' HEAD

   # Force push (use with caution)
   git push --force-with-lease
   ```

4. **Monitor your OpenAI account**
   - Check usage logs for unauthorized access
   - Enable billing alerts

## Development Security

### **Local Development**

1. **Never share .env files**
   - Each developer should have their own API key
   - Include .env.example with dummy values

2. **Use separate keys for different environments**
   - Development keys with usage limits
   - Production keys with appropriate permissions

3. **Regular key rotation**
   - Rotate development keys monthly
   - Rotate production keys quarterly

### **Testing Security**

1. **Mock API calls in tests**
   - Don't use real API keys in automated tests
   - Use mock responses for predictable testing

2. **Sanitize logs**
   - Never log API keys or responses
   - Redact sensitive information from debug output

## Input Validation

### **Transcript Content**

While transcripts may contain sensitive business information:

1. **No persistent storage**
   - Transcripts are processed in memory only
   - No automatic caching of input content

2. **Output sanitization**
   - Generated proposals don't expose raw API responses
   - Sensitive information handling depends on your use case

3. **Data handling recommendations**
   - Review generated proposals before sharing
   - Consider data classification requirements
   - Implement appropriate access controls

## Reporting Security Issues

### **Vulnerability Reporting**

If you discover a security vulnerability:

1. **Do NOT open a public issue**
2. **Contact maintainers privately**
3. **Provide detailed reproduction steps**
4. **Allow time for responsible disclosure**

### **Security Contact**

- Report security issues through GitHub Security Advisories
- For urgent matters, contact repository maintainers directly

## Compliance Considerations

### **Data Processing**

- **Input data**: Discovery call transcripts may contain confidential business information
- **AI processing**: Content is sent to OpenAI's API - review OpenAI's privacy policy
- **Output data**: Generated proposals may contain derived business insights

### **Recommendations**

1. **Review OpenAI's Terms of Service**
   - Understand data processing policies
   - Ensure compliance with your organization's requirements

2. **Implement appropriate controls**
   - Data classification
   - Access logging
   - Retention policies

3. **Consider regulatory requirements**
   - GDPR, CCPA, or other privacy regulations
   - Industry-specific compliance (HIPAA, SOX, etc.)

## Security Checklist

### **Before Deployment**

- [ ] API keys stored securely (not in code)
- [ ] .gitignore configured properly
- [ ] No sensitive data in commit history
- [ ] Environment variables configured
- [ ] Access controls implemented
- [ ] Monitoring and alerting configured

### **Regular Security Tasks**

- [ ] Rotate API keys quarterly
- [ ] Review access logs monthly
- [ ] Update dependencies regularly
- [ ] Monitor for security advisories
- [ ] Audit .gitignore effectiveness

## Additional Resources

- [OpenAI API Security Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Git Security Documentation](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)
- [Environment Variable Security](https://12factor.net/config)

---

**Remember: Security is a shared responsibility. Every contributor and user plays a role in keeping the project and its users secure.**