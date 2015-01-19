import requests  
from lxml import html  
import sys  
import urlparse
from PIL import Image
import os

strl ="http://www.hackett.com/catalog/product/view/id/161407/category/12/?color=37"
strL = strl.split(",")
text=""
for elem in strL:
    i=0
    response = requests.get(elem) ## website name
    #print("response= ",response)
    parsed_body = html.fromstring(response.text)
    #print("pb= ",parsed_body)

    # Grab links to all images
    images = parsed_body.xpath('//img/@src')
    #print(images)
    if not images:  
        sys.exit("Found No Images")

    # Convert any relative urls to absolute urls
    images = [urlparse.urljoin(response.url, url) for url in images]
    print ('Found %s images' % len(images))

    
    for url in images[0:100]:## number of pictures to scrape
        print url
        r = requests.get(url)
        #print(r)
        f = open('pics/%s' % (url.split('/')[-1]+".png"), 'w') ## folder name
        b = r.content
        f.write(b)
        #i=i+1
        f.close()
        nm = "pics/"+(url.split('/')[-1]+".png")
        im = Image.open(nm)
        zing = nm+" , "+elem+"\n"

        width,height= im.size # returns (width, height) tuple
        print im.size
        if ((width < 401) and (height<400)):
            os.remove(nm)
            zing = ""
            
    text = text + zing
with open("clothname.txt", "a") as myfile:
    myfile.write(text+"\n")
