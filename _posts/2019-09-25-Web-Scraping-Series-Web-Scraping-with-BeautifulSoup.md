---
layout: post
title: "Web Scraping (A Series): Web Scraping w/ the BeautifulSoup and Requests Packages"
date: 2019-12-17
description: A blog post from a series of blog posts on Web Scraping using Python. Introduces the BeautifulSoup and Request packages and demonstrates how they can be used to extract Wheel of Fortune data from a WoF Bonus Round Puzzle repo.
tags: wheel-of-fortune web-scraping beautifulsoup requests python3
---

<br>
<div id= "Table-of-Contents">
<h2 id= "ToC">Table of Contents:</h2>
    <ul>
        <li><a href="#Intro">Introduction</a></li>
        <li><a href="#Prereq">Prerequisites</a></li>
        <li><a href="#GetStart">Getting Started</a></li>
        <li><a href="#ScraperOverview">Scraping Wheel of Fortune Bonus Round Puzzles</a>
            <ul>
                <li><a href= "#Part0">Part 0: Setting up our functions</a></li>
                <li><a href= "#Part1">Part 1: Scraping the First Layer (Years)</a></li>
                <li><a href= "#Part2">Part 2: Scraping the Second Layer (Months)</a></li>
                <li><a href= "#Part3">Part 3: Scraping our Tables</a></li>
            </ul>
        </li>
        <li><a href="#Conclusion">Conclusion</a></li>
    </ul>
</div>
<br>

<h2 id= "Intro">Introduction:</h2>

* <strong><a href= "#ToC">Back to Table of Contents:</a></strong>

