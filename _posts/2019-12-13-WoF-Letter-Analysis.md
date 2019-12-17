---
layout: post
mathjax: true
title: "Wheel of Fortune: Bonus Round Puzzle Analysis"
date: 2019-11-13
description: A blog post on the Analysis of Wheel of Fortune Bonus Round puzzles. We briefly cover natural language processing subject matter such as language models as we go through our analysis. We hope to gain some insights that we can visual and then exploit later on when we build our Neural Network.
tags: machine-learning artificial-intelligence natural-language-processing tensorflow python3
---
<h2 id="Introduction">Introduction</h2>

For this post, we'll do some Exploratory Data Analysis on the Wheel of Fortune Bonus Round Puzzle data we scraped <a href="https://cbamedjonekou.github.io/blog/2019/09/25/Web-Scraping-Series-Web-Scraping-with-BeautifulSoup">here</a>. We'd like to analyze the frequencies of letters as the appear within our data. This includes but is not limited to frequency independent of phrase length, or category.  

<div id="Table-of-Contents">
  <h3 id="Contents">Contents</h3>
  <ol>
      <li><a href="#Prerequisites">Prerequisites</a></li>
      <li><a href="#Packages">Packages</a></li>
      <li><a href="#DWC">Data Wrangling/Cleaning</a></li>
      <li><a href="#EDA">Exploratory Data Analysis</a>
          <ul>
              <li><a href="#2nd-order-approx">$2$-$nd$ Order Approximations</a></li>
              <li><a href="#3rd-order-approx">$3$-$rd$ Order Approximations</a></li>
              <li><a href="#1st-order-word">$1$-$st$ Order Word Approximations</a></li>
              <li><a href="#NLTK">Using NLTK to get Parts of Speech</a></li>
              <li></li>
          </ul>
      </li>
  </ol>
</div>

<h2 id="Prerequisites">Prerequisites</h2>

The goal of this post is to give some understanding and insight into analyzing Text Data. We'll accomplish this by giving a concise introduction into a Frequency Analysis along the way. Therefore, it would be helpful if you had some experience with the following:

* Programming Experience, particularly w/ Python 3 and Jupyter Notebooks
* Mathematics, particularly w/ Probability & Statistics

However, these are not strict requirements; Following along will still give you some insights that you can explore in the future.

<h2 id= "Packages">Packages</h2>

To begin we need to import the following packages since we'll need some of their functions later on.


```python
# Package Imports being used to make things happen
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go
import plotly.offline as po
import seaborn as sns
import string
from os import listdir
from os.path import isfile, join

# Special methods/'magic' functions for the visualizations
sns.set()
%matplotlib inline
# po.init_notebook_mode(connected=False)
```

<h2 id= "DWC">Putting the Data Together</h2>

<a href="#Contents">Back to Contents</a>

The data we'll be looking at is the Wheel of Fortune Bonus Round Puzzle data we scraped <a href="https://cbamedjonekou.github.io/blog/2019/09/25/Web-Scraping-Series-Web-Scraping-with-BeautifulSoup">here</a>. The data in question (on my end) is saved in a folder as files of type `.csv` (comma-separated-values). The first thing we'll need to do is pull the tables from this folder and merge them into one table. 

* The following code will handle this action:


```python
# path where files are located
path = '/Users/Chris/Desktop/WoF Final Round Puzzles/bs4'

# Getting a list of files in path
directory_contents = listdir(path)

# Sorting the files
stripped_directory_contents = []
for elem in directory_contents:
    stripped_directory_contents.append(int(elem.strip('WoFTable.csv')))
    
stripped_directory_contents.sort()

filepath = []
for elem in stripped_directory_contents:
    filename = 'WoFTable'+ str(elem) +'.csv'
    if isfile(join(path, filename)):
        filepath.append(join(path, filename))
        
# Importing dataframes and merging
for file in filepath:
    if filepath.index(file) == 0:
        WoF_DF = pd.read_csv(file)
    else:
        generic_DF = pd.read_csv(file)
        WoF_DF = pd.concat([WoF_DF, generic_DF], ignore_index= True, sort= False)
```

* `WoF_DF` now contains our merged table. The following code writes the table to a new file. This is optional, of course. 


```python
# Function for exporting tables
def exportTable(path, dataframe):
    with open(path, 'w') as f:
        dataframe.to_csv(path_or_buf= f, index= False)


filepath = '/Users/Chris/Desktop/WoF Final Round Puzzles/WoF_Merged.csv'
exportTable(filepath, WoF_DF)
```

Now that we have all scraped tables merged into one, let's get some preliminary information from our new dataframe. We'll use the `.info()` for this task.  


