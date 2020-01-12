import urllib.request 
import HTMLParser

sock = urllib.request.urlopen("https://www.bibus.fr/fr/se-deplacer/infos-trafic") 
htmlSource = sock.read()                            
sock.close()                                        


class BaseParser(HTMLParser.HTMLParser):
	def handle_starttag(self, tag, attrs):
		print("start tag:",tag)
		print("attributes:",attrs)
 
	def handle_endtag(self, tag):
		print("end tag:",tag)
 
	def handle_data(self, data):
		print("data:",data)
 
if __name__ == "__main__":
        p = BaseParser()
        p.feed(htmlSource)
#print(htmlSource)          
