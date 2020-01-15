import requests
from lxml import html


# Get Release Notes Page
page = requests.get('https://winreleaseinfoprod.blob.core.windows.net/winreleaseinfoprod/en-US.html').content
root = html.fromstring(page)
# # For some reason, lxml tosses out <tbody> elements when parsing. odd.
# version = len(root.xpath("/html/body/div/table[1]")[0])
# kb_article = root.xpath("/html/body/div/table[3]/tr[2]/td[4]")[0].text_content()

# For some reason, lxml tosses out <tbody> elements when parsing. odd.
for i in range(len(root.xpath("/html/body/div/table[1]")[0]) - 2):
    release_num = root.xpath(f"/html/body/div/table[1]/tr[{i+2}]/td[1]")[0].text_content()
    if release_num == "1909":
        build_1909 = root.xpath(f"/html/body/div/table[1]/tr[{i+2}]/td[4]")[0].text_content()
        # kb_article_1909 = root.xpath(f"/html/body/div/table[3]/tr[{i+2}]/td[4]")[0].text_content()
    elif release_num == "1809":
        build_1809 = root.xpath(f"/html/body/div/table[1]/tr[{i+2}]/td[4]")[0].text_content()
        # kb_article_1809 = root.xpath(f"/html/body/div/table[3]/tr[2]/td[4]")[0].text_content()

print(f"Version: {build_1909}, {build_1809}")
