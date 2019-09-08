from amazon.client  import Client
from amazon.client  import _css_select
from amazon.client  import _SPAN_CLASS_TITLE
from amazon.client  import _HTML_PARSER
from amazon.client  import _SPAN_SPONSERED_TITLE
import pytest
from bs4 import BeautifulSoup

def test_css_select_valid():
    # I could reformat this to be pretty but I will do that later
    test_page = """
    <div class="sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28" data-asin="1789532221" data-index="12"><div class="sg-col-inner">
    <div class="s-include-content-margin s-border-bottom">
    <div class="a-section a-spacing-medium">
    <div class="sg-row">
    <div class="a-section a-spacing-micro s-min-height-small">
    </div>
    </div>
    <div class="sg-row">
    <div class="sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32"><div class="sg-col-inner">
    <div class="a-section a-spacing-none">
    <span class="rush-component" data-component-type="s-product-image">
    <a class="a-link-normal" href="/Hands-RESTful-Python-Web-Services/dp/1789532221/ref=sr_1_13?keywords=python+scraping&amp;qid=1567971851&amp;s=gateway&amp;sr=8-13">
    <div class="a-section aok-relative s-image-fixed-height">
    <img alt="Hands-On RESTful Python Web Services: Develop RESTful web services or APIs with modern Python 3.7, 2nd Edition" class="s-image" data-image-index="12" data-image-latency="s-product-image" data-image-load="" data-image-source-density="1" src="https://m.media-amazon.com/images/I/61lK-WxPQYL._AC_UY218_.jpg" srcset="https://m.media-amazon.com/images/I/61lK-WxPQYL._AC_UY218_.jpg 1x, https://m.media-amazon.com/images/I/61lK-WxPQYL._AC_UY327_FMwebp_QL65_.jpg 1.5x, https://m.media-amazon.com/images/I/61lK-WxPQYL._AC_UY436_FMwebp_QL65_.jpg 2x, https://m.media-amazon.com/images/I/61lK-WxPQYL._AC_UY545_FMwebp_QL65_.jpg 2.5x, https://m.media-amazon.com/images/I/61lK-WxPQYL._AC_UY654_FMwebp_QL65_.jpg 3x"/>
    </div>
    </a>
    </span>
    </div>
    </div></div>
    <div class="sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28"><div class="sg-col-inner">
    <div class="sg-row">
    <div class="sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-32 sg-col-12-of-20 sg-col-12-of-36 sg-col sg-col-12-of-24 sg-col-12-of-28"><div class="sg-col-inner">
    <div class="a-section a-spacing-none">
    <h2 class="a-size-mini a-spacing-none a-color-base s-line-clamp-2">
    <a class="a-link-normal a-text-normal" href="/Hands-RESTful-Python-Web-Services/dp/1789532221/ref=sr_1_13?keywords=python+scraping&amp;qid=1567971851&amp;s=gateway&amp;sr=8-13">
    <span class="a-size-medium a-color-base a-text-normal">Hands-On RESTful Python Web Services: Develop RESTful web services or APIs with modern Python 3.7, 2nd Edition</span>
    </a>
    </h2>
    <div class="a-row a-size-base a-color-secondary"><span class="a-size-base">by </span><span class="a-size-base">C. Hillar, Gaston</span><span class="a-letter-space"></span><span class="a-size-base a-color-secondary"> | </span><span class="a-letter-space"></span><span class="a-size-base a-color-secondary a-text-normal">Dec 26, 2018</span></div>
    </div>
    </div></div>
    </div>
    <div class="sg-row">
    <div class="sg-col-4-of-12 sg-col-6-of-20 sg-col-4-of-16 sg-col sg-col-6-of-36 sg-col-6-of-28 sg-col-6-of-32 sg-col-6-of-24"><div class="sg-col-inner">
    <div class="a-section a-spacing-none a-spacing-top-small">
    <div class="a-row a-size-base a-color-base">
    <a class="a-size-base a-link-normal a-text-bold" href="/Hands-RESTful-Python-Web-Services/dp/1789532221/ref=sr_1_13?keywords=python+scraping&amp;qid=1567971851&amp;s=gateway&amp;sr=8-13">
        
            
            
                Paperback
            
        
    </a>
    </div><div class="a-row a-size-base a-color-base"><div class="a-row">
    <a class="a-size-base a-link-normal s-no-hover a-text-normal" href="/Hands-RESTful-Python-Web-Services/dp/1789532221/ref=sr_1_13?keywords=python+scraping&amp;qid=1567971851&amp;s=gateway&amp;sr=8-13">
    <span class="a-price" data-a-color="base" data-a-size="l"><span class="a-offscreen">$44.99</span><span aria-hidden="true"><span class="a-price-symbol">$</span><span class="a-price-whole">44<span class="a-price-decimal">.</span></span><span class="a-price-fraction">99</span></span></span>
    </a>
    <span class="a-letter-space"></span></div></div>
    </div>
    <div class="a-section a-spacing-none a-spacing-top-micro">
    <div class="a-row a-size-base a-color-secondary s-align-children-center"><div class="a-row s-align-children-center">
    <span class="aok-inline-block s-image-logo-view">
    <span class="aok-relative s-icon-text-medium s-prime">
    <i aria-label="Amazon Prime" class="a-icon a-icon-prime a-icon-medium" role="img"></i>
    </span>
    <span>
    </span>
    </span>
    <span aria-label="Get it as soon as Wed, Sep 11">
    <span>Get it as soon as </span><span class="a-text-bold">Wed, Sep 11</span>
    </span>
    </div><div class="a-row">
    <span aria-label="FREE Shipping by Amazon">
    <span>FREE Shipping by Amazon</span>
    </span>
    </div></div>
    </div>
    <div class="a-section a-spacing-none a-spacing-top-mini">
    <div class="a-row"><div class="a-row a-spacing-mini"><hr class="a-spacing-mini a-divider-normal"/><div class="a-row a-size-base a-color-base">
    <a class="a-size-base a-link-normal a-text-bold" href="/Hands-RESTful-Python-Web-Services-ebook/dp/B07KYQR1NQ/ref=sr_1_13?keywords=python+scraping&amp;qid=1567971851&amp;s=gateway&amp;sr=8-13">
        
            
            
                Kindle
            
        
    </a>
    </div><div class="a-row a-size-base a-color-base"><div class="a-row">
    <a class="a-size-base a-link-normal s-no-hover a-text-normal" href="/Hands-RESTful-Python-Web-Services-ebook/dp/B07KYQR1NQ/ref=sr_1_13?keywords=python+scraping&amp;qid=1567971851&amp;s=gateway&amp;sr=8-13">
    <span class="a-price" data-a-color="base" data-a-size="l"><span class="a-offscreen">$29.49</span><span aria-hidden="true"><span class="a-price-symbol">$</span><span class="a-price-whole">29<span class="a-price-decimal">.</span></span><span class="a-price-fraction">49</span></span></span>
    <span class="a-price a-text-price" data-a-color="secondary" data-a-size="b" data-a-strike="true"><span class="a-offscreen">$35.99</span><span aria-hidden="true">$35.99</span></span>
    </a>
    <span class="a-letter-space"></span></div></div></div></div>
    </div>
    </div></div>
    <div class="sg-col-4-of-12 sg-col-6-of-20 sg-col-4-of-16 sg-col sg-col-6-of-36 sg-col-6-of-28 sg-col-6-of-32 sg-col-6-of-24"><div class="sg-col-inner">
    </div></div>
    </div>
    <div class="sg-row">
    <div class="sg-col-20-of-24 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-8-of-12 sg-col-12-of-16 sg-col-24-of-28"><div class="sg-col-inner">
    </div></div>
    </div>
    <div class="sg-row">
    <div class="sg-col-20-of-24 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-8-of-12 sg-col-12-of-16 sg-col-24-of-28"><div class="sg-col-inner">
    </div></div>
    </div>
    </div></div>
    </div>
    </div>
    </div>
    </div></div>
    """

    test_html_parser = _HTML_PARSER
    test_css_select = _SPAN_CLASS_TITLE
    soup = BeautifulSoup(test_page, test_html_parser)

    title = _css_select(soup, test_css_select)
    if len(title) != 1:
        assert False 
    return


