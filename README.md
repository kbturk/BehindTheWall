# 🧱 Behind the Wall 🧱

Behind the wall is a simple website scraper using requests and beautiful soup that pulls text from a website using the command line.

This will output to a file called website.txt.

## Main commands: 
    
    short search: {html tag search term - usually "body"} {URL} 
    
    class or id search: {-c | --class | -i | --id } {html tag search term - usually a class or id name} {URL} 

## Examples:
   ```
   >python BehindTheWall.py -c references https://en.wikipedia.org/wiki/Platform_game
   ```
   ```
   >python BehindTheWall.py body https://en.wikipedia.org/wiki/Platform_game
   ```
### Success:
   ```
   site scraping is complete. To view results, please open website.txt or
    you can view in the terminal using something like: `fold -s website.txt`
    ```
