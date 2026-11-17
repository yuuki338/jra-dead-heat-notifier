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
        self.current_link = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self.current_link = {
                "href": "",
                "text": []
            }

            for name, value in attrs:
                if name.lower() == "href" and value:
                    self.current_link["href"] = value

                if name.lower() in ("alt", "title") and value:
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
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(
            charset,
            errors="replace"
        )


def find_result_links(url):
    print("\n確認ページ:", url)

    html = get_page(url)

    parser = JRAParser()
    parser.feed(html)

    print("取得したリンク総数:", len(parser.links))
    
    print("\nリンク内容の確認:")

    for link in parser.links[:20]:
        print("文字:", " ".join(link["text"]))
        print("URL:", urljoin(url, link["href"]))
        keywords = [
        "レース結果",
        "過去のレース結果",
        "開催情報",
        "出馬表"
    ]

    found = 0

    for link in parser.links:
        href = link["href"]
        label = " ".join(link["text"])

        full_url = urljoin(url, href)

        if any(word in label for word in keywords):
            print("\nリンク文字:", label)
            print("リンクURL:", full_url)
            found += 1

        elif "JRADB" in full_url or "pw01sde" in full_url:
            print("\n結果ページ候補:", full_url)
            found += 1

    print("\n今回見つかった候補数:", found)


if __name__ == "__main__":
    print("JRAリンク詳細取得テスト開始")

    for url in JRA_URLS:
        try:
            find_result_links(url)
        except Exception as error:
            print("\n取得エラー:", error)

    print("\nJRAリンク詳細取得テスト終了")
