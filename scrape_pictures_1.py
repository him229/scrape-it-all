import mechanize
import extraction
import requests  
from lxml import html  
import sys  
import urlparse
from PIL import Image
import os


######

def grab_my_pictures(final_link):#iterates through the urls and pulls down picture

    strl =final_link
    strL = strl.split(",")
    text=""
    for elem in strL:
        i=0
        response = requests.get(elem) ## replace with the website name
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
            r = requests.get(url)
            #print(r)
            f = open('pics/%s' % (url.split('/')[-1]+".png"), 'w') ## folder name
            b = r.content
            f.write(b)
            #i=i+1
            f.close()
            nm = "pics/"+(url.split('/')[-1]+".png")
            im = Image.open(nm)
            htmll = requests.get(elem).text
            extracted = extraction.Extractor().extract(htmll, source_url=elem)
            titleh = extracted.title
            zing = nm+" , "+titleh+","+elem+"\n"

            width,height= im.size # returns (width, height) tuple
            print im.size
            if ((width < 300) and (height < 300)):
                os.remove(nm)
                zing = ""
        text = text + zing
    with open("clothname.txt", "a") as myfile:
        myfile.write(text+"\n")

#####
        
website_name = raw_input("Please enter the name of the website ")

list_of_links = []
br = mechanize.Browser()
br.set_handle_robots(False)
response = br.open(website_name) #mechanzie code

#checks and returns all the webpage links
for link in br.links():
    print (link.url) #test for every url link
    list_of_links.append(link.url) #adds the url linsk to a list

list_of_links.pop(1)
list_of_links.pop(1)
pres = ""
partof = raw_input("Enter part ")
for item in list_of_links:
    #final_link = final_website + item
    if partof in item:
        pres = pres +"http://"+item+","
pres = pres[0:-1]
#print pres
grab_my_pictures(pres)
    

