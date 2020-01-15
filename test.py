import requests
from lxml import html


# Get Release Notes Page
page = requests.get('https://winreleaseinfoprod.blob.core.windows.net/winreleaseinfoprod/en-US.html').content
root = html.fromstring(page)
# For some reason, lxml tosses out <tbody> elements when parsing. odd.
version = root.xpath("/html/body/div/table[1]/tr[2]/td[4]")[0].text_content()
kb_article = root.xpath("/html/body/div/table[3]/tr[2]/td[4]")[0].text_content()

print(f"Version: {version}, {kb_article}")