```python
WoF_DF.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4285 entries, 0 to 4284
    Data columns (total 8 columns):
    DATE          3638 non-null object
    CATEGORY      3050 non-null object
    PUZZLE        3050 non-null object
    LETTERS       2874 non-null object
    PRIZE         2916 non-null object
    WIN           3019 non-null object
    COMMENTS      1007 non-null object
    Unnamed: 7    1 non-null object
    dtypes: object(8)
    memory usage: 267.9+ KB


The output of the `.info()` method shows that we are missing some values in our table. To perform frequency analysis on the data, we have to tidy it up. We want to get rid of all missing values as they will not contribute in anyway. Let's get a quick look at the first ten elements of the data using the `.head()` method. 


```python
WoF_DF.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DATE</th>
      <th>CATEGORY</th>
      <th>PUZZLE</th>
      <th>LETTERS</th>
      <th>PRIZE</th>
      <th>WIN</th>
      <th>COMMENTS</th>
      <th>Unnamed: 7</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5 September 1988</td>
      <td>Phrase</td>
      <td>OPEN YOUR EYES</td>
      <td>R S T L N E</td>
      <td>Corvette</td>
      <td>Yes</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6 September 1988</td>
      <td>Person</td>
      <td>LIZA MINNELLI</td>
      <td>R S T L N E</td>
      <td>$25,000</td>
      <td>Yes</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>7 September 1988</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>8 September 1988</td>
      <td>Phrase</td>
      <td>PUT ON THE SPOT</td>
      <td>S T R L N E</td>
      <td>$25,000</td>
      <td>No</td>
      <td>That sounds awkward and disjointed. Shouldn't ...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>9 September 1988</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>12 September 1988</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>13 September 1988</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>14 September 1988</td>
      <td>Place</td>
      <td>TOMBSTONE ARIZONA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>15 September 1988</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



Right off the bat there are two columns we can drop:`"Unnamed: 7"`, and `"COMMENTS"` columns. We drop the `"Unnamed: 7"` column because we don't know what it represents and there's only 1 non-null (not missing) value in the column. We also drop the `"COMMENTS"` column because the comments describing the bonus round on a particular night have no bearing on our analysis. We'll use the `.drop()` method to complete this action.


```python
WoF_DF = WoF_DF.drop(["Unnamed: 7","COMMENTS"], axis= 1)
WoF_DF.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DATE</th>
      <th>CATEGORY</th>
      <th>PUZZLE</th>
      <th>LETTERS</th>
      <th>PRIZE</th>
      <th>WIN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5 September 1988</td>
      <td>Phrase</td>
      <td>OPEN YOUR EYES</td>
      <td>R S T L N E</td>
      <td>Corvette</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6 September 1988</td>
      <td>Person</td>
      <td>LIZA MINNELLI</td>
      <td>R S T L N E</td>
      <td>$25,000</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>2</th>
      <td>7 September 1988</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>8 September 1988</td>
      <td>Phrase</td>
      <td>PUT ON THE SPOT</td>
      <td>S T R L N E</td>
      <td>$25,000</td>
      <td>No</td>
    </tr>
    <tr>
      <th>4</th>
      <td>9 September 1988</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



We can also drop `"PRIZE"` because we care mostly that they won, not 'what' or 'how much' they won.


```python
WoF_DF = WoF_DF.drop(["PRIZE"], axis= 1)
WoF_DF.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DATE</th>
      <th>CATEGORY</th>
      <th>PUZZLE</th>
      <th>LETTERS</th>
      <th>WIN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5 September 1988</td>
      <td>Phrase</td>
      <td>OPEN YOUR EYES</td>
      <td>R S T L N E</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6 September 1988</td>
      <td>Person</td>
      <td>LIZA MINNELLI</td>
      <td>R S T L N E</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>2</th>
      <td>7 September 1988</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>8 September 1988</td>
      <td>Phrase</td>
      <td>PUT ON THE SPOT</td>
      <td>S T R L N E</td>
      <td>No</td>
    </tr>
    <tr>
      <th>4</th>
      <td>9 September 1988</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



The last thing we'll do is remove all rows with missing values. If we don't have data for even one entry of the remaing columns, the row will be of no use in our frequency analysis, therefore we'll drop them. To complete that action we'll use the `.dropna()` method. 


```python
WoF_DF = WoF_DF.dropna()
WoF_DF.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DATE</th>
      <th>CATEGORY</th>
      <th>PUZZLE</th>
      <th>LETTERS</th>
      <th>WIN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5 September 1988</td>
      <td>Phrase</td>
      <td>OPEN YOUR EYES</td>
      <td>R S T L N E</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6 September 1988</td>
      <td>Person</td>
      <td>LIZA MINNELLI</td>
      <td>R S T L N E</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>3</th>
      <td>8 September 1988</td>
      <td>Phrase</td>
      <td>PUT ON THE SPOT</td>
      <td>S T R L N E</td>
      <td>No</td>
    </tr>
    <tr>
      <th>22</th>
      <td>30 September 1988</td>
      <td>Thing</td>
      <td>FIRST PRIZE</td>
      <td>S T L N D E</td>
      <td>No</td>
    </tr>
    <tr>
      <th>24</th>
      <td>4 October 1988</td>
      <td>Place</td>
      <td>THE VATICAN</td>
      <td>C D M A</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>
</div>



Wheel of Fortune is known to have some episodes that are either reruns or anniversary episodes. Those events (rows) have no usable data for us so we'll remove them. We can choose any column to search for them; The column chosen will be `"CATEGORY"`. We'll use the `.unique()` method to weed them out.  


```python
WoF_DF["CATEGORY"].unique()
```




    array(['Phrase', 'Person', 'Thing', 'Place', 'Title', 'Things', 'People',
           'Event', 'Occupation', 'Slang', 'Fictional Character', 'Landmark',
           'Reruns aired the week of December 30.',
           '3,000th episode. No gameplay, just clips.', 'On the Map',
           'Proper Name', 'Around the House', 'Living Things', 'Rhyme Time',
           'Living Thing', 'Fictional Characters',
           '4000th episode — No gameplay, just clips. This was rerun with the above Monday-Thursday episodes in Summer 2004. Weird.',
           'Around The House', 'On The Menu', 'On The Map', 'Classic TV',
           'On the Menu', 'Show Biz', 'Fun & Games', 'Song Lyrics',
           'Best Seller', 'In the Kitchen', 'Food & Drink',
           'What Are You Doing?', 'Fictional Place', 'Places', 'Quotation'],
          dtype=object)



We found that 3 pieces of data that will not make any contribution to our dataset, and analysis:  `['Reruns aired the week of December 30.','3,000th episode. No gameplay, just clips.', '4000th episode — No gameplay, just clips. This was rerun with the above Monday-Thursday episodes in Summer 2004. Weird.']`. So, we'll drop them. 


```python
# list of items to remove from dataset
to_remove = ['Reruns aired the week of December 30.',
             '3,000th episode. No gameplay, just clips.', 
             '4000th episode — No gameplay, just clips. This was rerun with the above Monday-Thursday episodes in Summer 2004. Weird.']

