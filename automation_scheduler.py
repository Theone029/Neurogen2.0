import schedule
import time
import subprocess

def run_scraper():
    subprocess.run(["scrapy", "crawl", "leads", "-o", "leads.json"], cwd="lead_scraper")

def run_email():
    subprocess.run(["python3", "email_bot.py"])

schedule.every().day.at("06:00").do(run_scraper)
schedule.every().day.at("09:00").do(run_email)

print("Automation scheduler started...")
while True:
    schedule.run_pending()
    time.sleep(60)
