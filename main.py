import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin


JRA_URLS = [
    "https://www.jra.go.jp/",
    "https://www.jra.go.jp/keiba/",
]


class JRAParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return

        for name, value in attrs:
            if name.lower() == "href" and value:
                self.links.append(value)


def get_page(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
)

    with urllib.request.urlopen(request, timeout=20) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def find_result_links(url):
    print("\n確認ページ:", url)

    html = get_page(url)
    parser = JRAParser()
    parser.feed(html)

    found = set()

    for link in parser.links:
        full_url = urljoin(url, link)

        if "accessS.html" in full_url or "pw01sde" in full_url:
            found.add(full_url)

    if found:
        for result_url in sorted(found):
            print("レース結果候補:", result_url)
    else:
        print("このページから直接のレース結果リンクは見つかりませんでした。")

    return found


if __name__ == "__main__":
    print("JRA公式リンク取得テスト開始")

    all_links = set()

    for url in JRA_URLS:
        try:
            all_links.update(find_result_links(url))
        except Exception as error:
            print("取得エラー:", error)

    print("\n取得できた結果リンク数:", len(all_links))
    print("JRA公式リンク取得テスト終了")
