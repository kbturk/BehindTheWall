import requests, sys, argparse
from bs4 import BeautifulSoup

def error_log(s: str) -> bool:
    print(f'\033[31;1m{s}\033[0m', file=sys.stderr)
    return False

def arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('tag_string', help='html tag string', type=str)
    parser.add_argument('url', help='URL to fetch', type=str)
    g = parser.add_mutually_exclusive_group()
    g.add_argument('-c', '--class', dest='class_',
      help='search for text where tag_string matches HTML class name', action='store_true')
    g.add_argument('-i', '--id', dest= 'id', help='search for text where tag_string matches HTML id name',
      action='store_true')
    return parser

def pretty_format(text: str, par_length:int = 5) -> str:
    '''
    create pretty output format by splitting the text into paragraphs based on periods.
    par_length is an optional paramater.
    '''

    s_list = text.split('.')
    for i, s in enumerate(s_list):
        s_list[i] = f"{s}."
        if i% 5 == 0:
            s_list[i] = s_list[i] + "\n\n"

    return "".join(s_list)

def scraper(args) -> bool:
    '''
    use requests to stream html from a website URL which is then parsed using
    beautifulSoup's find_all function.

    requests is a popular 3rd party open source python library
    see https://github.com/psf/requests.git for more info

    beautifulSoup4 is a popular 3rd party os python library that parses
    html code.
    '''

    r: requests.models.Response = requests.get(args.url, stream=True)
    r.encoding = 'utf-8'

    if len(r.text) == 0:
        return error_log('had issue with requests.get scraper.')

    #Translate to beautiful soup.
    soup = BeautifulSoup(r.text, 'html.parser')

    #find the content you're looking for:
    if args.id:
        entries = soup.find_all( id = args.tag_string )
    elif args.class_:
            entries = soup.find_all( class_ = args.tag_string )
    else:
        entries = soup.find_all( args.tag_string )

    if len(entries) == 0:
        return error_log(f'no entries found when searching for: {args.tag_string}')

    content = []

    for entry in entries:
        try:
            for text in entry.stripped_strings:
                content.append(" "+text)

        except ValueError:
            return error_log(f'issues scraping text: {entry}')
    
    content_string = pretty_format(''.join(content))

    with open('website.txt', 'w', encoding = 'utf8') as f:
        f.write(content_string)

    print('''\033[32;1msite scraping is complete. To view results, please open website.txt or 
    you can view in the terminal using something like: `fold -s website.txt`\033[0m''')

    return True

def main(argv: list[str]) -> int:
    scraper(arg_parser().parse_args(argv[1:]))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
