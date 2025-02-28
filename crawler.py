import requests
import mysql.connector
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Database connection details
DB_HOST = "localhost"
DB_DATABASE = "news"
DB_USERNAME = "root"
DB_PASSWORD = ""

def get_db_connection():
    """Establishes connection to MySQL database"""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

def create_table():
    """Creates a table for storing news articles if it does not exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS NewsArticles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            headline VARCHAR(500) NOT NULL,
            link VARCHAR(1000) NOT NULL,
            summary TEXT,
            source VARCHAR(255) NOT NULL,
            scrape_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def insert_news(headline, link, summary, source):
    """Inserts news data into the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO NewsArticles (headline, link, summary, source)
        VALUES (%s, %s, %s, %s)
    """, (headline, link, summary, source))
    
    conn.commit()
    conn.close()

def get_news_headlines(url, selector, keywords, countries, paragraph_selector="p"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': url
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.select(selector)
        
        for item in headlines:
            text = item.get_text(strip=True)
            link = item.find_parent("a")
            href = urljoin(url, link['href']) if link and 'href' in link.attrs else url
            
            if any(k.lower() in text.lower() for k in keywords + countries):
                paragraph = get_article_paragraph(href, paragraph_selector)
                insert_news(text, href, paragraph, url)  # Save to MySQL
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from {url}: {e}")

def get_article_paragraph(article_url, paragraph_selector="p"):
    """Fetches the first paragraph from the news article."""
    try:
        response = requests.get(article_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraph = soup.select_one(paragraph_selector)
        
        return paragraph.get_text(strip=True) if paragraph else "No content extracted"
    
    except requests.exceptions.RequestException:
        return "Could not fetch article content"

if __name__ == "__main__":
    create_table()  # Ensure the table exists
    
    news_sites = [
        {"url": "https://www.bbc.com/news", "selector": "h3"},
        {"url": "https://thehackernews.com/", "selector": "h2"},
        {"url": "https://www.cnn.com/world", "selector": "h2"},
        {"url": "https://www.securityweek.com/", "selector": ".article-title a"},
        {"url": "https://www.bleepingcomputer.com/", "selector": "h2 a"},
        {"url": "https://www.darkreading.com/", "selector": "h3 a"},
        {"url": "https://threatpost.com/", "selector": "h2 a"}
       
       
       
    ]
    
    keywords = [
        "cyber", "cyber attack", "hacking", "APT", "Spear Phishing", "Whaling Attack", "Smishing SMS Phishing",
        "Vishing Voice Phishing", "Clone Phishing", "Angler Phishing", "Business Email Compromise BEC", "Evil Twin Attack",
        "Social Engineering", "Credential Harvesting", "Keylogging", "Man-in-the-Middle MitM Attack",
        "Credential Stuffing", "Brute Force Attack", "Spoofing Email, Caller ID, IP", "DNS Poisoning",
        "Session Hijacking", "URL Obfuscation", "Cross-Site Scripting XSS", "SQL Injection SQLi",
        "Multi-Factor Authentication MFA", "Anti-Phishing Solutions", "Email Filtering", "Sandboxing",
        "Security Awareness Training", "Threat Intelligence", "Incident Response","Cybersecurity", "Threat Actor",
        "Zero-Day Exploit", "Ransomware", "Malware", "Trojan Horse", "Spyware",
        "Adware", "Rootkit", "Worm", "Botnet", "Command and Control C2", "Exploit Kit", "Drive-By Download",
        "Malvertising", "Fileless Malware", "Polymorphic Malware", "Crimeware", "Cyber Espionage", "Data Breach",
        "Identity Theft", "Insider Threat", "Advanced Persistent Threat APT", "Dark Web", "Deep Web",
        "Phishing Kit", "Malicious Payload", "Exploit Chain", "Payload Delivery", "Threat Hunting",
        "Security Operations Center SOC", "Endpoint Detection and Response EDR", "Intrusion Detection System IDS",
        "Intrusion Prevention System IPS", "Firewall", "Next-Generation Firewall NGFW", "Virtual Private Network VPN",
        "Secure Sockets Layer SSL", "Transport Layer Security TLS", "Public Key Infrastructure PKI",
        "Digital Certificate", "Certificate Authority CA", "Privileged Access Management PAM", "Data Loss Prevention DLP",
        "Behavioral Analytics", "User Entity Behavior Analytics UEBA", "Security Information and Event Management SIEM",
        "Cyber Kill Chain", "MITRE ATT&CK Framework", "Cyber Threat Intelligence CTI", "Tactics Techniques and Procedures TTP",
        "Indicators of Compromise IoC", "Indicators of Attack IoA", "Threat Intelligence Platform TIP",
        "Data Encryption", "End-to-End Encryption", "Homomorphic Encryption", "Steganography", "Cryptography",
        "Symmetric Encryption", "Asymmetric Encryption", "RSA Algorithm", "Elliptic Curve Cryptography ECC",
        "Diffie-Hellman Key Exchange", "Quantum Cryptography", "Blockchain Security", "Cyber Resilience",
        "Security Policy", "Access Control", "Role-Based Access Control RBAC", "Discretionary Access Control DAC",
        "Mandatory Access Control MAC", "Multi-Layered Security", "Zero Trust Architecture", "Least Privilege Principle",
        "Network Segmentation", "Microsegmentation", "Security Token", "One-Time Password OTP", "Password Hashing",
        "Salting", "Hash Function", "SHA-256", "MD5", "HMAC", "Kerberos Authentication", "OAuth 2.0", "SAML",
        "OpenID Connect OIDC", "Identity and Access Management IAM", "Single Sign-On SSO", "Federated Identity",
        "Cloud Security", "Container Security", "Serverless Security", "DevSecOps", "Security Hardening",
        "Patch Management", "Software Bill of Materials SBOM", "Code Injection", "Command Injection",
        "Remote Code Execution RCE", "Privilege Escalation", "Side-Channel Attack", "Cold Boot Attack","CERT"
    ]
    
    countries = ["China", "Pakistan", "Russia", "Korea","India","United States", "United Kingdom", "Germany", "France", "Japan", "Canada", "Australia", "Brazil", "South Africa", "Italy",
                "Spain", "Mexico", "Argentina", "Turkey", "Iran", "Saudi Arabia", "United Arab Emirates", "Israel", "Egypt", "Indonesia",
                "Malaysia", "Thailand", "Vietnam", "Philippines", "Singapore", "Bangladesh", "Sri Lanka", "Afghanistan", "Kazakhstan", "Uzbekistan",
                "Ukraine", "Belarus", "Poland", "Sweden", "Norway", "Denmark", "Finland", "Greece", "Portugal", "Netherlands",
                "Belgium", "Switzerland", "Austria", "Czech Republic", "Hungary", "Romania", "Serbia", "South Sudan", "Nigeria", "Colombia"
]
    
    for site in news_sites:
        get_news_headlines(site['url'], site['selector'], keywords, countries)

    print("Filtered news headlines saved to MySQL database.")
