import requests
import hashlib
import sys

def display_header():
    print("  ____  ____   ____  _   _  ____ ")
    print(" / __ \\/ ___| / ___|| | | ||  _ \\")
    print("| |  | \\___ \\| |    | |_| || |_) |")
    print("| |__| |___) | |___ |  _  ||  _ < ")
    print(" \\____/|____/ \\____||_| |_||_| \\_\\")
    print("                                  ")
    print("       O S I N T : User Information Gatherer      ")
    print("         Scan Public Information ---\n")

def check_username_on_social_media(username):
    print(f"\n[+] Checking username '{username}' on social media platforms...")
    platforms = {
        "Instagram": f"https://www.instagram.com/{username}/",
        "Twitter": f"https://twitter.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}/",
        "LinkedIn (Public Profile)": f"https://www.linkedin.com/in/{username}/"
    }
    
    found_any = False
    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"  [+] Found on {platform}: {url}")
                found_any = True
            elif response.status_code == 404:
                print(f"  [i] Not found on {platform}")
            else:
                print(f"  [!] Could not verify {platform} (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"  [!] Error checking {platform}: {e}")
    
    if not found_any:
        print(f"  [i] Username '{username}' not found on checked platforms or errors occurred.")

def check_email_for_breaches(email):
    print(f"\n[+] Checking email '{email}' for data breaches via Have I Been Pwned...")
    hibp_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {'User-Agent': 'OSINT_Tool'}

    try:
        response = requests.get(hibp_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            breaches = response.json()
            print(f"  [!] Email '{email}' found in the following data breaches:")
            for breach in breaches:
                print(f"    - {breach.get('Title')} (Date: {breach.get('BreachDate')}, Domain: {breach.get('Domain')})")
                print(f"      Description: {breach.get('Description')[:100]}...")
            print("  [!] Consider changing your password for accounts associated with this email.")
        elif response.status_code == 404:
            print(f"  [+] Good news! Email '{email}' not found in any known data breaches.")
        elif response.status_code == 400:
             print(f"  [!] Bad request to HIBP API (Status 400). Please check the email format: {email}")
        else:
            print(f"  [!] HIBP API error (Status: {response.status_code}). Please try again later.")
            if response.status_code == 403:
                print("      Note: HIBP API might be rate-limiting requests or requires an API key for more queries.")

    except requests.exceptions.RequestException as e:
        print(f"  [!] Error connecting to HIBP API: {e}")
    except Exception as e:
        print(f"  [!] An unexpected error occurred during email breach check: {e}")

def main():
    display_header()

    while True:
        choice = input("Enter 'u' for username check, 'e' for email check, or 'q' to quit: ").strip().lower()
        
        if choice == 'q':
            break
        elif choice == 'u':
            username = input("Enter username to search: ").strip()
            if username:
                check_username_on_social_media(username)
            else:
                print("[!] Username cannot be empty.")
        elif choice == 'e':
            email = input("Enter email address to check for breaches: ").strip()
            if email:
                check_email_for_breaches(email)
            else:
                print("[!] Email cannot be empty.")
        else:
            print("[!] Invalid choice. Please enter 'u', 'e', or 'q'.")
        
        print("\n" + "-"*60 + "\n")

    print("[+] OSINT Tool finished. Goodbye!")

if __name__ == '__main__':
    main()