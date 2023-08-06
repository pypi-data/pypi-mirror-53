import click
import logging
import urllib.parse
import swashbookler

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)


@click.command()
@click.option('--save-metadata/--no-metadata', default=True, show_default=True,
              help='Fetch the book\'s metadata and save it to a YAML file.')
@click.option('--save-pdf/--no-pdf', default=True, show_default=True,
              help='Save the book as a PDF.')
@click.option('--save-images/--no-images', default=False, show_default=True,
              help='Keep the downloaded page images after download is complete.')
@click.option('--width', metavar='W', type=click.INT, default=2048,
              help='Suggested page width in pixels. Default 2048, pass 0 to use the Google Books default.')
@click.option('--max-threads', metavar='N', type=click.INT, default=None,
              help='Maximum number of download threads to use. If zero, run in single-threaded mode. '
                        'Defaults to the number of usable CPU cores.')
@click.option('--max-pages', metavar='N', default=None, type=click.INT,
              help='Maximum number of pages to download. Defaults to all pages.')
@click.option('--debug/--no-debug', default=False,
              help='Print additional debug information.')
@click.version_option(version=swashbookler.__version__, prog_name='swashbookler')
@click.argument('book_id', type=click.STRING)
def cli(**kwargs):
    """Downloads a Google Book and saves it as either a PDF or a folder of images.

    BOOK_ID may be either a Google Books ID or a URL to a book page (enclosed in quotes).
    """

    if kwargs['debug']:
        log.setLevel(logging.DEBUG)
    del kwargs['debug']

    book_id = kwargs['book_id']
    if book_id.find('books.google.com') != -1:
        parse_result = urllib.parse.urlparse(book_id)
        query = urllib.parse.parse_qs(parse_result.query)
        if 'id' in query and len(query['id']) > 0:
            kwargs['book_id'] = query['id'][0]

    swashbookler.download_book(**kwargs)


if __name__ == '__main__':
    cli()
