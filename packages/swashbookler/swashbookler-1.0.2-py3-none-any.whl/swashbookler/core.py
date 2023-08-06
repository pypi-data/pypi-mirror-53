import os
import random
import re
import requests
import multiprocessing
import multiprocessing.pool
from typing import Optional, Dict, List
import urllib
import unicodedata
import yaml
from bs4 import BeautifulSoup
import img2pdf
import shutil
import logging
import time
from . import exceptions

__all__ = [
    'download_book'
]

_PAGE_URL: str = 'https://books.google.com/books?id={book_id}&jtp={page}'

_USER_AGENTS: List[str] = [
    'Mozilla/5.0 (Mobile; rv:18.0) Gecko/18.0 Firefox/18.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MSAppHost/1.0)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B142',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
]

_MAX_DOWNLOAD_ATTEMPTS = 5

_TEMP_DIRECTORY = '{book_id}_temp'

# Used for testing. Suppresses addition of timestamps to PDF.
_NO_DATE = None


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def download_book(
        book_id: str,
        save_metadata: bool = True,
        save_pdf: bool = True,
        save_images: bool = False,
        width: int = 2048,
        max_threads: Optional[int] = None,
        max_pages: Optional[int] = None) -> str:
    """Downloads a Google book with a given ID.

    :param book_id: The ID of the book to download
    :param save_metadata: If True, get additional metadata and save it into a companion file
    :param save_pdf: If True, download book as a PDF. Default True.
    :param save_images: If True, download pages as individual images. Default False.
    :param width: The page image width in pixels. Default 2048.
    :param max_threads: The maximum number of download threads to use, or None to default to the number of CPUs
    :param max_pages: If specified, only this number of pages will be downloaded. Default None, for all pages
    :return: The book filename, corresponding to the PDF and/or metadata file and/or image
    directory.
    """

    book_url = _PAGE_URL.format(book_id=book_id, page=0)
    log.info('Downloading book at %s', book_url)
    start_time = time.time()

    # Grab metadata
    metadata = {'title': book_id}
    if save_metadata:
        log.debug('Fetching metadata...')
        try:
            metadata = _get_metadata(book_url)
        except requests.exceptions.RequestException as e:
            log.warning(
                'Failed to download metadata. Check that book ID is valid and network is available. Error: %s', str(e))
        except Exception as e:
            log.warning('Failed to parse metadata: %s', str(e))

    book_filename = _slugify(metadata['title'])
    directory_filename = _slugify(_TEMP_DIRECTORY.format(book_id=book_id))
    log.info('Saving book as \"%s\"', book_filename)

    # Download metadata
    if save_metadata:
        with open('{}.yaml'.format(book_filename), 'w') as metadata_file:
            yaml.dump(metadata, metadata_file)

    if not save_pdf and not save_images:
        return book_filename

    # Create directory to hold downloaded files
    os.makedirs(directory_filename, exist_ok=True)

    # Find pages and download them
    log.debug('Getting page info and downloading images...')
    try:
        page_filenames = _discover_and_save_pages(book_url, width, max_pages, directory_filename, max_threads)
    except requests.exceptions.RequestException as e:
        log.error('Failed to download book pages. Check that book ID is valid and network is available.')
        raise exceptions.NetworkError(e)
    except Exception as e:
        log.error('Failed to parse page info: %s', str(e))
        raise exceptions.ParsingError(e)

    # Assemble to PDF
    if save_pdf:
        log.debug('Saving PDF...')
        with open('{}.pdf'.format(book_filename), 'wb') as pdf_file:
            pdf_file.write(img2pdf.convert(page_filenames, nodate=_NO_DATE))
        log.info('Book PDF saved')

    # Delete images if not needed
    if save_images:
        log.debug('Saving page images to output directory...')
        os.makedirs(book_filename, exist_ok=True)
        for page_filename in page_filenames:
            shutil.copy(page_filename, book_filename)
        log.info('Saved page images to output directory')

    log.debug('Deleting temporary files...')
    for page_filename in page_filenames:
        try:
            os.remove(page_filename)
        except OSError as e:
            log.error('Could not remove temporary file \"%s\", got error: %s', page_filename, str(e))

    if os.path.exists(directory_filename) \
            and os.path.isdir(directory_filename) \
            and not os.listdir(directory_filename):
        os.rmdir(directory_filename)

    log.info('Removed temporary files')

    end_time = time.time()
    elapsed = end_time - start_time
    log.info('Downloaded book in %.1f seconds, at a rate of %.2f seconds per page', elapsed, elapsed / len(page_filenames))

    return book_filename


