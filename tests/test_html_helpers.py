# tests/test_html_helpers.py

import pytest
from bs4 import BeautifulSoup
from src.collect_web import extract_column_name_from_header, extract_table_headers, fetch_html

def test_soup_title():
    url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"
    html = fetch_html(url)
    _, soup = extract_table_headers(html, return_soup=True)
    print(soup.title.string) # to check
    assert "Falcon 9 and Falcon Heavy launches" in soup.title.string


def test_extract_column_from_header_removes_tags():
    html = "<th>Rocket<sup>1</sup><br><a href='#'>link</a></th>"
    row = BeautifulSoup(html, "html.parser").th
    assert extract_column_name_from_header(row) == "Rocket"


def test_extract_column_from_header_ignores_digits():
    html = "<th>123</th>"
    row = BeautifulSoup(html, "html.parser").th
    assert extract_column_name_from_header(row) is None


def test_extract_column_from_header_returns_clean_text():
    html = "<th>   Launch Site  </th>"
    row = BeautifulSoup(html, "html.parser").th
    assert extract_column_name_from_header(row) == "Launch Site"


def test_extract_table_headers_returns_expected_columns():
    html = """
    <html>
        <body>
            <table><tr><td>Not this one</td></tr></table>
            <table><tr><td>Still not this one</td></tr></table>
            <table>
                <tr><th>Rocket</th><th>Payload<sup>*</sup></th></tr>
            </table>
        </body>
    </html>
    """
    headers = extract_table_headers(html, table_index=2)
    assert headers == ["Rocket", "Payload"]


def test_extract_table_headers_with_return_soup():
    html = """
    <html><body>
        <table><tr><th>Col1</th><th>Col2</th></tr></table>
        <table><tr><th>A</th><th>B</th></tr></table>
        <table><tr><th>Foo</th><th>Bar</th></tr></table>
    </body></html>
    """
    headers, soup = extract_table_headers(html, table_index=2, return_soup=True)
    assert headers == ["Foo", "Bar"]
    assert isinstance(soup, BeautifulSoup)

