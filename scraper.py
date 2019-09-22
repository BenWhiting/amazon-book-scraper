#!/user/bin/env python3
import click
import amazon

@click.command()
@click.option(
    '--url', '-u',
    type=str,
    help='An Amazon result Page',
    default=""
)
def main(url): 
    conn = amazon.Connection(url)
    products = conn.scrape_search_pages()

if __name__ == "__main__":
    # TODO: This will show up as an error due to click,
    #  find way to fix. Not sure if I like how the click lib works
    main()