def _slugify(text: str) -> str:
    """Removes invalid characters from a string, rendering it usable as a filename.

    :param text: Input string, supporting Unicode
    :returns: A normalized string with whitespace and invalid characters replaced with hyphens.
    """

    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^\w\s-]', '', text).strip()
    return re.sub(r'[-\s]+', '-', text)


def _slugify_path(path: str) -> str:
    """Slugifies a path by replacing slashes with hyphens, then passing it through _slugify.

    :param path: Input path
    :returns: A normalized string with slashes, whitespace, and invalid characters replaced with
    hyphens.
    """

    return _slugify(re.sub(r'[\\/]+', '-', path.strip('/\\')))


def _unwrap(text: str) -> str:
    """Un-wraps text paragraphs by removing linebreaks and duplicate whitespaces."""

    return re.sub(r'[\s]+', ' ', text).strip()


def _get_remote_file(url: str, attempts: Optional[int] = None) -> requests.Response:
    """Fetches a remote file at a given URL. Automatically reties if the file could not be downloaded.

    :param url: The URL of the file to download
    :param attempts: The max number of attempts to allow. Default 5
    :returns: A "requests" Response with the contents of the file
    :raises NetworkException: Raised in the event of an error
    """

    if attempts is None:
        attempts = _MAX_DOWNLOAD_ATTEMPTS

    if attempts < 1:
        attempts = 1

    while True:
        attempts -= 1
        try:
            # NB: Google denies access if a browser-like user agent isn't supplied.
            # Randomizing the user-agent also tends to speed up downloading for some reason.
            headers = {
                'user-agent': random.choice(_USER_AGENTS)
            }

            req = requests.get(url, headers=headers)
            req.raise_for_status()
            log.debug('\t[%i] Downloaded file at %s', req.status_code, url)
            return req
        except requests.exceptions.RequestException as e:
            log.warning('Could not download %s. Remaining attempts: %i Error: %s', url, attempts, str(e))
            if attempts < 1:
                log.error('Failed to download %s', url)
                raise exceptions.NetworkError(e)


def _discover_and_save_pages(
        book_url: str, width: int, max_pages: Optional[int], directory: str, max_threads: Optional[int]) -> List[str]:
    """Assembles page information for a given book and downloads associated page images.
    Simultaneously locates pages and downloads images to save time.

    :param book_url: The URL for the book
    :param width: The suggested page image width in pixels. Google may not respect the exact dimensions.
    :param max_pages: The maximum pages to download, or None for all
    :param directory: Output directory for images
    :param max_threads: The maximum page download threads to use, or None for default. Use 0 to download in single-thread mode.
    :returns: A list of page filenames in order.
    """
    url = book_url
    first_page_code = None
    page_number = 0
    page_filenames = []

    # Set up pool if using
    pool = None
    if max_threads is not None and max_threads <= 0:
        log.debug('Downloading pages in single-threaded mode...')
    else:
        log.debug('Downloading pages using %i processes...', max_threads or multiprocessing.cpu_count())
        pool = multiprocessing.pool.ThreadPool(processes=max_threads)
        pool_results = []

    log.debug('Getting page info...')
    while True:
        # Request the next page
        page = _get_remote_file(url)

        # Parse the page
        page_soup = BeautifulSoup(page.text, 'html.parser')

        # Extract image URL and page code from page style
        try:
            page_image_div = page_soup.find('div', class_='html_page_image')
            style = page_image_div.parent.style.text
            image_url = re.search(r'background-image:\s*url\(\s*"([^"]+)"\s*\)', style).group(1)
            image_url_parsed = urllib.parse.urlparse(image_url)
            code_elements = [_slugify_path(image_url_parsed.path)]
            image_url_query = urllib.parse.parse_qs(image_url_parsed.query)
            code_elements.extend(
                image_url_query[key][0]
                for key in ('id', 'pg', 'img', 'zoom', 'hl')
                if key in image_url_query and image_url_query[key])
            page_code = _slugify('-'.join(code_elements))
        except AttributeError as e:
            log.error('Could not parse page at %s. Error: %s', url, str(e))
            raise exceptions.ParsingError(e)

        # Check that the page isn't the first page (indicating the end of the book as reaches)
        if page_code == first_page_code:
            break

        # If this is the first page we've checked, extract the image code and store it to compare against
        if first_page_code is None:
            first_page_code = page_code

        log.info('Discovered page %i (%s)', page_number + 1, page_code)

        # Download the page image
        if width:
            image_url = image_url + '&w={}'.format(width)  # Force a larger image size
        page_filename = os.path.join(directory, '{}.png'.format(page_code))
        page_filenames.append(page_filename)

        page_name = '{page_number} ({page_code})'.format(page_number=page_number + 1, page_code=page_code)

        if pool:
            pool_results.append(pool.apply_async(_download_and_save_page, args=(image_url, page_filename, page_name)))
        else:
            _download_and_save_page(image_url, page_filename, page_name)

        # Extract URL and code for next page
        try:
            next_page = page_soup.find(id="next_btn").find_parent('a').get('href')
        except (AttributeError, IndexError) as e:
            log.error('Could not parse page. Error: %s', str(e))
            raise exceptions.ParsingError(e)

        # Move on to the next page
        url = next_page
        page_number += 1

        if max_pages is not None and page_number >= max_pages:
            break

    if pool:
        log.info('Page discovery complete')
        log.debug('Waiting for image downloads to complete...')
        pool.close()

        # Doing a 'get' on every result ensures exceptions are propagated from the worker threads
        for pool_result in pool_results:
            pool_result.get()

        pool.join()
        log.info('Downloaded all pages')
    else:
        log.info('Page discovery and download complete')

    return page_filenames


