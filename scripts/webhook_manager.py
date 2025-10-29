#!/usr/bin/env python3
"""
Telegram Webhook Manager
Utility to manage webhook configuration for your Telegram bot
"""

import os
import sys
import requests
from dotenv import load_dotenv


def get_token():
    """Get bot token from environment"""
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file")
        sys.exit(1)
    return token


def get_webhook_info(token):
    """Get current webhook information"""
    url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    response = requests.get(url)
    return response.json()


def set_webhook(token, webhook_url):
    """Set webhook URL"""
    url = f"https://api.telegram.org/bot{token}/setWebhook"
    response = requests.post(url, json={"url": webhook_url})
    return response.json()


def delete_webhook(token):
    """Delete webhook (return to polling mode)"""
    url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    response = requests.post(url)
    return response.json()


def print_webhook_info(info):
    """Pretty print webhook information"""
    result = info.get('result', {})
    
    print("\n📊 Current Webhook Status:")
    print("=" * 60)
    print(f"URL: {result.get('url', 'Not set')}")
    print(f"Has Custom Certificate: {result.get('has_custom_certificate', False)}")
    print(f"Pending Update Count: {result.get('pending_update_count', 0)}")
    
    if result.get('last_error_date'):
        from datetime import datetime
        error_date = datetime.fromtimestamp(result['last_error_date'])
        print(f"\n⚠️  Last Error Date: {error_date}")
        print(f"Last Error Message: {result.get('last_error_message', 'N/A')}")
    
    if result.get('max_connections'):
        print(f"\nMax Connections: {result.get('max_connections')}")
    
    if result.get('allowed_updates'):
        print(f"Allowed Updates: {', '.join(result.get('allowed_updates'))}")
    
    print("=" * 60)


def main():
    """Main function"""
    print("\n🤖 Telegram Bot Webhook Manager")
    print("=" * 60)
    
    token = get_token()
    
    while True:
        print("\nOptions:")
        print("1. Get webhook info")
        print("2. Set webhook URL")
        print("3. Delete webhook (switch to polling)")
        print("4. Test webhook with ngrok")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            print("\n🔍 Fetching webhook info...")
            info = get_webhook_info(token)
            print_webhook_info(info)
            
        elif choice == "2":
            webhook_url = input("\nEnter webhook URL (with https://): ").strip()
            if not webhook_url.startswith("https://"):
                print("❌ Error: Webhook URL must start with https://")
                continue
            
            # Add /webhook if not present
            if not webhook_url.endswith("/webhook"):
                webhook_url = f"{webhook_url}/webhook"
            
            print(f"\n🔧 Setting webhook to: {webhook_url}")
            result = set_webhook(token, webhook_url)
            
            if result.get('ok'):
                print("✅ Webhook set successfully!")
                print(f"Description: {result.get('description', 'N/A')}")
            else:
                print(f"❌ Error: {result.get('description', 'Unknown error')}")
            
        elif choice == "3":
            confirm = input("\n⚠️  This will delete the webhook. Continue? (yes/no): ")
            if confirm.lower() in ['yes', 'y']:
                print("\n🗑️  Deleting webhook...")
                result = delete_webhook(token)
                
                if result.get('ok'):
                    print("✅ Webhook deleted successfully!")
                    print("Your bot is now in polling mode.")
                else:
                    print(f"❌ Error: {result.get('description', 'Unknown error')}")
        
        elif choice == "4":
            print("\n🔗 ngrok Setup Instructions:")
            print("=" * 60)
            print("1. Install ngrok: brew install ngrok")
            print("2. Start your bot on port 8443")
            print("3. In another terminal, run: ngrok http 8443")
            print("4. Copy the HTTPS URL from ngrok (e.g., https://abc123.ngrok.io)")
            print("5. Come back here and select option 2 to set that URL")
            print("=" * 60)
            input("\nPress Enter to continue...")
        
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option. Please select 1-5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

