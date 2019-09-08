# amazon-book-scraper

## Description

Designed to scrape Amazon HTML pages for product details and
comparing book prices for books of mathcing titles.

I wanted to do this with no overhead budget and as simple as possible for
a [non-profit][non-profit], so utilizing the Amazon [API][api] which required AWS wasn't an options.

[api]: https://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemSearch.html
[non-profit]: http://www.seattlemetaphysicallibrary.org/

## Current state

This code base currently takes an amazon URL and scrapes the HTML from the page. It does so by
loop through multiple client types (desktop/mobile), searches through those client types, scans
the CSS, and it will attempt to find all intsances of products on the page.

## Dependencies

* click 7.0
* beautifulsoup4 4.8.0
* pytest 5.1.2