def test_css_select_sponsered():
    # I could reformat this to be pretty but I will do that later
    test_page = """
    <div class="s-result-item AdHolder sg-col sg-col-12-of-12" data-asin="" data-index="1"><div class="sg-col-inner">
    <div class="rush-component" data-component-props='{"percentageShownToFire":"50","batchable":true,"requiredElementSelector":".s-image","url":"https://www.amazon.com/gp/sponsored-products/logging/log-action.html?qualifier=1567978498&amp;id=4643333303029875&amp;widgetName=sp_phone_search_atf&amp;adId=200005194757471&amp;eventType=1&amp;adIndex=1"}' data-component-type="s-impression-logger">
    <div class="rush-component" data-component-type="sp-sponsored-result">
    <div class="s-include-content-margin s-border-bottom">
    <div class="a-section a-spacing-medium">
    <a class="a-link-normal s-faceout-link a-text-normal" href="/gp/slredirect/picassoRedirect.html/ref=pa_sp_phone_search_atf_aps_sr_pg1_2?ie=UTF8&amp;adId=A015931116VDNX60HWH8G&amp;url=%2FScraping-Python-Community-Experience-Distilled%2Fdp%2F1782164367%2Fref%3Dmp_s_a_1_2_sspa%3Fkeywords%3Dpython%2Bscraping%26qid%3D1567978499%26s%3Dgateway%26sr%3D8-2-spons%26psc%3D1&amp;qualifier=1567978498&amp;id=4643333303029875&amp;widgetName=sp_phone_search_atf" title="status-badge">
    <div class="sg-row">
    <div class="sg-col sg-col-12-of-12"><div class="sg-col-inner">
    <div class="a-section a-spacing-none s-status-badge-container s-min-height-base">
    </div>
    </div></div>
    </div>
    </a>
    <div class="sg-row">
    <a class="a-link-normal s-faceout-link a-text-normal" href="/gp/slredirect/picassoRedirect.html/ref=pa_sp_phone_search_atf_aps_sr_pg1_2?ie=UTF8&amp;adId=A015931116VDNX60HWH8G&amp;url=%2FScraping-Python-Community-Experience-Distilled%2Fdp%2F1782164367%2Fref%3Dmp_s_a_1_2_sspa%3Fkeywords%3Dpython%2Bscraping%26qid%3D1567978499%26s%3Dgateway%26sr%3D8-2-spons%26psc%3D1&amp;qualifier=1567978498&amp;id=4643333303029875&amp;widgetName=sp_phone_search_atf" title="product-image">
    <div class="sg-col-4-of-12 sg-col"><div class="sg-col-inner">
    <div class="a-section a-spacing-none a-text-center s-list-image-container">
    <span class="rush-component" data-component-type="s-product-image">
    <img alt="Web Scraping with Python (Community Experience Distilled)" class="s-image" data-image-index="1" data-image-latency="s-product-image" data-image-load="" data-image-source-density="1" onload="" src="https://m.media-amazon.com/images/I/71F30jnxtHL._AC_SX118_SY170_QL70_.jpg" srcset="https://m.media-amazon.com/images/I/71F30jnxtHL._AC_SX118_SY170_QL70_.jpg 1x, https://m.media-amazon.com/images/I/71F30jnxtHL._AC_SX177_SY255_FMwebp_QL65_.jpg 1.5x, https://m.media-amazon.com/images/I/71F30jnxtHL._AC_SX236_SY340_FMwebp_QL65_.jpg 2x, https://m.media-amazon.com/images/I/71F30jnxtHL._AC_SX295_SY425_FMwebp_QL65_.jpg 2.5x, https://m.media-amazon.com/images/I/71F30jnxtHL._AC_SX354_SY510_FMwebp_QL65_.jpg 3x"/>
    </span>
    </div>
    </div></div>
    </a>
    <div class="sg-col sg-col-8-of-12"><div class="sg-col-inner">
    <a class="a-link-normal s-faceout-link a-text-normal" href="/gp/slredirect/picassoRedirect.html/ref=pa_sp_phone_search_atf_aps_sr_pg1_2?ie=UTF8&amp;adId=A015931116VDNX60HWH8G&amp;url=%2FScraping-Python-Community-Experience-Distilled%2Fdp%2F1782164367%2Fref%3Dmp_s_a_1_2_sspa%3Fkeywords%3Dpython%2Bscraping%26qid%3D1567978499%26s%3Dgateway%26sr%3D8-2-spons%26psc%3D1&amp;qualifier=1567978498&amp;id=4643333303029875&amp;widgetName=sp_phone_search_atf" title="product-detail">
    <div class="a-section a-spacing-none">
    <span class="a-size-small a-color-secondary">Sponsored</span>
    <h2 class="a-size-mini a-spacing-none a-color-base s-line-clamp-3">
    <span class="a-size-base a-color-base a-text-normal">Web Scraping with Python (Community Experience Distilled)</span>
    </h2>
    <div class="a-row a-size-small a-color-secondary"><span class="a-size-small">by </span><span class="a-size-small">Richard Penman</span></div>
    </div>
    <div class="a-section a-spacing-none a-spacing-top-mini">
    <div class="a-row a-size-small">
    <span aria-label="3.9 out of 5 stars">
    <i class="a-icon a-icon-star-small a-star-small-4 aok-align-bottom"><span class="a-icon-alt">3.9 out of 5 stars</span></i>
    </span>
    <span aria-label="14">
    <span class="a-size-small a-color-secondary">14</span>
    </span>
    </div>
    </div>
    <div class="a-section a-spacing-mini a-spacing-top-small">
    <div class="a-row a-size-small a-color-base"><span class="a-size-small a-color-base a-text-bold">Paperback</span></div><div class="a-row a-size-small a-color-base"><div class="a-row"><span class="a-price" data-a-color="base" data-a-size="l"><span class="a-offscreen">$24.99</span><span aria-hidden="true"><span class="a-price-symbol">$</span><span class="a-price-whole">24<span class="a-price-decimal">.</span></span><span class="a-price-fraction">99</span></span></span></div></div>
    </div>
    <div class="a-section a-spacing-none">
    <div class="a-row a-size-small a-color-secondary s-align-children-center"><div class="a-row s-align-children-center">
    <span class="aok-inline-block s-image-logo-view">
    <span class="aok-relative s-icon-text-medium s-prime">
    <i aria-label="Amazon Prime" class="a-icon a-icon-prime a-icon-medium" role="img"></i>
    </span>
    <span>
    </span>
    </span>
    <span aria-label="Get it as soon as Wed, Sep 11">
    <span>Get it as soon as </span><span class="a-text-bold">Wed, Sep 11</span>
    </span>
    </div><div class="a-row">
    <span aria-label="FREE Shipping over $25 by Amazon">
    <span>FREE Shipping over $25 by Amazon</span>
    </span>
    </div></div>
    </div>
    </a>
    </div></div>
    </div>
    <div class="aok-hidden">
    </div>
    </div>
    </div>
    </div>
    </div>
    </div></div>
    """

    test_html_parser = _HTML_PARSER
    test_css_select = _SPAN_SPONSERED_TITLE
    soup = BeautifulSoup(test_page, test_html_parser)

    title = _css_select(soup, test_css_select)
    if len(title) != 1:
        assert False 
    return

def test_valid_url():
    cli = Client()
    url = 'https://www.amazon.com/s?k=python+scraping&page=1&qid=1567979575&ref=sr_pg_1'
    valid = cli._valid_url(url)
    if not valid:
        assert False