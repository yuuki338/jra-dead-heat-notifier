
import urllib.request
from html.parser import HTMLParser


class JRAParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name.lower() in ("alt", "title") and value:
                self.text.append(value)

    def handle_data(self, data):
        if data.strip():
            self.text.append(data.strip())

def check_jra_result(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        charset = response.headers.get_content_charset() or "shift_jis"
        html = response.read().decode(charset, errors="replace")
    
    parser = JRAParser()
    parser.feed(html)

    page_text = " ".join(parser.text)

    if "同着" in page_text:
        print("ページ内に「同着」の文字を確認しました。")
    else:
        print("ページ内に「同着」の文字は見つかりませんでした。")


if __name__ == "__main__":
    print("JRA公式ページ読み取りテスト")
    check_jra_result(
        "https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202605020820261108/7F"
    )
