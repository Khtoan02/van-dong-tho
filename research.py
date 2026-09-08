from hermes_tools import web_search

def check_resource(name, queries):
    """Kiếm resource/domain cụ thể, trả kết quả có structured."""
    results = []
    for q in queries:
        r = web_search(q, limit=3)
        results.append((name, q, r.get("data", {}).get("web", [])))
    return results

if __name__ == "__main__":
    tasks = {
        "Thiết kế landing page PDF bán sản phẩm": [
            "landing page thiết kế PDF bán ebook 베트남",
            "sales pagePDF đơn giản HTML CSS mẹo enfants người Việt",
        ],
        "Ngữ cảnh phụ huynh trẻ tự kỷ": [
            "phụ huynh trẻ tự kỷ vận động thô hoạt động nhà 베트남 tài liệu",
        ],
        "Nền tảng phân phối PDF tiếng Việt": [
            "Gumroad ZaloPay Việt Nam bán PDF ebook",
        ],
        "UX CTA bán sản phẩm kỹ thuật số": [
            "digital product sales page CTA best practices",
        ],
    }
    for name, queries in tasks.items():
        for q, res in check_resource(name, queries):
            print(f"=== {name} | {q} ===")
            for item in res:
                print(f"- {item.get('title')}")
                print(f"  {item.get('url')}")
                print(f"  {item.get('description','')[:200]}")
            print()
