import sys, json, requests, re, concurrent.futures, time
from bs4 import BeautifulSoup

def web_info(url):

    # Output informations.
    infos = {"logo":'', "phones":[], "website": url}

    # Html extraction and parse.
    html = requests.get(url)
    if(html.status_code//100 != 2): # Status code starting with a 2 generally indicates success.
        print("Error Code:",html.status_code, 'website:',url)
        return
    soup = BeautifulSoup(html.content, "html.parser")

    # Search for the logo image.
    image_tags = soup.findAll('img')
    for image_tag in image_tags: # Search for 'logo' through the classes and tags. If positive, then correct eventualities according the case.
        if('logo' in (str(image_tag.get('class'))+image_tag.get('src')).lower()):
            if any(x in image_tag.get('src') for x in ['.com', '.net', '.org', '.co', '.us', '.eu', '.blog']): # Most common domain extensions.
                img_url = image_tag.get('src')
                if 'http' not in img_url: img_url = 'http:' + img_url
            else:
                img_url = 'http://'+url.split('/')[2]+'/'+image_tag.get('src').replace('//','')
            img_html = requests.get(img_url) # Check if it is a valid url for the logo.
            if(img_html.status_code//100 == 2):
                infos['logo'] = img_url
                break

    # Search for the phone numbers.
    phone_patterns = "\+?[\d ]{0,3}\(?\d{1,3}\)?[\. \d-]+\)?" # Most common phone patterns.
    phone_nums = re.findall(phone_patterns, soup.text) # Search for possible phone patterns via regugular expression through the text.
    phones = list(set(map(lambda x:re.sub(r"[^\d \(\)+]"," ",x.strip()),phone_nums))) # Format corrections.
    phones = list(filter(lambda x:len(x.replace(' ',''))>9, phones)) # Remove cases with less than 10 valid characters.
    infos['phones'] = phones

    # Output print and return.
    print(infos)
    return(infos)

if __name__ == '__main__':
    
    start_time = time.time() # Time counter variable.

    # Read and format the inputs.
    url_inputs = [line.rstrip('\r\n') for line in sys.stdin]

    # Concurrent execution.
    output_data = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(web_info, url) for url in url_inputs]

        for f in concurrent.futures.as_completed(results):
            if(f.result()): # Check if result is not None.
                output_data.append(f.result())

    # Save the results, one per line, unordered and in JSON format in 'output_data' file.
    with open('output_data', 'w') as outfile:
        for data in output_data:
            outfile.write(json.dumps(data)+'\n')
    
    print("Finished in %s seconds" % (round(time.time() - start_time, 2))) # Total time of execution print.
