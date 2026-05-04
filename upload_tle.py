from config import Config
from skyfield.api import utc
from datetime import datetime, timedelta

date = datetime(2025, 9, 17, 16, 39, 39, tzinfo=utc) - timedelta(hours=2)

str_date_inf = date.strftime('%y-%m-%d')
str_date_sup = (date + timedelta(days=1.)).strftime('%y-%m-%d')

query_url = f'https://www.space-track.org/basicspacedata/query/class/gp_history/NORAD_CAT_ID/{Config.NORAD_ID}/EPOCH/%3E{str_date_inf}%2C%3C{str_date_sup}/orderby/EPOCH%20asc/format/tle/emptyresult/show'

print(query_url)