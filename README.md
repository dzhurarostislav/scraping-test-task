# scraping-test-task

To run this spider you need to clone project 
```
git clone project_name
```
After this you have to install all dependencies mentioned in requirements.txt and run command into bash 
```
scrapy crawl auto_ria
```

# Automate Scrapy and Backups

# 1 Schedule Scrapy Spider:

You can use a task scheduler to run your Scrapy spider script at specific intervals. Here's an example using cron on Unix-based systems:

Open your crontab file by running:
```
crontab -e
```
Add a line to schedule your script, for example, to run it every day at 12 AM:
```
0 12 * * * /path/to/python3 /path/to/your/auto_ria_spider.py
```
Replace /path/to/python3 with the path to your Python 3 executable and /path/to/your/auto_ria_spider.py with the actual path to your Scrapy spider script.

Save and exit the crontab editor.

# 2 Schedule Daily Backup:

Similarly, you can schedule your daily backup script using cron. Add another line in your crontab file:
```
0 0 * * * /path/to/python3 /path/to/your/daily_backup.py
```
Replace /path/to/python3 and /path/to/your/daily_backup.py with the appropriate paths.


For windows users it can be done with Task Scheduler
