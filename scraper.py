#!/user/bin/env python3
import click

@click.command()
@click.option(
    '--url', '-u',
    type=str,
    help='An Amazon result Page',
    default=""
)
@click.option(
    '--maxpages', '-m',
    type=int,
    help='Max number of pages Scraped',
    default=10
)
def main(url, maxpages): 
    print(url)
    print(maxpages)


if __name__ == "__main__":
    # TODO: This will show up as an error due to click,
    #  find way to fix. Not sure if I like how the click lib works
    main()