# loop to remove them
for i in range(len(to_remove)):
    index_to_drop = WoF_DF[WoF_DF['CATEGORY'] == to_remove[i]].index.values[0]
    WoF_DF = WoF_DF.drop(index_to_drop)
```

To check if the items in the `to_remove` list has been removed we'll run the following code cell again. Notice that the items in the `to_remove` list no longer appear.


```python
WoF_DF["CATEGORY"].unique()
```




    array(['Phrase', 'Person', 'Thing', 'Place', 'Title', 'Things', 'People',
           'Event', 'Occupation', 'Slang', 'Fictional Character', 'Landmark',
           'On the Map', 'Proper Name', 'Around the House', 'Living Things',
           'Rhyme Time', 'Living Thing', 'Fictional Characters',
           'Around The House', 'On The Menu', 'On The Map', 'Classic TV',
           'On the Menu', 'Show Biz', 'Fun & Games', 'Song Lyrics',
           'Best Seller', 'In the Kitchen', 'Food & Drink',
           'What Are You Doing?', 'Fictional Place', 'Places', 'Quotation'],
          dtype=object)



* `WoF_DF` now contains our cleaned table. The following code writes the table to a new file. This is optional, of course. 


```python
filepath = '/Users/Chris/Desktop/WoF Final Round Puzzles/WoF_Merged_cleaned.csv'
with open(filepath, 'w') as f:
    WoF_DF.to_csv(path_or_buf= f, index= False)
```

<h2 id="EDA">Exploratory the Data</h2>

We completed cleaning our dataset. It now contains all relevant data we'll use for our Frequency Analysis. First thing we should do is get some baseline information about our new dataset. 


```python
WoF_DF = pd.read_csv(filepath)
WoF_DF.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 2868 entries, 0 to 2867
    Data columns (total 5 columns):
    DATE        2868 non-null object
    CATEGORY    2868 non-null object
    PUZZLE      2868 non-null object
    LETTERS     2868 non-null object
    WIN         2868 non-null object
    dtypes: object(5)
    memory usage: 112.1+ KB


Looks like we have 2868 rows filled with Wheel of Fortune Bonus Round Puzzles. Our dataset should contain Bonus Round Puzzles from 1988 to 2016. What we're concerned with is the frequency of each letter present within in each puzzle across that time span. 
The column we want to focus on, and extract information from, is the `"PUZZLE"` column.


```python
WoF_DF['PUZZLE'].head(10)
```




    0        OPEN YOUR EYES
    1         LIZA MINNELLI
    2       PUT ON THE SPOT
    3           FIRST PRIZE
    4           THE VATICAN
    5    FLYING DOWN TO RIO
    6            POGO STICK
    7         YANKEE DOODLE
    8       FINGER PAINTING
    9            JOE NAMATH
    Name: PUZZLE, dtype: object



We can do this by converting this column into a giant string of characters that will act as a corpus (or body of text). We do this with the following code.


```python
# Step 1: Create a string of text representing all solved bonus round puzzles.
corpus = ''.join(WoF_DF['PUZZLE'])
```

***Note: The following code was used to remove whitespace from the string. At the time whitespace seemed unnecessary but according to Shannon it serves a purpose (indicates beginning/end of a word). The code is commented out but I'll keep it here since it may still serve a purpose. For now leave it commented.***


```python
# Step 2(: Remove the whitespace as they're not important to our analysis right now.
# corpus = corpus.translate({ord(c): None for c in string.whitespace})
```

Now have our corpus. Using the `len()` function, we find that the length of our string is 33099 characters. This will be a relevant number for future calculations.


```python
len(corpus)
```




    33099



We expect this `corpus` to have all 26 letters of the alphabet in varying frequency. However, it's always good to check. First, we'll convert our list into a numpy array and use its `.unique()` method. 


```python
# Creates an array containing each character in the corpus
corpus_index = np.array([char for char in corpus])

# Finds/Returns an array of unique values
corpus_index = np.unique(corpus_index)
print(corpus_index)
```

    [' ' '&' "'" '-' '?' 'A' 'B' 'C' 'D' 'E' 'F' 'G' 'H' 'I' 'J' 'K' 'L' 'M'
     'N' 'O' 'P' 'Q' 'R' 'S' 'T' 'U' 'V' 'W' 'X' 'Y' 'Z']


Just as we suspected; All 26 letters of the english alphabet appear as unique characters.  We also have additional characters that we did not expect. The additional characters are mostly punctuation and whitespace, but we'll keep them for now since we don't know yet the significance of the punctiation/whitespace. Additionally, punctiation/whitespace is a significant part of English, so their value cannot be understated.

* Now we'll calculate the total amount of each unique character.


