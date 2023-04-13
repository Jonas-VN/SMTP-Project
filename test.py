import dns.resolver

mx_records = dns.resolver.Resolver().resolve("gmail.com", "MX")
mx_records = sorted(mx_records, key=lambda x: x.preference)

for mx in mx_records:
    preference = mx.preference
    smtp_server = mx.exchange.to_text().rstrip('.')
    print(f"Preference: {preference}\t SMTP Server: {smtp_server}")
