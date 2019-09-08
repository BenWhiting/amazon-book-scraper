# amazon-book-scraper

## Description

Designed to scrape Amazon HTML pages for product details and
comparing book prices for books of mathcing titles.

I wanted to do this with no overhead budget and as simple as possible for
a [non-profit][non-profit], so utilizing the Amazon [API][api] which required AWS wasn't an option.

[api]: https://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemSearch.html
[non-profit]: http://www.seattlemetaphysicallibrary.org/

## Current state

This code base currently takes an amazon URL and scrapes the HTML from the page. It does so by
loop through multiple client types (desktop/mobile), searches through those client types, scans
the HTML, find all intsances of products on the page and will print them.

NOTE: sponsored books will be ignored - for now

### Expected URL format

The expected URL format can be found after...

 1. Completing a search in Amazon for the book you wish
 2. Clicking a page button at the bottom of the search (for auto-formatting)
 3. Copying the URL.

#### Additional format details

Example:

 `https://www.amazon.com/s?k=python+scraping&page=1&qid=1567979575&ref=sr_pg_1`

    - must contain:
        - page={N}
        - sr_pg_{N}
            - where N is equal to the current search page

### How to run

`python3 scraper.py --url "https://www.amazon.com/s?k=python+scraping&page=1&qid=1567979575&ref=sr_pg_1"`

WARNING: Include quotes around the URL or the path will be malformed

## Build Dependencies

* click 7.0
* beautifulsoup4 4.8.0
* pytest 5.1.2