**This blog post is the first of a series of blog posts on Web Scraping**. Web Scraping is a very useful/important tool for gathering data off the web for data related tasks/projects. While there are various methods/approaches in which one can accomplish this task, this series will cover how to approach web scraping using Python (specifically Python 3). For this particular entry, I will introduce the BeautifulSoup and Request packages and demonstrate how they can be used to extract Wheel of Fortune data from this [link](http://www.angelfire.com/mi4/malldirectories/wheel/wheelbonus.html). By the conclusion of this blog post you should be able to extrapolate what we covered for your own use cases. Let's get started.

<h2 id="Prereq">Prerequisites:</h2>

* <strong><a href= "#ToC">Back to Table of Contents:</a></strong>

It would be very helpful if you have a basic understanding of the following:

* HTML (HyperText Markup Language)
* Python 3

If not you can visit [here](https://www.youtube.com/playlist?list=PL4cUxeGkcC9ibZ2TSBaGGNrgh4ZgYE6Cc) for an introduction to HTML and [here](https://www.youtube.com/playlist?list=PL4cUxeGkcC9idu6GZ8EU_5B6WpKTdYZbK) for an introduction to Python 3.  

<h2 id="GetStart">Getting Started:</h2>

* <strong><a href= "#ToC">Back to Table of Contents:</a></strong>

We will begin by assuming that Python 3 is already installed. [Click here if it has not been previously installed](https://www.python.org/downloads/). Otherwise, the initial step is to check if you have the appropriate packages (and dependencies) installed. We can do this using `pip`, the python package manager. By default it should be installed if you’re using `Python 3.4 (or greater)`. If that is not the case, then you should refer to this [link](https://www.makeuseof.com/tag/install-pip-for-python/) for instructions on how to accomplish this. Otherwise, to install the BeautifulSoup and Requests packages complete the following:

```python
pip install beautifulsoup4
pip install request
```

After that is complete, open up a new file of type `.py` and complete the following:  

```python
# Required Package Imports
from requests import get
from requests.exceptions import RequestException  
from contextlib import closing
from bs4 import BeautifulSoup
```

The `contextlib` package in the above code segment is installed in your python distribution by default. Once all the above is complete, we can move on to creating our very first scraper.

<h2 id="ScraperOverview">Scraping Wheel of Fortune Bonus Round Puzzles:</h2>

* <strong><a href= "#ToC">Back to Table of Contents:</a></strong>

<h3 id= "Part0">Part 0: Setting up our functions</h3>

**Congratulations**, you've made it past the first step. Now we can get down to the nitty gritty: ***Scraping the required tables filled with WoF Bonus Round puzzles.*** The first thing we need to do is create functions that perform "HTML get requests" and responses of those requests:

```python
# Scraper functions created using Beautifulsoup and Request modules

def getRequest(link):
    '''Performs a simple HTML Get request. Involves some exception handling.
    Therefore, if we get a valid reponse, we return the content. 
    Otherwise nothng gets returned.'''
    try:
        with closing(get(link, stream= True)) as resp:
            if response(resp):
                return resp.content
            else:
                return None

    except RequestException as logErr:
        print('Error during request to {} \n'.format(link))
        print('Error merssage: {}'.format(str(logErr)))

def response(respnse):
    """Returns the response of the HTML get request. Returns true given that 
    the status code equals 200 (a successful get request). Returns false given 
    that the status code equals 404 (failed get request/page doesn't exist)."""
    if respnse.status_code == 200:
        return True
    else:
        return False
```

The `getRequest()` function above performs "HTML get requests" and returns the content given that the page exist. If that's not the case, then the `getRequest()` function returns nothing. If there are any issues performing the request an exception is thrown, and we get an error message that we can understand. Read more about exception handling [here](https://www.pythonforbeginners.com/error-handling/exception-handling-in-python).

The `getRequest()` function is dependent upon the `response()` function in that the `response()` function returns `True` given that the `respnse.status_code equals 200` (**'200' means our hyperlink links to a page that exists**). Otherwise, the response function returns `False` since the `respnse.status_code equals 404` (**'404' means our hyperlink links to a page that does not exists**). More on status codes (in general) [here](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes).

```python
# Part 1: Scraping Outer Links

wofLink = 'http://www.angelfire.com/mi4/malldirectories/wheel/wheelbonus.html'
src = getRequest(wofLink)
soup = BeautifulSoup(src, 'lxml')
links = soup.find_all('a')

container = []
for link in links:
    if type(link.text) is str:
        if link.text == '\n\n' or link.text == 'Back home':
            continue
        else:
            container.append(link.attrs['href'])
    else:
        continue

print(container, '\n')
print('# of links: ',len(container), '\n\n')
```

<h3 id= "Part1">Part 1: Scraping the First Layer (Years)</h3>

* <strong><a href= "#ToC">Back to Table of Contents:</a></strong>

We use the `getRequest()` function to get the content and save it in a variable named `src` (or `source`, as shown above). Then, we "soupify" or parse the source using the `BeautifulSoup()` constructor. The `BeautifulSoup()` constructor "***works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree***" ([find the documentation here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)).

Now here's the groovy part. Once we parse the link we're interested in, we can pull all the elements of interest. For this particular website, our tables are behind several layers of hyperlinks; The tables are separated first by year, and then by month. Therefore, the first thing we need to do is find all the `<a>` tags. `<a>` tags are, in essence, the hyperlinks we need to scrape first. We don't want to scrape every single `<a>` tag, however, because some of them are not of interest to us. For example, links that are not of interest to us would be the ***"Angelfire: Build your free website today!"*** link and the navigation links. If you were to right click any link of interest and inspect (as seen in the gif below) you can determine the cooresponding `<a>` tag.

<img src= "https://i.stack.imgur.com/7Wn97.gif" height= "300" width= "700">

So to acquire our links of interest we'll write a conditional statement that selects only the years (which are also hyperlinks) on the page. This is done in a round about way by skipping over any `link.text` (text between the `<a>` tags) that are new line characters and the word *'back'* as it is a navigation link. If the link is what we're looking for then we'll append it (grabbed using the .attrs['href'] attribute; `'href'` is assigned the address) to an empty list called `container`. The expected output should be the following:

<img src= "/assets/screen-shots/seg1_output.png" id= "seg1" height= "300" width= "700">

<h3 id= "Part2">Part 2: Scraping the Second Layer (Months)</h3>

* <strong><a href= "#ToC">Back to Table of Contents:</a></strong>

We now have the first layer of links. We will have to scrape these links as well to get the second layer of links: the months for each year. The code to scrape these links will be similar to the one above. This is shown below:

```python
# Part 2: Scraping nested links  
count = 1
cupboard = []
for elem in container:
    src = getRequest(elem)
    soup = BeautifulSoup(src, 'lxml')
    links_ = soup.find_all('a')
    count += 1
    
    jar = []
    for link in links_:
        if type(link.text) is str:
            if link.text == '\n\n' or link.text == 'Back':
                continue
            else:
                jar.append(link.attrs['href'])
        else:
            continue
    cupboard.append(jar)
```

The result will look a lot like the list of links (but with more links) pictured <a href="#seg1">above</a>.

<h3 id= "Part3">Part 3: Scraping our Tables</h3>

* <strong><a href= "#ToC">Back to Table of Contents:</a></strong>

Now that we have our second layer of hyperlinks, we can obtain our tables. We will employ code similar to the one we use to scrape the site for the first and second layer of links, scraping each link in the list via a loop. The difference, however, is that we no longer are looking for `<a>` tags. We want the `<table>` tag as it references the tables of interest. After obtaining these tables, we will convert each HTML table into a pandas dataframe and write them to a file of the `.csv` (comma separated value) type. This is done by converting each table to a string and passing them through the `pd.read_html()` method ([more about it here](https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.read_html.html)). The `pd.read_html()` method returns a list of dataframes which we then can output to files of the `.csv` (comma separated value) type.

```python
#Part 3: Scraping Tables & converting them to pandas dataframes
urn_ = []
for shelve in cupboard:
    for ingredient in shelve:
        # print(ingredient, '\n')
        src = getRequest(ingredient)
        if src == None:
            continue
        else:
            soup = BeautifulSoup(src, 'lxml')
            tables = soup.find_all('table')
            urn_.append(tables)

count = 1
for holders in urn_:
    for table in holders:
        dataframes = pd.read_html(str(table), flavor= 'bs4', header= 0)
        for df in dataframes:
            file_path = '/Users/Chris/Desktop/WoF Final Round Puzzles/bs4/WoFTable' + str(count) + '.csv'
            df.to_csv(file_path, index= False)
            count += 1
```

<img src= "/assets/screen-shots/seg2_output.png" id= "seg2" height= "300" width= "700">

And that's it. We have successfully scraped all the available Wheel of Fortune bonus round tables from our [link](http://www.angelfire.com/mi4/malldirectories/wheel/wheelbonus.html) of interest.

<h2 id= "Conclusion">Conclusion:</h2>

* <strong><a href= "#ToC">Back to Table of Contents:</a></strong>

This is a pretty simple example of using the BeautifulSoup  and Requests packages to scrape table data off the [WoF Bonus Round Puzzles](http://www.angelfire.com/mi4/malldirectories/wheel/wheelbonus.html) web page. If you're interested in the analysis of the table data [click here](). For more web scraping with python [click here]().
