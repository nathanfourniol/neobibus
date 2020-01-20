import urllib.request 
from html.parser import HTMLParser

sock = urllib.request.urlopen("https://www.bibus.fr/fr/se-deplacer/infos-trafic") 
htmlSource = sock.read()                            
sock.close()                                        

soup = BeautifulSoup(htmlSource)
for p in soup.find_all('p'):
    print p.get("class")



    
 
if __name__ == "__main__":
        p = BaseParser()
        p.feed(htmlSource)
#print(htmlSource)          
