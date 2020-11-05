#Let's create a little rss feed generator in Derrick's favorite language.
#written by kbturk @ 10/28/2020

import requests, sys
from bs4 import BeautifulSoup

def error_log(s):
    print(s, file=sys.stderr)

def main(argv):

    if len(argv) > 4:
        try:
            URL, search, child, class_or_id, _id = argv[1].strip(), argv[2].strip(), argv[3].strip(), argv[4].string() == True, argv[5].strip() == True
            print(f'URL: {URL}\n search string: {search}\n child: {child}' )  

        except ValueError:
            print( 'issues parsing command line inputs.\n' )
    elif len(argv) == 3:
        try:
            URL, search = argv[1].strip(),argv[2].strip()
        except ValueError:
            print( 'issues parsing command line inputs.\n' )

        class_or_id, _id, child = False, False, 'div'
    else: 
        print(f'I got the following arguments:\n {argv}')
        print('wrong number of arguments provided. Using defaults.')
        print('''please provide one of the following combinations of arguments:
        short search: {URL} {html tag search term - usually "body"}
        deep search: {URL} {html tag search term - usually body or div} {child - item inside of first search tag term} {class_: True or False} {id: True or False}
        ''')

        return

        #Troubleshooting defaults:
        '''
        URL = 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'
        search = 'div'
        class_or_id = True
        _id = True
        child = 'installing-beautiful-soup'''

    print(f'URL: {URL}\nsearch: {search}\nclass_or_id: {class_or_id}\n_id:{_id}\nchild:{child}')


    #Let's do a little web scraping. returns a urllib3.response.HTTPResponse object.
    r = requests.get(URL, stream=True)
    r.encoding = 'utf-8'

    if len(r.text) == 0:
        print('had issue with requests.get scraper.')

    #Translate that shit to beautiful soup.
    soup = BeautifulSoup(r.text, 'html.parser')

    #find the content you're looking for:
    if class_ or id:

        if _id:
            entries = soup.find_all( id = child )

        else:
            entries = soup.find_all( class_ = child )

    else:
        entries = soup.find_all( search )

    if len(entries) == 0:
        print(f'no entries found. {entries}')

    content = []

    for entry in entries:
            try:
                content.append(entry.get_text().strip('   \n'))
            except ValueError:
                print('issues scraping text.')
                error_log(entry)

    content = ''.join(content)

    with open('website.txt', 'w', encoding = 'utf8') as f:
        f.write(content)
    print('''site scraping is complete. To view results, please open website.txt. 
    We recommend using the following command from the command line: fold -s website.txt to view in terminal.''')

if __name__ == '__main__':
    sys.exit(main(sys.argv))