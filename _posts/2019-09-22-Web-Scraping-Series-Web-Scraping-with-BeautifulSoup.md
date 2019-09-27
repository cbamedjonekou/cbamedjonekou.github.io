---
layout: post
title: "Web Scraping Series: Web Scraping w/ the BeautifulSoup"
date: 2019-09-22
---

**This blog post is the first of a series of blog posts on Web Scraping**. Web Scraping is a very useful/important tool for gathering data off the web for data related tasks/projects. While there are various methods/approaches in which one can accomplish this task, this series will cover how to approach web scraping using python (specifically Python 3). For this particular entry, I will introduce the BeautifulSoup and Request packages and demonstrate how they can be used to extract Wheel of Fortune data from this [link](http://www.angelfire.com/mi4/malldirectories/wheel/wheelbonus.html). By the conclusion of this blog post you should be able to extrapolate what we covered for your own use cases. Let's get started.

## Getting Started:

We will begin by assuming you already have Python 3 installed. [Click here if you don't](https://www.python.org/downloads/). If you do, then the initial step is to check if you have the appropriate packages (and dependencies) installed. We can do this using `pip`, the python package manager. By default it should be installed if you’re using `Python 3.4 (or greater)`. If that is not the case, then you should refer to this [link](https://www.makeuseof.com/tag/install-pip-for-python/) for instructions on how to accomplish this. Otherwise, to install the BeautifulSoup and Requests package complete the following:

<script src="https://gist.github.com/cbamedjonekou/2c631eac175038d7eafa8988fe51bd0e.js"></script>

After that is complete, open up a new file of type `.py` and complete the following:  

<script src="https://gist.github.com/cbamedjonekou/9c6665d55e8dd4ec8ae883f09768c987.js"></script>

The `contextlib` package in the above code segment is installed in your python distribution by default. Once all the above is complete, we can move on the creating our very first scraper.

## Scraping Wheel of Fortune Bonus Round Puzzles:

**Congratulations**, you've made it past the first step. Now we can get down to the nitty gritty: ***How can we scrape the required tables filled with WoF Bonus Round puzzles?*** The first thing we need to do is create functions that perform "HTML get requests" and responses of the requests:

<script src="https://gist.github.com/cbamedjonekou/dc9c4dbc1229ba5772de501ba56e17c1.js"></script>

The `getRequest()` function above performs "HTML get requests" and returns the content given that the page exist. If that's not the case, then the `getRequest()` function returns nothing. If there are any issues performing the request an exception is thrown, and we get an error message that we can understand. Read more about exception handling [here](https://www.pythonforbeginners.com/error-handling/exception-handling-in-python).

The `getRequest()` function is dependent upon the `response()` function in that the response function returns `True` given that the `respnse.status_code equals 200` (**'200' means our link links to a page that exists**). Otherwise, the response function returns `False` since the `respnse.status_code equals 404` (**'404' means our link links to a page that does not exists**). More on status codes in general [here](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes).

<script src="https://gist.github.com/cbamedjonekou/0090d5df30ddb16216e4abcee60dfab6.js"></script>

We use the `getRequest()` function to get the content and save it in a variable named `src` (or `source`, as shown above). Then, we "soupify" or parse the source using the `BeautifulSoup()` constructor. The `BeautifulSoup()` constructor "***works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree***" ([find the documentation here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)).

Now here's the groovy part. Once we parse the link we're interested in, we can pull all the elements of interest. For this particular website, our tables are behind several layers of hyperlinks; The tables are seperated first by year, and then by month. Therefore, the first thing we need to do is find all the `<a>` tags. `<a>` tags are, in essence, the hyperlinks we need to scrape first. We don't want to scrape every single `<a>` tag, however, because some of them are not of interest to us. For example, links that are not of interest to us would be the ***"Angelfire: Build your free website today!"*** link and the navigation links. If you were to right click any link of interest and inspect (as seen in the gif below) you can determine the cooresponding `<a>` tag.

<img src= "https://i.stack.imgur.com/7Wn97.gif" height= "300" width= "700">

So to acquire our links of interest we'll write a conditional statement that selects only the years (which are also hyperlinks) on the page. This is done in a round about way by skipping over any `link.text` (text between the `<a>` tags) that are new line characters and the word *'back'* as it is a navigation link. If the link is what we're looking for then we'll append it (grabbed using the .attrs['href'] attribute; `'href'` is assigned the address) to an empty list called `container`. The expected output should be the following:

<img src= "/assets/seg1_output.png" id= "above" height= "300" width= "700">

We now have the first layer of links. We will have to scrape these links as well to get the second layer of links: the months for each year. The code to scrape these links will be similar to the one above. This is shown below:

<script src="https://gist.github.com/cbamedjonekou/49ee4e32bc68f1ece5165fb257c7e630.js"></script>

The result will look a lot like the list of links (but with more links) pictured <a href="above">above</a>.

We've reached the 
