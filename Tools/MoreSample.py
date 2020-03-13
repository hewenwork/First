import requests_html

url = "http://blueskycloud.ys168.com/"
response = requests_html.HTMLSession().get(url)
print(response.html.find("li > a"))