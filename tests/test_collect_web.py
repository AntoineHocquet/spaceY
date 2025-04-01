# tests/test_collect_web.py

from src.collect_web import extract_column_name_from_header,fetch_html, 

def test_soup_title():
    url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"
    html = fetch_html(url)
    _, soup = parse_launch_table(html, return_soup=True)
    print(soup.title.string) # to check
    assert "Falcon 9 and Falcon Heavy launches" in soup.title.string

