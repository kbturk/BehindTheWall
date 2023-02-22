import requests, sys, argparse
from bs4 import BeautifulSoup

def error_log(s) -> None:
    print(s, file=sys.stderr)

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL to fetch', type=str)
    parser.add_argument('tag_string', help='html tag string', type=str)
    g = parser.add_mutually_exclusive_group()
    g.add_argument('-c', '--class', dest='class_',
      help='search for text where tag_string matches HTML class name', action='store_true')
    g.add_argument('-i', '--id', dest= 'id', help='search for text where tag_string matches HTML id name',
      action='store_true')
    return parser

def pretty_format(text: str, par_length = 5) -> str:
    s_list = text.split('.')
    for i, s in enumerate(s_list):
        s_list[i] = f"{s}."
        if i% 5 == 0:
            s_list[i] = s_list[i] + "\n\n"

    return "".join(s_list)

def scraper(args) -> bool:
    '''
    uses requests to stream html from a website URL which is then parsed using
    beautifulSoup
    '''

    # returns a urllib3.response.HTTPResponse object.
    r = requests.get(args.url, stream=True)
    r.encoding = 'utf-8'

    if len(r.text) == 0:
        print('had issue with requests.get scraper.')

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
        print(f'no entries found. {entries}')
        return False

    content = []

    for entry in entries:
        try:
            for text in entry.stripped_strings:
                content.append(" "+text)

        except ValueError:
            print('issues scraping text.')
            error_log(entry)
            return False
    
    content_string = pretty_format(''.join(content))

    with open('website.txt', 'w', encoding = 'utf8') as f:
        f.write(content_string)

    print('''site scraping is complete. To view results, please open website.txt or 
    you can view in the terminal using something like: `fold -s website.txt`''')

    return True

def main(argv) -> int:
    scraper(arg_parser().parse_args(argv[1:]))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
