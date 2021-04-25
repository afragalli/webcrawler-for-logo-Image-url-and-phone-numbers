# Webcrawler for Logo Image URL and Phone Numbers

This is an application that, given a list of website URLs as input, visits and searches them for the websites' logo image URLs and all phone numbers present on the websites.

Please, note that in this current version we don't handle Flash websites, websites generated dynamically through Javascript, phone numbers represented as images on the website or any other similar scenario.

## Usage

First, you will need to install Python 3.5+ on your machine, then pip install the dependencies:
`pip install -r requirements.txt`

Then, running the webcrawler is just a matter of calling `python3 webcrawler.py input_file.txt` from this repository root, where "input_file.txt" is a list of websites URLs, one per line.

The standard output for each website is terminal print of a dictionary(JSON format) with the following keys:
- logo: Website's logo image URL.
- phones: All phone numbers found on the website.
- website: Input URL.

If an http error occours, the output will be a terminal print of the error status code and the website inputed.

## Current Methods

This application process the inputs concurrently and was made to be as generic as possible. The problem of working with unknown websites is that you need to use nonspecific strategies to retrieve the information, which may compromise the accuracy of the results.

### Logo Image

To find the logo image, this application searches for the string 'logo' through the classes and tags from the parsed HTML. If positive, then corrects eventualities according the case to output an absolute URL and tests if the image URL extracted is valid.

### Phone Numbers

For the phone numbers, this application searches the text of the parsed HTML using regular expression for the following generic worldwide phone pattern: The number can start with the country code (plus sign followed by up to three digits), then it can have an area code inside or not a parentheses, and finally the line number. The number can also use spaces, points and dashes to separate the digits.
After the search the numbers are formated to replace any characters that are not digits, a plus sign or parentheses with whitespaces, and then are filtered to have at least 10 characters, excluding the spaces. This is done to remove false positives such as postal codes, as there are no countries with fewer than seven digits if you count the country code, reaching at least ten characters if you also count the plus sign and the parenthesis.

More info: https://en.wikipedia.org/wiki/Telephone_numbering_plan , https://en.wikipedia.org/wiki/E.164 , https://en.wikipedia.org/wiki/List_of_mobile_telephone_prefixes_by_country