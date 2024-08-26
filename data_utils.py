import re
from datetime import datetime,timezone
import pytz



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
  zone=pytz.timezone('US/Central')
  for course in data:
      course['time_updated'] = datetime.now(zone).strftime("%Y-%m-%d %H:%M:%S")
  return data

def time_difference(data):
  zone=pytz.timezone('US/Central')
  for course in data:
      time_updated = zone.localize(datetime.strptime(course['time_updated'], "%Y-%m-%d %H:%M:%S"))
      current_time = datetime.now(zone)
      time_difference = current_time - time_updated
      if(time_difference.total_seconds() > 60):
          minutes = int(time_difference.total_seconds()/60)
          if(minutes > 60):
              hours = int(minutes/60)
              if(hours > 24):
                  days = int(hours/24)
                  if days > 1:
                      course['time_difference'] = str(days)+" days"
                  else:
                      course['time_difference'] = str(days)+" day"
              elif hours > 1:
                  course['time_difference'] = str(hours)+" hours"
              else:
                course['time_difference'] = str(hours)+" hour"
          else:
              course['time_difference'] = str(minutes)+" minutes"
      else:
        course['time_difference'] = str(int(time_difference.total_seconds()))+" seconds"
  return data

def clean_dept_name(data):
  for course in data:
      course['department'] = course['department'].replace(" ", "_").lower()
      course['name'] = course['name'].replace(" ", "_").lower()
  return data