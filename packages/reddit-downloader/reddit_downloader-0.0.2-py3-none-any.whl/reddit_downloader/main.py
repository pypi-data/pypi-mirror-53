import argparse
import logging
import re
from os import mkdir
from os.path import isdir, isfile
from queue import Queue
from threading import Thread
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import wget
from requests import ConnectionError

logging.basicConfig(level=40,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    filename='reddit_downloader/log/myapp.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)


try:
    import praw as praw
    from prawcore import exceptions as pc_exceptions

except ModuleNotFoundError:
    print('Praw not imported.  Please import and try again.')
    exit(1)


def wrap(pre, post):
    """ Wrapper """

    def decorate(func):
        """ Decorator """

        def call(*args, **kwargs):
            """ Actual wrapping """
            pre(func, *args)
            result = func(*args, **kwargs)
            post(func)
            return result

        return call

    return decorate


def entering(func, *args):
    """ Pre function logging """
    wrap_log = logger.getChild(func.__name__)
    wrap_log.debug("Entered")
    if len(args) == 0:
        wrap_log.debug('No arguments')

    try:
        for i in range(len(args)):
            wrap_log.debug("The argument %s is %s" % (func.__code__.co_varnames[i], args[i]))
    except IndexError:
        wrap_log.exception('Exception raised')


def exiting(func):
    """ Post function logging """
    wrap_log = logger.getChild(func.__name__)
    wrap_log.debug("Exited")


num_dl_threads = 2
download_queue = Queue()
threads = []


@wrap(entering, exiting)
def main(lookup_sub_array, limit, allow_imgur_album, sub_sort, log_level):
    set_log_level(verbose_level)
    first_run()
    reddit = praw.Reddit('download_bot')
    for sub in lookup_sub_array:
        post_url = pull_posts(reddit, sub, limit, sub_sort)
        url_sorter(post_url, sub, allow_imgur_album)
    thread_control()
    download_queue.join()
    exit(0)

@wrap(entering, exiting)
def set_log_level(lvl):
    '''
    Changes default logging level to a new level that is set during argsparse.
    +----+-------------+
    | -v | Error Level |
    +----+-------------+
    | 1  | Warning     |
    +----+-------------+
    | 2  | Info        |
    +----+-------------+
    | 3  | Debug       |
    +----+-------------+
    :param lvl: Numerical count of -v flag on run.
    :return: None.
    '''
    log_level = 40
    if lvl == 0:
        logger.debug('Logging Disabled')
        logging.disabled = True
    elif lvl == 1:
        logger.debug('Logging level ERROR')
        log_level = logging.ERROR
    elif lvl == 2:
        logger.debug('Logging INFO')
        log_level = logging.INFO
    elif lvl == 3:
        logger.debug('Logging DEBUG')
        log_level = logging.DEBUG
    logger.setLevel(log_level)


@wrap(entering, exiting)
def download_file(i, data):
    name = 'download_file.' + str(i)
    root_path = 'reddit_downloader/images/'
    sub = data[0]
    url = data[1]
    filename = data[2]
    file_directory = root_path + sub
    filepath = root_path + sub + '/' + filename
    if not isdir(file_directory):
        try:
            mkdir(file_directory)
        except FileExistsError:
            pass
    if not isfile(filepath):
        try:
            wget.download(url, filepath)
        except FileNotFoundError as err:
            pass
        except HTTPError as err:
            pass
        except URLError as err:
            pass
    else:
        pass


@wrap(entering, exiting)
def worker(i, q):
    name = 'worker.' + str(i)
    while True:
        b = q.get()
        if b is None:
            break
        download_file(i, b)
        q.task_done()


@wrap(entering, exiting)
def thread_control():
    for t in range(num_dl_threads):
        t += 1
        t_worker = Thread(target=worker, args=(t, download_queue))
        t_worker.setDaemon(True)
        t_worker.start()
        threads.append(t)


@wrap(entering, exiting)
def url_sorter(url_list, sub, allow_album):
    log = logger.getChild('url_sorter')
    for url in url_list:
        log.debug(url)
        imgur_album = re.match("(?:https?:\/\/)(?:m.)?imgur.com\/a\/(?P<album_key>[0-9a-zA-Z]*)", url)

        if imgur_album and allow_album:
            album_key = imgur_album.group('album_key')
            url_sorter_imgur_album(sub, album_key)

        if not imgur_album:
            m = re.match("(?P<url>(?:https?):\/\/(?P<domain>(?:i\.|pbs\.|m\.)?(redd("
                         "?:.it|ituploads\.com|itmedia\.com)|imgur\.com|twimg\.com))\/(?P<album>a\/)?(?:.*\/)?("
                         "?P<filename>[-_0-9a-zA-Z]*)(?P<file_ext>\.jpg|\.jpeg|\.gifv|\.png|\.gif)?)", url)
            if m:  # Ignore non matches.
                m_filename = (m.group('filename'))
                log.debug(m_filename)
                m_file_ext = (m.group('file_ext'))
                log.debug(m_file_ext)
                if m_file_ext is None:
                    m_file_ext = '.jpg'
                filename_dl = m_filename + m_file_ext
                log.debug('Adding Sub: %s, URL: %s, File: %s' % (sub, url, filename_dl))
                download_queue.put([sub, url, filename_dl])


@wrap(entering, exiting)
def url_sorter_imgur_album(sub, key):
    log = logger.getChild('url_sorter_imgur_album')
    full_list_url = "http://imgur.com/a/" + key + "/layout/blog"
    try:
        response = urlopen(url=full_list_url)
    except HTTPError as err:
        # log.exception(err)
        pass
    except URLError as err:
        # log.exception(err)
        pass
    html = response.read().decode('utf-8')
    image_i_ds = re.findall('.*?{"hash":"([a-zA-Z0-9]+)".*?"ext":"(\.[a-zA-Z0-9]+)".*?', html)
    for i in image_i_ds:
        filename = i[0]
        ext = i[1]
        filename_dl = filename + ext
        url = 'http://imgur.com/' + filename_dl
        log.debug('Adding Sub: %s, URL: %s, File: %s' % (sub, url, filename_dl))
        download_queue.put([sub, url, filename_dl])


@wrap(entering, exiting)
def pull_posts(reddit, sub, pull_limit, sort):
    submissions = eval("reddit.subreddit(sub).%s(limit=pull_limit)" % sort)
    posts = []
    try:
        for post in submissions:
            posts.append(post.url)
        return posts
    except pc_exceptions.Redirect:
        logger.error('Sub not found')
        pass
    except pc_exceptions.RequestException:
        logger.error('No connection.')
        exit(1)
    except ConnectionError:
        logger.error("Requets error, no conneciton.")
    except pc_exceptions.ResponseException:
        logger.error('Bad authentication. Check praw.ini file.')
        exit(1)


@wrap(entering, exiting)
def args_parser():
    """Function to allow arguments passed on run time to be converted to strings."""
    parser = argparse.ArgumentParser(description="Tool allowing the downloading of images and gifs from listed "
                                                 "subreddit.")
    parser.add_argument('sub', nargs='+', help='Input subreddit for downloading.')
    parser.add_argument('-l', '--limit', help='Number of submissions to be downloaded.', type=int, default=5)
    parser.add_argument('-a', '--album', help='Allow Imgur albums', action='store_true', default=False)
    parser.add_argument('-s', '--sort', help='Change default sort.', choices=["new", "hot", "top", "rising"],
                        default='new')
    parser.add_argument('-v', '--verbose', help='More verbose logging.', action='count',
                        default=0)
    args = parser.parse_args()
    return args.sub, args.limit, args.album, args.sort, args.verbose


@wrap(entering, exiting)
def first_run():
    if not isdir('images'):
        mkdir('images')


if __name__ == '__main__':
    lookup_sub_array, limit, allow_imgur_album, sub_sort, verbose_level = args_parser()
    main(lookup_sub_array, limit, allow_imgur_album, sub_sort, verbose_level)
