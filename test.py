import mechanize

URL = "http://spa:8080?a=1"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.addheaders = [('User-Agent', USER_AGENT), ('Accept', '*/*')] 
br.open(URL)