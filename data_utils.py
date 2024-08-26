import re
from datetime import datetime


def seats_scraper(data):
  pattern = r"(\d+) of \d+ seats remain\.|FULL: 0 of \d+ seats remain\."
  for course in data:
    availability = course['availability']
    match = re.search(pattern, availability)
    if match:
        if "FULL" in availability:
            seats = 0  # If full, seats remaining is 0
        else:
            seats = match.group(1)
        course['seats'] = int(seats)
    else:
        course['seats'] = 0

  return data

def updated_time(data):
  for course in data:
      course['time_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  return data

def time_difference(data):
  for course in data:
      time_updated = datetime.strptime(course['time_updated'], "%Y-%m-%d %H:%M:%S")
      time_difference = datetime.now() - time_updated
      course['time_difference'] = str(int(time_difference.total_seconds()))+" seconds"
  return data

def clean_dept_name(data):
  for course in data:
      course['department'] = course['department'].replace(" ", "_").lower()
      course['name'] = course['name'].replace(" ", "_").lower()
  return data