from datetime import datetime
dates = ['Oct  4 2022  2:38PM'
'Dec 27 2022  9:37AM',
'Jan 16 2023  8:05AM',
'Jan  3 2023  1:19PM',
'Jun  6 2023  9:28AM',
'Sep 20 2022 10:45AM',
'May 25 2023 10:13AM',
'May 30 2023  1:04PM',
'Sep 21 2022  9:55AM',
'Jan 10 2023  2:23PM',
'Mar 17 2023  8:01AM',
'Nov  8 2022 10:25AM']
formatted_dates = []
for date_string in dates:
    dt = datetime.strptime(date_string, '%b %d %Y %I:%M%p')
    formatted_dates.append(dt)
print(formatted_dates)