```python
# Makes a dictionary: Each character in the corpus index (unique characters in corpus)
# is a 'key' in the dictionary. Each value is initialized to zero
letter_counter = dict((character, 0) for character in corpus_index)

# Begins the counting, adding 1 for each key match
for character in corpus:
    letter_counter[character] += 1
```

* The result of our count


```python
print(letter_counter)
```

    {' ': 3171, '&': 18, "'": 41, '-': 65, '?': 1, 'A': 2490, 'B': 1072, 'C': 988, 'D': 1038, 'E': 2258, 'F': 926, 'G': 1308, 'H': 1393, 'I': 2396, 'J': 212, 'K': 722, 'L': 1086, 'M': 656, 'N': 1406, 'O': 2834, 'P': 1033, 'Q': 116, 'R': 1514, 'S': 1097, 'T': 1472, 'U': 1346, 'V': 492, 'W': 767, 'X': 117, 'Y': 926, 'Z': 138}


Based on our results, looks like the letters `EAIOTR` (in no particular order) appear the most in our corpus. Whitespace which indicates the beginning/end of a word also appears in abundance. We'll use this first count as a springboard to create our new dataframe. We'll start by separating  our key/value pairs and creating a dataframe having the columns `Symbol` and `Frequency`.


```python
# Separating the key/value pairs of our dictionary
letters = list(letter_counter.keys())
frequency = list(letter_counter.values())

# Creating a dataframe called WoF_Letter_dist
wof_unigram_dist = pd.DataFrame.from_dict({'Symbol': letters,'Frequency': frequency})

# First 10 rows
wof_unigram_dist.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Symbol</th>
      <th>Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td></td>
      <td>3171</td>
    </tr>
    <tr>
      <th>1</th>
      <td>&amp;</td>
      <td>18</td>
    </tr>
    <tr>
      <th>2</th>
      <td>'</td>
      <td>41</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-</td>
      <td>65</td>
    </tr>
    <tr>
      <th>4</th>
      <td>?</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>A</td>
      <td>2490</td>
    </tr>
    <tr>
      <th>6</th>
      <td>B</td>
      <td>1072</td>
    </tr>
    <tr>
      <th>7</th>
      <td>C</td>
      <td>988</td>
    </tr>
    <tr>
      <th>8</th>
      <td>D</td>
      <td>1038</td>
    </tr>
    <tr>
      <th>9</th>
      <td>E</td>
      <td>2258</td>
    </tr>
  </tbody>
</table>
</div>



***Optional Table Export***


```python
filepath = '/Users/Chris/Desktop/WoF Final Round Puzzles/WoF_unigram_unordered.csv'
exportTable(filepath, wof_unigram_dist)
```

We'll also use the `sns.barplot()` function to visualize the frequency distribution


```python
# Plotting:
fig = px.bar(wof_unigram_dist, x= 'Symbol', y= 'Frequency')
pio.write_html(fig, file='unigram_unordered.html', auto_open=True)
fig.show()
```

-GRAPH-

For probabilities we'll modifying the line above by dividing each element by total corpus length. We'll also sort the plot by descending order (highest to lowest)

```python
# Sorts dataframe before plotting
wof_unigram_dist = wof_unigram_dist.sort_values(by= ['Frequency'], ascending= False)

# Exports to CSV
filepath = '/Users/Chris/Desktop/WoF Final Round Puzzles/WoF_unigram_ordered.csv'
exportTable(filepath, wof_unigram_dist)

# Plotting:
fig = px.bar(wof_unigram_dist, x= 'Symbol', y= wof_unigram_dist['Frequency']/len(corpus))
pio.write_html(fig, file='unigram_ordered.html', auto_open=True)
fig.show()
```

-GRAPH-

```python
wof_unigram_dist['Frequency'] = wof_unigram_dist['Frequency']/len(corpus)

# Exports to CSV
filepath = '/Users/Chris/Desktop/WoF Final Round Puzzles/unigram_ordered_bar.csv'
exportTable(filepath, wof_unigram_dist)
```

What we have in our table so far are the occurrences of each letter in our corpus independent of puzzle length. Let's now consider puzzle length. We want to look at the frequency of letters given a particular puzzle length. We'll define ***puzzle length*** as number of words in each puzzle. Let's find out the range of lengths to start. 


```python
WoF_DF.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DATE</th>
      <th>CATEGORY</th>
      <th>PUZZLE</th>
      <th>LETTERS</th>
      <th>WIN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5 September 1988</td>
      <td>Phrase</td>
      <td>OPEN YOUR EYES</td>
      <td>R S T L N E</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6 September 1988</td>
      <td>Person</td>
      <td>LIZA MINNELLI</td>
      <td>R S T L N E</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8 September 1988</td>
      <td>Phrase</td>
      <td>PUT ON THE SPOT</td>
      <td>S T R L N E</td>
      <td>No</td>
    </tr>
    <tr>
      <th>3</th>
      <td>30 September 1988</td>
      <td>Thing</td>
      <td>FIRST PRIZE</td>
      <td>S T L N D E</td>
      <td>No</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4 October 1988</td>
      <td>Place</td>
      <td>THE VATICAN</td>
      <td>C D M A</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>5</th>
      <td>25 October 1988</td>
      <td>Title</td>
      <td>FLYING DOWN TO RIO</td>
      <td>C D M O</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>6</th>
      <td>26 October 1988</td>
      <td>Thing</td>
      <td>POGO STICK</td>
      <td>C D M A</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>7</th>
      <td>27 October 1988</td>
      <td>Title</td>
      <td>YANKEE DOODLE</td>
      <td>C D G A</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th>8</th>
      <td>28 October 1988</td>
      <td>Thing</td>
      <td>FINGER PAINTING</td>
      <td>C D P A</td>
      <td>No</td>
    </tr>
    <tr>
      <th>9</th>
      <td>14 November 1988</td>
      <td>Person</td>
      <td>JOE NAMATH</td>
      <td>D M C A</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Part 1: Each element in column are turned to list
