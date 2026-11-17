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

    parser = JRAParser()
    parser.feed(html)

    print("取得リンク数:", len(parser.links))

    action_count = 0
    srl_count = 0
    sde_count = 0

    for link in parser.links:
        onclick = link["onclick"]
        label = " ".join(link["text"])

        match = re.search(
            r"doAction\(['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]",
            onclick
        )

        if not match:
            continue

        path = match.group(1)
        cname = match.group(2)

        target_url = (
            urljoin(url, path)
            + "?CNAME="
            + quote(cname, safe="/")
        )

        action_count += 1

        if "pw01srl" in cname:
            srl_count += 1

        if "pw01sde" in cname:
            sde_count += 1

        print("\nリンク文字:", label)
        print("CNAME:", cname)
        print("取得URL:", target_url)

    print("\nJavaScriptリンク数:", action_count)
    print("開催選択リンク数:", srl_count)
    print("レース結果リンク数:", sde_count)
    print("JRAリンク調査終了")


if __name__ == "__main__":
    try:
        find_jra_actions(TEST_URL)
    except Exception as error:
        print("エラー:", error)
