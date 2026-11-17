import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, quote
import re


TEST_URL = (
    "https://www.jra.go.jp/JRADB/accessS.html"
    "?CNAME=pw01sde1008202605031120261114/B7"
)


class JRAParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_link = None

def handle_starttag(self, tag, attrs):
    if tag.lower() == "a":
        self.current_link = {
            "href": "",
            "onclick": "",
            "text": []
        }

    if self.current_link:
        for name, value in attrs:
            if not value:
                continue

            if name.lower() == "href":
                self.current_link["href"] = value

            elif name.lower() == "onclick":
                self.current_link["onclick"] = value

            elif name.lower() in ("alt", "title"):
                self.current_link["text"].append(value)

    def handle_data(self, data):
        if self.current_link and data.strip():
            self.current_link["text"].append(data.strip())

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self.current_link:
            self.links.append(self.current_link)
            self.current_link = None


def get_page(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        charset = response.headers.get_content_charset() or "shift_jis"
        return response.read().decode(
            charset,
            errors="replace"
        )


def find_jra_actions(url):
    print("JRA公式ページ取得開始")

    html = get_page(url)

    matches = re.findall(
        r"doAction\(['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]",
        html
    )

    print("取得リンク数:", len(matches))

    result_count = 0

    for path, cname in matches:
        if "accessS.html" in path:
            target_url = (
                urljoin(url, path)
                + "?CNAME="
                + quote(cname, safe="/")
            )

            print("レース結果リンク:", cname)
            print("取得URL:", target_url)

            result_count += 1

    print("レース結果リンク数:", result_count)
    print("JRAリンク調査終了")

if __name__ == "__main__":
    try:
        find_jra_actions(TEST_URL)
    except Exception as error:
        print("エラー:", error)