# We find length of each list and append them to new list
puzzle_word_length = np.array([len(elem.split(' ')) for elem in WoF_DF['PUZZLE']])

# Part 2 (Optional): Adding to dataframe column called `PUZZLE LENGTH`
WoF_DF['PUZZLE WORD LENGTH'] = puzzle_word_length

# Part 3: Find unique elements
puzzle_word_length_range = np.unique(puzzle_word_length)
puzzle_word_length_range
```




    array([1, 2, 3, 4, 5, 6, 7])



Using the `unique()` function, we have discovered that we have seven different puzzle lengths (based on the amount of words). If we completed the optional step of creating a new column (`PUZZLE WORD LENGTH`), then we can use the groupby().count() to get the amount of puzzles that fit the criteria.


```python
WoF_DF.groupby(['PUZZLE WORD LENGTH']).count()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DATE</th>
      <th>CATEGORY</th>
      <th>PUZZLE</th>
      <th>LETTERS</th>
      <th>WIN</th>
    </tr>
    <tr>
      <th>PUZZLE WORD LENGTH</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>605</td>
      <td>605</td>
      <td>605</td>
      <td>605</td>
      <td>605</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1538</td>
      <td>1538</td>
      <td>1538</td>
      <td>1538</td>
      <td>1538</td>
    </tr>
    <tr>
      <th>3</th>
      <td>565</td>
      <td>565</td>
      <td>565</td>
      <td>565</td>
      <td>565</td>
    </tr>
    <tr>
      <th>4</th>
      <td>140</td>
      <td>140</td>
      <td>140</td>
      <td>140</td>
      <td>140</td>
    </tr>
    <tr>
      <th>5</th>
      <td>18</td>
      <td>18</td>
      <td>18</td>
      <td>18</td>
      <td>18</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



The next thing we want to do is find the distribution of letters given the length of the puzzle (in terms of number of words present). We'll complete this action by running the code below.


```python
# Empty lists to hold the 7 corpora, and the lengths
corpora_holder = []
length_holder = []

# Loop to create list dependent on word length, 
for i in range(1,8):
    # Step 1: Get pandas series for each word length
    testDF = WoF_DF[WoF_DF['PUZZLE WORD LENGTH'] == i]['PUZZLE']
    
    # Step 2: Create a string from pandas series of text representing 
    # solved bonus round puzzles for each word length.
    corpus = ''.join(testDF)
    
    # Step 3: Store our corpora and their lengths
    corpora_holder.append(corpus)
    length_holder.append(len(corpus))

# Empty list to hold our count dictionaries
symbol_count_holder = []

# Loop to count letter frequency given word length 
for corpus in corpora_holder:
    
    # Step 1: Makes a dictionary - Each character in the corpus index 
    # (unique characters in corpus) is a 'key' in the dictionary. 
    # Each value is initialized to zero
    letter_counter = dict((character, 0) for character in corpus_index)
    
    # Step 2: Use loop to begin counting, adding 1 for each key match
    for character in corpus:
        letter_counter[character] += 1
        
    # Step 3: Store resulting count dictionaries in list for later use
    symbol_count_holder.append(letter_counter)
```

Now, we'll plot all the distributions (dependent on puzzle length).


```python
fig, axs = plt.subplots(7, 1, figsize= (10, 30))

# Loop use to plot dataframes
for i in range(len(length_holder)):
    # Step 1: Separating the key/value pairs of our dictionary
    temp_letters = list(symbol_count_holder[i].keys())
    temp_frequency = list(symbol_count_holder[i].values())

    # Step 2: Creating a dataframe called tempDF and sorting it
    tempDF = pd.DataFrame.from_dict({'Symbol': temp_letters,'Frequency': temp_frequency})
    tempDF = tempDF.sort_values(by= ['Frequency'], ascending= False)
    
    
    filepath = '/Users/Chris/Desktop/WoF Final Round Puzzles/word_count_df_' + str(i) + '.csv'
    exportTable(filepath, tempDF)
    
    # Step 3: Plotting temp dataframes
    
    sns.barplot(tempDF['Symbol'], tempDF['Frequency']/length_holder[i], ax= axs.flatten()[i])
```


![png](output_57_0.png)


<h3 id='2nd-order-approx'>$2$-$nd$ Order Approximations</h3>

