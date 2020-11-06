Behind the Wall

Behind the wall is a simple website scraper using requests and beautiful soup that pulls text from a website using the command line.

This will output to a file called website.txt. 
    Use this command to easily read this from the command line:  fold -s website.txt 


Main commands: 
    
    short search: {URL} {html tag search term - usually "body"}
    
    deep search: {URL} {html tag search term - usually a class or id name} {class_: True or False} {_id: True or False}

    deep search example: 
    if _id is True:
            entries = soup.find_all( id = search_text )