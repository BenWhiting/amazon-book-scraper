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
@click.option(
    '--maxproducts', '-m',
    type=int,
    help='Max number of pages Scraped',
    default=10
)
def main(url, maxproducts): 
    conn = amazon.Connection()
    conn.search(url, maxproducts)

if __name__ == "__main__":
    # TODO: This will show up as an error due to click,
    #  find way to fix. Not sure if I like how the click lib works
    main()