[Claude Shannon](https://en.wikipedia.org/wiki/Claude_Shannon), father of Information Theory (Mathematical Theory of Communication), formed a mathematical process (and model) demonstrating how English words and text can be approximated and carried out by machines. Most of the distributions shown earlier considers the letters as independent from each other (i.e.: [First-Order Approximations of English text](http://people.seas.harvard.edu/~jones/cscie129/nu_lectures/lecture2/info%20theory/Info_Theory_5.html)). 

We'll begin to look at  [n-Order Approximations of English text](http://people.seas.harvard.edu/~jones/cscie129/nu_lectures/lecture2/info%20theory/Info_Theory_5.html) where $2 \leq n < 4$. ***Digrams*** (or [bigrams](https://en.wikipedia.org/wiki/Bigram)), which are 2 symbol combinations (including white space) will be the first to be considered. 

The first steps are to create bigrams and dictionary of the bigrams to initialize our counter. 


```python
# Step 1: We get the cartesian product of corpus_index w/ itself (they're unique pairs)
bigrams = np.array([x+y for x in corpus_index for y in corpus_index])

# Step 2: Makes a dictionary: Each character in bigrams is a 'key' in the dictionary. 
# Each value is initialized to zero
bigram_counter = dict((character, 0) for character in bigrams)
```

We'll search each element in our `WoF_DF['PUZZLE']` array and count how many times the bigram appears.


```python
# Step 3: Begins the counting, adding 1 for each key match
for elem in WoF_DF['PUZZLE']:
    for bigram in bigrams:
        if bigram in elem:
            bigram_counter[bigram] += 1
```

Now visualize the results. Click the image to get a larger view.


```python
# Creating a dataframe called bigram_dist
symbols = np.array(list(bigram_counter.keys()))
frequencies = np.array(list(bigram_counter.values()))
bigram_dist = pd.DataFrame.from_dict({'Symbol': symbols, 
                                      'X': [x[0] for x in symbols],
                                      'Y': [x[1] for x in symbols],
                                      'Frequency': frequencies})

# Scales the probabilities
bigram_dist['Frequency'] = bigram_dist['Frequency']/frequencies.sum() 

# Optional export
filepath = '/Users/Chris/Desktop/WoF Final Round Puzzles/bigramD3.csv'
exportTable(filepath, bigram_dist[['X', 'Y', 'Frequency']])

# Plots a heatmap
fig = go.Figure(data= go.Heatmap(z= np.transpose(np.array(bigram_dist['Frequency']).reshape(31, 31)), 
                                 x= corpus_index,
                                 y= corpus_index,
                                 colorscale='Viridis'))

fig.update_layout(title='Bigrams', xaxis_nticks= 31)
po.plot(fig, filename='bigram_heatmap.html', auto_open=True)
# pio.write_html(fig, file='bigram_heatmap.html', auto_open=True)
fig.show()
```

-GRAPH-

<h3 id='3rd-order-approx'>$3$-$rd$ Order Approximations</h3>

We'll now consider [trigrams](https://en.wikipedia.org/wiki/Trigram), which is the [n-Order Approximation of English text](http://people.seas.harvard.edu/~jones/cscie129/nu_lectures/lecture2/info%20theory/Info_Theory_5.html) where $n = 3$. Trigrams are 3 symbol combinations (including white space) and will be considered next. 

The first steps are to create trigrams and dictionary of the trigrams to initialize our counter. 


```python
# Step 1: We get the cartesian product of corpus_index w/ itself (they're unique pairs)
trigrams = np.array([x+y+z for x in corpus_index for y in corpus_index for z in corpus_index])

# Step 2: Makes a dictionary: Each character in bigrams is a 'key' in the dictionary. 
# Each value is initialized to zero
trigram_counter = dict((character, 0) for character in trigrams)
```

We'll search each element in our `WoF_DF['PUZZLE']` array and count how many times the trigram appears.


```python
# Step 3: Begins the counting, adding 1 for each key match
for elem in WoF_DF['PUZZLE']:
    for trigram in trigrams:
        if trigram in elem:
            trigram_counter[trigram] += 1
```

Now we'll table the counts and visualize the results. Click the image to get a larger view.


```python
# Creating a dataframe called bigram_dist
symbols_ = np.array(list(trigram_counter.keys()))
frequencies_ = np.array(list(trigram_counter.values()))
trigram_dist = pd.DataFrame.from_dict({'Symbol': symbols_,
                                       'X': [x[0] for x in symbols_],
                                       'Y': [x[1:] for x in symbols_],
                                       'Frequency': frequencies_})

# Scales the probabilities
trigram_dist['Frequency'] = trigram_dist['Frequency']/frequencies_.sum()
                                       
# Optional export
filepath = '/Users/Chris/Desktop/WoF Final Round Puzzles/trigram.csv'
exportTable(filepath, trigram_dist)

# Plots a heat map
three_gram = np.transpose(np.array(trigram_dist['Frequency']).reshape(31, 961))
fig = go.Figure(data= go.Heatmap(z= three_gram, 
                                 x= corpus_index,
                                 y= bigrams,
                                 colorscale='Viridis_r'))

fig.update_layout(title='Trigrams', xaxis_nticks= 961)
po.plot(fig, filename='Trigram_heatmap.html', auto_open=True)
# pio.write_html(fig, file='trigram_heatmap.html', auto_open=True)
fig.show()
```

-GRAPH-

<h3 id="1st-order-word">$1$-$st$ Order Word Approximations</h3>

We'll now consider [1st-Order Word Approximations of English text](http://people.seas.harvard.edu/~jones/cscie129/nu_lectures/lecture2/info%20theory/Info_Theory_5.html). Each word is considered independent in 1st-Order Word Approximations but maintain their relative frequency w/ regard to English text. We'll construct the frequency tables

The first steps are to find the unique words and create dictionary to count them. 


```python
# Creating reconstructing the corpus again
testDF = WoF_DF['PUZZLE']
corpus = ' '.join(testDF)

# Removing extra whitespace
corpus.strip()

# Converting to numpy array, getting/counting unique elements
corpus_index, counts = np.unique(np.array(corpus.split(" ")), return_counts= True)

# Creating the dataframe
first_order_dist = pd.DataFrame.from_dict({'Symbol': corpus_index, 'Frequency': counts})

# Sorting from greatest to least counts
first_order_dist = first_order_dist.sort_values(by= ['Frequency'], ascending= False)

# Optional export
filepath = '/Users/Chris/Desktop/WoF Final Round Puzzles/1st-order_word.csv'
exportTable(filepath, first_order_dist)
```

We have 2664 unique words in our Puzzle data


```python
first_order_dist.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 2664 entries, 1 to 1332
    Data columns (total 2 columns):
    Symbol       2664 non-null object
    Frequency    2664 non-null int64
    dtypes: int64(1), object(1)
    memory usage: 62.4+ KB


Now we plot the data


```python
# Plotting:
fig = px.bar(first_order_dist.iloc[:31], x= 'Symbol', y= 'Frequency')
pio.write_html(fig, file='word_unigram_ordered.html', auto_open=True)
fig.show()
```

-GRAPH-

<h3 id="NLTK">Using NLTK to get Parts of Speech</h3>

Below we'll use the Natural Language Toolkit to get parts of speech of our set of words.
First we'll import `nltk` and the tokenize each element in the `PUZZLE` category. The functions used are:

* `import nltk`
* `nltk.word_tokenize()`
* `nltk.pos_tag()`


```python
# importing the Natural Language Toolkit package, and download 
# "punkt" since we'll need it
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Empty list to hold all the tags
tag_list = []

# tokenizes each element in the `Puzzle` category, then finds 
# the P-O-S tags of each word in each element
for elem in WoF_DF['PUZZLE']:
    text = nltk.word_tokenize(elem)
    tag_list.append(nltk.pos_tag(text))
```

    [nltk_data] Downloading package punkt to /Users/Chris/nltk_data...
    [nltk_data]   Package punkt is already up-to-date!
    [nltk_data] Downloading package averaged_perceptron_tagger to
    [nltk_data]     /Users/Chris/nltk_data...
    [nltk_data]   Package averaged_perceptron_tagger is already up-to-
    [nltk_data]       date!


We'll show the parts of speech for th first 10 elements


```python
tag_list[:10]
```




    [[('OPEN', 'NNP'), ('YOUR', 'NNP'), ('EYES', 'NNP')],
     [('LIZA', 'NNP'), ('MINNELLI', 'NNP')],
     [('PUT', 'VB'), ('ON', 'RP'), ('THE', 'DT'), ('SPOT', 'NN')],
     [('FIRST', 'NNP'), ('PRIZE', 'NNP')],
     [('THE', 'DT'), ('VATICAN', 'NNP')],
     [('FLYING', 'VBG'), ('DOWN', 'NNP'), ('TO', 'NNP'), ('RIO', 'NNP')],
     [('POGO', 'NNP'), ('STICK', 'NNP')],
     [('YANKEE', 'NNP'), ('DOODLE', 'NNP')],
     [('FINGER', 'CD'), ('PAINTING', 'NN')],
     [('JOE', 'NNP'), ('NAMATH', 'NNP')]]



Separates the word and tags


```python
words, tags = [], []
for lst in tag_list:
    for item in lst:
        words.append(item[0])
        tags.append(item[1])
        
            
nltk_tag_dist = pd.DataFrame.from_dict({'Symbol': words, 'Tag': tags})
```

Plots them


```python
# Unique tags and their counts
nltk_tags, counts = np.unique(nltk_tag_dist['Tag'], return_counts= True)

# Orders the distribution
nltk_tagCounts_dist = pd.DataFrame.from_dict({'Tag': nltk_tags, 'Frequency': counts})
nltk_tagCounts_dist['Frequency'] = nltk_tagCounts_dist['Frequency']/nltk_tagCounts_dist['Frequency'].sum()

# Plots them
fig = px.bar(nltk_tagCounts_dist, x= 'Tag', y= 'Frequency')
pio.write_html(fig, file='POS-tagging.html', auto_open=True)
fig.show()
```

-GRAPH-

Noticed that some of the proper nouns (above) aren't actually proper nouns. We considered case - to see if case had an effect of the tagging. 


```python
# Empty list to hold all the tags
tag_list_2 = []

# tokenizes each element in the `Puzzle` category, then finds 
# the P-O-S tags of each word in each element
for elem in WoF_DF['PUZZLE']:
    text = nltk.word_tokenize(elem.lower())
    tag_list_2.append(nltk.pos_tag(text))
```

First ten elements


```python
tag_list_2[:10]
```




    [[('open', 'VB'), ('your', 'PRP$'), ('eyes', 'NNS')],
     [('liza', 'NN'), ('minnelli', 'NN')],
     [('put', 'NN'), ('on', 'IN'), ('the', 'DT'), ('spot', 'NN')],
     [('first', 'RB'), ('prize', 'VB')],
     [('the', 'DT'), ('vatican', 'JJ')],
     [('flying', 'VBG'), ('down', 'RP'), ('to', 'TO'), ('rio', 'VB')],
     [('pogo', 'NN'), ('stick', 'NN')],
     [('yankee', 'NN'), ('doodle', 'NN')],
     [('finger', 'NN'), ('painting', 'VBG')],
     [('joe', 'NN'), ('namath', 'NN')]]



Put the words and tags into another dataframe


```python
words, tags = [], []
for lst in tag_list_2:
    for item in lst:
        words.append(item[0])
        tags.append(item[1])
        
            
nltk_tag_dist = pd.DataFrame.from_dict({'Symbol': words, 'Tag': tags})
```

Plots the result


```python
# Unique tags and their counts
nltk_tags, counts = np.unique(nltk_tag_dist['Tag'], return_counts= True)

# Orders the distribution
nltk_tagCounts_dist_2 = pd.DataFrame.from_dict({'Tag': nltk_tags, 'Frequency_': counts})
nltk_tagCounts_dist_2['Frequency_'] = nltk_tagCounts_dist_2['Frequency_']/nltk_tagCounts_dist_2['Frequency_'].sum()

# Plots them
fig = px.bar(nltk_tagCounts_dist_2, x= 'Tag', y= 'Frequency_')
pio.write_html(fig, file='POS-tagging-2.html', auto_open=True)
fig.show()
```

-GRAPH-

Looks like we were right. Case seems to cause some issues with tagging. Lets join the datasets and plot a comparison bar chart. 


```python
# Join dataframes
pos_outer = pd.merge(nltk_tagCounts_dist, nltk_tagCounts_dist_2, on='Tag', how="outer")
pos_outer.fillna(0, inplace= True)
pos_outer
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Tag</th>
      <th>Frequency</th>
      <th>Frequency_</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>.</td>
      <td>0.000164</td>
      <td>0.000164</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CC</td>
      <td>0.004933</td>
      <td>0.012333</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CD</td>
      <td>0.005920</td>
      <td>0.003124</td>
    </tr>
    <tr>
      <th>3</th>
      <td>DT</td>
      <td>0.037658</td>
      <td>0.058379</td>
    </tr>
    <tr>
      <th>4</th>
      <td>FW</td>
      <td>0.000329</td>
      <td>0.000164</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IN</td>
      <td>0.020227</td>
      <td>0.052458</td>
    </tr>
    <tr>
      <th>6</th>
      <td>JJ</td>
      <td>0.025489</td>
      <td>0.112646</td>
    </tr>
    <tr>
      <th>7</th>
      <td>MD</td>
      <td>0.001151</td>
      <td>0.001973</td>
    </tr>
    <tr>
      <th>8</th>
      <td>NN</td>
      <td>0.173820</td>
      <td>0.535767</td>
    </tr>
    <tr>
      <th>9</th>
      <td>NNP</td>
      <td>0.666667</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>10</th>
      <td>NNS</td>
      <td>0.007071</td>
      <td>0.060187</td>
    </tr>
    <tr>
      <th>11</th>
      <td>PDT</td>
      <td>0.001151</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>12</th>
      <td>POS</td>
      <td>0.000822</td>
      <td>0.000493</td>
    </tr>
    <tr>
      <th>13</th>
      <td>PRP</td>
      <td>0.010360</td>
      <td>0.017596</td>
    </tr>
    <tr>
      <th>14</th>
      <td>PRP$</td>
      <td>0.001480</td>
      <td>0.008716</td>
    </tr>
    <tr>
      <th>15</th>
      <td>RB</td>
      <td>0.006249</td>
      <td>0.025489</td>
    </tr>
    <tr>
      <th>16</th>
      <td>RP</td>
      <td>0.004605</td>
      <td>0.014142</td>
    </tr>
    <tr>
      <th>17</th>
      <td>UH</td>
      <td>0.000164</td>
      <td>0.000164</td>
    </tr>
    <tr>
      <th>18</th>
      <td>VB</td>
      <td>0.013320</td>
      <td>0.025818</td>
    </tr>
    <tr>
      <th>19</th>
      <td>VBD</td>
      <td>0.001316</td>
      <td>0.005427</td>
    </tr>
    <tr>
      <th>20</th>
      <td>VBG</td>
      <td>0.002302</td>
      <td>0.031903</td>
    </tr>
    <tr>
      <th>21</th>
      <td>VBN</td>
      <td>0.000822</td>
      <td>0.011347</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VBP</td>
      <td>0.009209</td>
      <td>0.010689</td>
    </tr>
    <tr>
      <th>23</th>
      <td>VBZ</td>
      <td>0.001809</td>
      <td>0.002302</td>
    </tr>
    <tr>
      <th>24</th>
      <td>WP</td>
      <td>0.001644</td>
      <td>0.001973</td>
    </tr>
    <tr>
      <th>25</th>
      <td>WRB</td>
      <td>0.001316</td>
      <td>0.001316</td>
    </tr>
    <tr>
      <th>26</th>
      <td>JJR</td>
      <td>0.000000</td>
      <td>0.000658</td>
    </tr>
    <tr>
      <th>27</th>
      <td>JJS</td>
      <td>0.000000</td>
      <td>0.000493</td>
    </tr>
    <tr>
      <th>28</th>
      <td>TO</td>
      <td>0.000000</td>
      <td>0.004276</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Join dataframes
pos_outer = pd.merge(nltk_tagCounts_dist, nltk_tagCounts_dist_2, on='Tag', how="outer")
pos_outer.fillna(0, inplace= True)

# Plotting
fig = go.Figure(go.Bar(x= pos_outer['Tag'], y= pos_outer['Frequency'], name='Uppercase'))
fig.add_trace(go.Bar(x= pos_outer['Tag'], y= pos_outer['Frequency_'], name='Lower'))
fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})
po.plot(fig, filename='POS-tagging-compare.html.html', auto_open=True)
# pio.write_html(fig, file='POS-tagging-compare.html', auto_open=True)
fig.show()
```

-GRAPH- 