def _get_metadata(book_url: str) -> Dict[str, str]:
    """Fetches metadata from a given book.

    :param book_url: The URL of the book to download
    :returns: A dictionary of book metadata
    """

    metadata = dict()

    # Download metadata from book URL
    first_page = _get_remote_file(book_url)
    first_page_soup = BeautifulSoup(first_page.text, 'html.parser')

    # Basic metadata
    try:
        metadata['title'] = _unwrap(first_page_soup.head.find('meta', attrs={'name': 'title'}).get('content'))
    except AttributeError as e:
        log.warning('Error parsing title: %s', e)

    try:
        metadata['description'] = _unwrap(
            first_page_soup.head.find('meta', attrs={'name': 'description'}).get('content'))
    except AttributeError as e:
        log.warning('Error parsing description: %s', e)

    try:
        metadata['about_url'] = _unwrap(first_page_soup.head.find('link', rel='canonical').get('href'))
    except AttributeError as e:
        log.warning('Error parsing about url: %s', e)

    log.info('Got basic metadata')

    # Download "about" page, if possible
    if not metadata.get('about_url', None):
        log.warning('Could not locate extended metadata')
        return {k: v for k, v in metadata.items() if v}

    try:
        about_page = _get_remote_file(metadata['about_url'])
        about_page_soup = BeautifulSoup(about_page.text, 'html.parser')

        # Additional metadata from "about" page
        try:
            metadata['full_title'] = _unwrap(about_page_soup.find(id='bookinfo').find(class_='booktitle').text)
        except AttributeError as e:
            log.warning('Error parsing full title: %s', e)

        try:
            metadata['synopsis'] = _unwrap(about_page_soup.find(id='bookinfo').find(id='synopsis').text)
        except AttributeError as e:
            log.warning('Error parsing synopsis: %s', e)

        try:
            infoblock = [item
                         for item in about_page_soup.find(id='bookinfo').find(class_="bookinfo_sectionwrap").children
                         if str(item).strip()]

            metadata['author'] = _unwrap(infoblock[0].text)
            pub_and_year, categories, pages_str = (_unwrap(item) for item in infoblock[1].text.split('-'))
            metadata['categories'] = _unwrap(categories)
            metadata['pages'] = _unwrap(pages_str)
            publisher, year = (_unwrap(item) for item in pub_and_year.split(','))
            metadata['publisher'] = _unwrap(publisher)
            metadata['year'] = _unwrap(year)
        except (AttributeError, IndexError, ValueError) as e:
            log.warning('Error parsing info block: %s', e)
    except Exception as e:
        log.warning('Could not get extended metadata. Error: %s', str(e))
    else:
        log.info('Got extended metadata')

    return {k: v for k, v in metadata.items() if v}


def _download_and_save_page(image_url: str, filename: str, page_name: Optional[str] = None):
    """Download a page and save it to a file.

    :param image_url: The URL of the page's image
    :param filename: THe local filename to which to save the page
    :param page_name: If specified, the name of the page to include in log messages
    """

    req = _get_remote_file(image_url)
    with open(filename, 'wb') as f:
        f.write(req.content)

    if page_name:
        log.info('Saved page %s to %s', page_name, filename)
    else:
        log.info('Saved page to %s')
