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


        <script type="text/javascript">
        window.PlotlyConfig = {MathJaxConfig: 'local'};
        if (window.MathJax) {MathJax.Hub.Config({SVG: {font: "STIX-Web"}});}
        if (typeof require !== 'undefined') {
        require.undef("plotly");
        define('plotly', function(require, exports, module) {
            /**
* plotly.js v1.51.2
* Copyright 2012-2019, Plotly, Inc.
* All rights reserved.
* Licensed under the MIT license
*/
        });
        require(['plotly'], function(Plotly) {
            window._Plotly = Plotly;
        });
        }
        </script>
        



<div>
        
        
            <div id="167dd74a-5909-42c8-a0b2-0b7b27e30b62" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};
                    
                if (document.getElementById("167dd74a-5909-42c8-a0b2-0b7b27e30b62")) {
                    Plotly.newPlot(
                        '167dd74a-5909-42c8-a0b2-0b7b27e30b62',
                        [{"alignmentgroup": "True", "hoverlabel": {"namelength": 0}, "hovertemplate": "Symbol=%{x}<br>Frequency=%{y}", "legendgroup": "", "marker": {"color": "#636efa"}, "name": "", "offsetgroup": "", "orientation": "v", "showlegend": false, "textposition": "auto", "type": "bar", "x": [" ", "&", "'", "-", "?", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"], "xaxis": "x", "y": [3171, 18, 41, 65, 1, 2490, 1072, 988, 1038, 2258, 926, 1308, 1393, 2396, 212, 722, 1086, 656, 1406, 2834, 1033, 116, 1514, 1097, 1472, 1346, 492, 767, 117, 926, 138], "yaxis": "y"}],
                        {"barmode": "relative", "legend": {"tracegroupgap": 0}, "margin": {"t": 60}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "xaxis": {"anchor": "y", "domain": [0.0, 1.0], "title": {"text": "Symbol"}}, "yaxis": {"anchor": "x", "domain": [0.0, 1.0], "title": {"text": "Frequency"}}},
                        {"responsive": true}
                    ).then(function(){
                            
var gd = document.getElementById('167dd74a-5909-42c8-a0b2-0b7b27e30b62');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>


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


<div>
        
        
            <div id="2593614a-12b8-4b33-a960-5d9f50bceabe" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};
                    
                if (document.getElementById("2593614a-12b8-4b33-a960-5d9f50bceabe")) {
                    Plotly.newPlot(
                        '2593614a-12b8-4b33-a960-5d9f50bceabe',
                        [{"alignmentgroup": "True", "hoverlabel": {"namelength": 0}, "hovertemplate": "Symbol=%{x}<br>y=%{y}", "legendgroup": "", "marker": {"color": "#636efa"}, "name": "", "offsetgroup": "", "orientation": "v", "showlegend": false, "textposition": "auto", "type": "bar", "x": [" ", "O", "A", "I", "E", "R", "T", "N", "H", "U", "G", "S", "L", "B", "D", "P", "C", "Y", "F", "W", "K", "M", "V", "J", "Z", "X", "Q", "-", "'", "&", "?"], "xaxis": "x", "y": [0.09580349859512372, 0.08562192211245052, 0.07522885887791173, 0.07238889392428774, 0.06821958367322276, 0.045741563189220215, 0.044472642678026524, 0.04247862473186501, 0.04208586362125744, 0.04066588114444545, 0.0395178102057464, 0.03314299525665428, 0.032810658932294026, 0.032387685428562796, 0.03136046406235838, 0.031209402096740082, 0.029849844406175413, 0.027976676032508536, 0.027976676032508536, 0.023172905525846704, 0.02181334783528203, 0.019819329889120517, 0.014864497416840388, 0.006405027342215777, 0.004169310251064987, 0.003534849995468141, 0.0035046376023444817, 0.0019638055530378563, 0.0012387081180700323, 0.0005438230762258679, 3.0212393123659326e-05], "yaxis": "y"}],
                        {"barmode": "relative", "legend": {"tracegroupgap": 0}, "margin": {"t": 60}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "xaxis": {"anchor": "y", "domain": [0.0, 1.0], "title": {"text": "Symbol"}}, "yaxis": {"anchor": "x", "domain": [0.0, 1.0], "title": {"text": "y"}}},
                        {"responsive": true}
                    ).then(function(){
                            
var gd = document.getElementById('2593614a-12b8-4b33-a960-5d9f50bceabe');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



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


<div>
        
        
            <div id="b58487bd-9e65-4093-9976-5d49cc70b7d8" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};
                    
                if (document.getElementById("b58487bd-9e65-4093-9976-5d49cc70b7d8")) {
                    Plotly.newPlot(
                        'b58487bd-9e65-4093-9976-5d49cc70b7d8',
                        [{"colorscale": [[0.0, "#440154"], [0.1111111111111111, "#482878"], [0.2222222222222222, "#3e4989"], [0.3333333333333333, "#31688e"], [0.4444444444444444, "#26828e"], [0.5555555555555556, "#1f9e89"], [0.6666666666666666, "#35b779"], [0.7777777777777778, "#6ece58"], [0.8888888888888888, "#b5de2b"], [1.0, "#fde725"]], "type": "heatmap", "x": [" ", "&", "'", "-", "?", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"], "y": [" ", "&", "'", "-", "?", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"], "z": [[0.0, 0.0006053065204963513, 0.0, 0.0, 0.0, 0.007499075226149242, 0.0005380502404412012, 0.0013114974610754278, 0.009045969667417695, 0.01563708511282241, 0.004640683323805361, 0.00887782896727982, 0.004035376803309009, 0.0017486632814339039, 0.0, 0.004203517503446884, 0.0029256481823990315, 0.0017822914214614789, 0.005313246124356862, 0.003127417022564482, 0.0019168039815717793, 0.0, 0.004909708444025961, 0.002824763762316306, 0.008776944547197095, 0.00033628140027575076, 0.00010088442008272523, 0.0015805225812960285, 0.00043716582035847597, 0.012341527390120052, 0.0002690251202206006], [0.0006053065204963513, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.3628140027575076e-05, 0.0, 0.0, 0.0, 0.0007734472206342267, 0.0, 0.0, 0.0, 0.0, 0.00023539698019302554, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00016814070013787538, 0.00010088442008272523, 0.0, 0.0, 0.0, 6.725628005515015e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.3628140027575076e-05, 0.0, 0.00010088442008272523, 0.0003699095403033258, 0.00033628140027575076, 3.3628140027575076e-05, 0.0001345125601103003, 0.0, 0.0, 6.725628005515015e-05, 0.00010088442008272523, 6.725628005515015e-05, 0.0001345125601103003, 0.00010088442008272523, 6.725628005515015e-05, 0.0, 0.00010088442008272523, 0.0, 0.00010088442008272523, 0.0, 0.0, 0.0001345125601103003, 3.3628140027575076e-05, 0.0002690251202206006, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.3628140027575076e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.008642431987086795, 0.0, 0.0, 6.725628005515015e-05, 0.0, 0.0, 0.005447758684467162, 0.002723879342233581, 0.0016814070013787537, 0.005313246124356862, 0.003665467263005683, 0.002286713521875105, 0.005851296364798063, 0.0020513165416820795, 0.001378753741130578, 0.0005716783804687762, 0.00457342704375021, 0.0039344923832262835, 0.0011769849009651277, 0.002690251202206006, 0.004707939603860511, 0.0, 0.00443891448363991, 0.0009415879207721021, 0.0025221105020681307, 0.001849547701516629, 0.0023875979419578303, 0.005716783804687763, 0.00020176884016545046, 0.0008743316407169519, 0.0003699095403033258], [0.009920301308134647, 0.0, 0.0, 0.00010088442008272523, 0.0, 0.0028920200423714565, 0.0014796381612133033, 0.0, 0.00047079396038605107, 0.0007398190806066516, 6.725628005515015e-05, 6.725628005515015e-05, 0.0001345125601103003, 0.0009752160607996771, 0.0, 0.0003699095403033258, 0.0002690251202206006, 0.0010088442008272522, 6.725628005515015e-05, 0.0019840602616269295, 0.00023539698019302554, 0.0, 0.0006053065204963513, 0.0, 0.00016814070013787538, 0.002286713521875105, 0.0, 0.00023539698019302554, 0.0, 0.0005044221004136261, 0.0], [0.004909708444025961, 0.0, 0.0, 6.725628005515015e-05, 0.0, 0.005414130544439587, 3.3628140027575076e-05, 0.0001345125601103003, 0.0, 0.0013114974610754278, 0.0, 0.0, 0.0, 0.007801728486397417, 0.0, 3.3628140027575076e-05, 0.00010088442008272523, 0.0, 0.0014796381612133033, 0.0019840602616269295, 6.725628005515015e-05, 0.0, 0.0005380502404412012, 0.0006389346605239264, 0.0011433567609375524, 0.0010424723408548272, 0.0, 0.0, 0.00020176884016545046, 0.0004035376803309009, 0.0], [0.0034300702828126577, 0.0, 0.0, 0.00023539698019302554, 0.0, 0.0028920200423714565, 3.3628140027575076e-05, 0.0, 0.00043716582035847597, 0.0038336079631435586, 0.0, 0.0, 0.0001345125601103003, 0.00450617076369506, 0.0, 0.0, 0.001849547701516629, 3.3628140027575076e-05, 0.005985808924908363, 0.003026532602481757, 0.00010088442008272523, 0.0, 0.0029929044624541815, 0.0001345125601103003, 3.3628140027575076e-05, 0.0015132663012408785, 0.0, 0.00043716582035847597, 0.0, 3.3628140027575076e-05, 0.0], [0.0012106130409927026, 0.0, 0.0, 3.3628140027575076e-05, 0.0, 0.00010088442008272523, 0.0029256481823990315, 0.0039344923832262835, 0.003699095403033258, 0.0008743316407169519, 0.0016141507213236037, 0.005279617984329287, 0.008238894306755893, 0.0033628140027575073, 0.00047079396038605107, 0.005918552644853213, 0.00437165820358476, 0.0038336079631435586, 0.0025557386420957057, 0.0005044221004136261, 0.0039344923832262835, 0.0, 0.004069004943336584, 0.0023539698019302553, 0.0023875979419578303, 0.00225308538184753, 0.005918552644853213, 0.0019504321215993543, 0.00033628140027575076, 0.0005380502404412012, 0.000907959780744527], [0.007499075226149242, 0.0, 0.0, 0.0001345125601103003, 0.0, 0.0008743316407169519, 0.0, 0.0, 6.725628005515015e-05, 0.0007061909405790765, 0.0038336079631435586, 0.0, 0.00033628140027575076, 0.0017486632814339039, 0.0, 3.3628140027575076e-05, 0.0008743316407169519, 0.00010088442008272523, 0.00010088442008272523, 0.006221205905101388, 0.00010088442008272523, 0.0, 0.00043716582035847597, 0.0, 0.00010088442008272523, 0.0009752160607996771, 0.0, 0.00010088442008272523, 3.3628140027575076e-05, 3.3628140027575076e-05, 0.0], [0.005817668224770488, 0.0, 0.0, 3.3628140027575076e-05, 0.0, 0.0039008642431987085, 0.0, 0.0, 0.0012778693210478529, 0.0006389346605239264, 0.0, 0.0011097286209099774, 3.3628140027575076e-05, 0.006187577765073814, 0.0, 6.725628005515015e-05, 0.0001345125601103003, 0.0, 0.010962773648989474, 0.003161045162592057, 0.00010088442008272523, 0.0, 0.000907959780744527, 3.3628140027575076e-05, 6.725628005515015e-05, 0.0034973265628678077, 0.0, 0.0, 0.0, 0.00010088442008272523, 0.0], [0.006389346605239264, 0.0, 0.0, 0.00033628140027575076, 0.0, 0.0005716783804687762, 3.3628140027575076e-05, 0.006288462185156539, 0.00010088442008272523, 0.0006053065204963513, 0.0, 0.0058849245048256385, 3.3628140027575076e-05, 0.0, 0.0, 0.00010088442008272523, 0.0, 0.0, 3.3628140027575076e-05, 0.0001345125601103003, 0.0017486632814339039, 0.0, 0.00030265326024817566, 0.004136261223391734, 0.009045969667417695, 0.0, 0.0, 0.0016477788613511787, 0.0002690251202206006, 0.00020176884016545046, 0.0], [0.003665467263005683, 0.0, 0.0, 0.0, 0.0, 0.0039344923832262835, 0.003699095403033258, 0.0013114974610754278, 0.0025893667821232807, 0.0010424723408548272, 0.0037999798231159836, 0.0024548542220129803, 0.006490231025321989, 6.725628005515015e-05, 0.00033628140027575076, 0.003665467263005683, 0.005548643104549888, 0.00211857282173723, 0.003060160742509332, 0.0025221105020681307, 0.0033964421427850828, 0.0, 0.005279617984329287, 0.0025557386420957057, 0.004102633083364159, 0.0033291858627299323, 0.00443891448363991, 0.004169889363419309, 0.0008743316407169519, 0.0007734472206342267, 0.0003699095403033258], [0.002824763762316306, 0.0, 0.0, 0.0, 0.0, 0.00033628140027575076, 0.00016814070013787538, 0.0, 6.725628005515015e-05, 3.3628140027575076e-05, 0.0, 0.0, 0.0, 6.725628005515015e-05, 0.0, 0.0, 0.0, 0.0, 0.00020176884016545046, 3.3628140027575076e-05, 0.0, 0.0, 3.3628140027575076e-05, 3.3628140027575076e-05, 0.0, 0.00010088442008272523, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0017150351414063289, 0.0, 0.0, 6.725628005515015e-05, 0.0, 0.003127417022564482, 0.0, 0.006322090325184114, 3.3628140027575076e-05, 0.00023539698019302554, 0.0, 3.3628140027575076e-05, 3.3628140027575076e-05, 0.0009752160607996771, 0.0, 0.00010088442008272523, 0.0008070753606618018, 0.0, 0.0019168039815717793, 0.0029929044624541815, 3.3628140027575076e-05, 0.0, 0.00218582910179238, 0.0012442411810202779, 0.0, 0.00010088442008272523, 0.0, 0.00023539698019302554, 0.0, 0.0, 0.0], [0.001849547701516629, 0.0, 0.0, 3.3628140027575076e-05, 0.0, 0.005817668224770488, 0.0035645828429229577, 0.0015132663012408785, 0.00030265326024817566, 0.001378753741130578, 0.0023203416619026803, 0.0011769849009651277, 0.00020176884016545046, 0.0032955577227023573, 0.0, 0.00020176884016545046, 0.0017822914214614789, 0.0, 0.00010088442008272523, 0.004169889363419309, 0.0019168039815717793, 0.0, 0.00043716582035847597, 0.0002690251202206006, 0.00016814070013787538, 0.002286713521875105, 0.0, 0.0005044221004136261, 0.0, 0.0002690251202206006, 0.00023539698019302554], [0.0034973265628678077, 0.0, 0.0007061909405790765, 6.725628005515015e-05, 0.0, 0.002757507482261156, 0.0, 0.0, 3.3628140027575076e-05, 0.0007734472206342267, 3.3628140027575076e-05, 3.3628140027575076e-05, 3.3628140027575076e-05, 0.0017150351414063289, 0.0, 0.00010088442008272523, 0.00030265326024817566, 0.0002690251202206006, 0.0, 0.0029929044624541815, 0.00010088442008272523, 0.0, 0.0012442411810202779, 0.00043716582035847597, 0.0001345125601103003, 0.0024548542220129803, 0.0, 0.0, 0.0, 0.0004035376803309009, 0.0], [0.0006053065204963513, 0.0, 0.0, 3.3628140027575076e-05, 0.0, 0.008407035006893769, 0.0, 6.725628005515015e-05, 0.0, 0.003127417022564482, 0.0, 0.00043716582035847597, 6.725628005515015e-05, 0.01715035141406329, 0.0, 0.0007734472206342267, 0.0, 0.00010088442008272523, 0.00023539698019302554, 0.006422974745266839, 0.0, 0.0, 0.0006725628005515015, 0.00020176884016545046, 0.0, 0.004203517503446884, 0.0, 0.00218582910179238, 0.0, 0.0001345125601103003, 0.0], [0.0077681003463698425, 0.0, 0.0, 0.00016814070013787538, 0.0, 0.00010088442008272523, 0.0071291656858459155, 0.0037663516830884086, 0.003093788882536907, 0.0007398190806066516, 0.00437165820358476, 0.004775195883915661, 0.00881057268722467, 0.0034300702828126577, 0.002757507482261156, 0.00033628140027575076, 0.004842452163970811, 0.0025221105020681307, 0.0017486632814339039, 0.007499075226149242, 0.0038672361031711336, 0.0, 0.007028281265763191, 0.0014796381612133033, 0.004169889363419309, 0.0002690251202206006, 0.0025221105020681307, 0.003631839122978108, 6.725628005515015e-05, 0.003161045162592057, 0.00030265326024817566], [0.007566331506204392, 0.0, 0.0, 0.0001345125601103003, 0.0, 0.0029256481823990315, 0.0, 0.0, 6.725628005515015e-05, 0.0007734472206342267, 0.0, 6.725628005515015e-05, 0.00010088442008272523, 0.0020176884016545045, 0.0, 6.725628005515015e-05, 0.0002690251202206006, 0.0020513165416820795, 6.725628005515015e-05, 0.0034300702828126577, 0.001849547701516629, 0.0, 0.0002690251202206006, 0.0012442411810202779, 3.3628140027575076e-05, 0.0029592763224266065, 0.0, 0.00010088442008272523, 0.00020176884016545046, 0.00033628140027575076, 0.0], [0.0009752160607996771, 0.0, 0.0, 0.0, 0.0, 3.3628140027575076e-05, 0.0, 0.0, 0.0, 0.00020176884016545046, 0.0, 0.0, 0.0, 0.0005044221004136261, 0.0, 0.0, 0.0, 0.0, 0.0001345125601103003, 3.3628140027575076e-05, 0.0, 0.0, 3.3628140027575076e-05, 0.0006725628005515015, 0.0, 0.00010088442008272523, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0015132663012408785, 0.0, 3.3628140027575076e-05, 0.00010088442008272523, 0.0, 0.008104381746645593, 0.003194673302619632, 0.0011097286209099774, 0.0010088442008272522, 0.008642431987086795, 0.0010761004808824024, 0.002791135622288731, 0.0002690251202206006, 0.0026229949221508557, 0.0, 0.0, 0.00010088442008272523, 0.0, 6.725628005515015e-05, 0.009382251067693446, 0.002656623062178431, 0.0, 0.00010088442008272523, 0.0, 0.0009415879207721021, 0.004741567743888085, 0.0, 0.00023539698019302554, 0.0, 6.725628005515015e-05, 0.0], [0.004909708444025961, 0.0, 0.0002690251202206006, 0.0001345125601103003, 0.0, 0.002723879342233581, 0.00033628140027575076, 0.00010088442008272523, 0.0014796381612133033, 0.003699095403033258, 3.3628140027575076e-05, 0.00043716582035847597, 0.00016814070013787538, 0.003732723543060833, 0.0, 0.0011097286209099774, 0.0004035376803309009, 0.00023539698019302554, 0.001378753741130578, 0.0015805225812960285, 0.0009415879207721021, 0.0, 0.0012106130409927026, 0.0008743316407169519, 0.0015468944412684535, 0.00423714564347446, 0.0, 0.00047079396038605107, 0.0, 0.00043716582035847597, 0.0], [0.006961024985708041, 0.0, 0.00023539698019302554, 0.00016814070013787538, 0.0, 0.004775195883915661, 6.725628005515015e-05, 0.0014796381612133033, 6.725628005515015e-05, 0.002286713521875105, 0.000907959780744527, 3.3628140027575076e-05, 0.002791135622288731, 0.008037125466590442, 0.0, 3.3628140027575076e-05, 0.0007398190806066516, 0.0, 0.0023203416619026803, 0.0032955577227023573, 0.00043716582035847597, 0.0, 0.0018831758415442043, 0.003093788882536907, 0.00023539698019302554, 0.0039344923832262835, 0.0, 0.00010088442008272523, 6.725628005515015e-05, 0.00023539698019302554, 0.0], [0.0016814070013787537, 0.0, 0.0, 0.00016814070013787538, 0.0, 0.002152200961764805, 0.0037999798231159836, 0.001412381881158153, 0.0012106130409927026, 0.00016814070013787538, 0.001849547701516629, 0.002723879342233581, 0.002286713521875105, 0.00043716582035847597, 0.0020849446817096545, 0.00010088442008272523, 0.0020176884016545045, 0.0007734472206342267, 0.0002690251202206006, 0.011500823889430675, 0.0018831758415442043, 0.0039008642431987085, 0.0008743316407169519, 0.0009752160607996771, 0.0007734472206342267, 0.00010088442008272523, 0.0, 0.0, 0.00010088442008272523, 0.00020176884016545046, 0.0], [0.003026532602481757, 0.0, 0.0001345125601103003, 0.0, 0.0, 0.0034636984228402327, 3.3628140027575076e-05, 0.0, 0.00030265326024817566, 0.0008743316407169519, 0.0, 0.0, 0.0, 0.0024884823620405557, 0.0, 0.0, 0.0001345125601103003, 0.0, 0.00010088442008272523, 0.002791135622288731, 0.0, 0.0, 0.0002690251202206006, 0.0, 0.00010088442008272523, 3.3628140027575076e-05, 0.00010088442008272523, 0.0, 0.0, 0.0, 0.0], [0.0060194370649359384, 0.0, 0.0, 3.3628140027575076e-05, 0.0, 0.0019504321215993543, 0.0001345125601103003, 0.0, 0.0002690251202206006, 0.0016814070013787537, 0.00010088442008272523, 6.725628005515015e-05, 0.00020176884016545046, 0.0, 0.0, 0.00016814070013787538, 3.3628140027575076e-05, 0.0, 0.00010088442008272523, 0.0067928842855701655, 0.00010088442008272523, 0.0, 0.00043716582035847597, 0.0005044221004136261, 0.00043716582035847597, 3.3628140027575076e-05, 0.0, 0.0, 0.0, 0.0002690251202206006, 3.3628140027575076e-05], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0007061909405790765, 0.0, 0.0, 0.0, 0.0013114974610754278, 0.0, 0.0, 0.0, 0.0007061909405790765, 0.0, 0.0, 0.0, 0.0, 3.3628140027575076e-05, 0.0009415879207721021, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00016814070013787538, 0.0, 0.0, 0.0, 0.0, 0.0], [0.001849547701516629, 0.0, 0.0, 6.725628005515015e-05, 0.0, 0.004640683323805361, 0.0017822914214614789, 0.0007398190806066516, 0.0009752160607996771, 0.0018831758415442043, 0.0005716783804687762, 0.0008070753606618018, 0.0009415879207721021, 0.0, 0.0, 0.0010424723408548272, 0.0020176884016545045, 0.0011097286209099774, 0.0006389346605239264, 0.0015805225812960285, 0.0007734472206342267, 0.0, 0.0020513165416820795, 0.0011097286209099774, 0.002791135622288731, 0.0006389346605239264, 0.0006053065204963513, 6.725628005515015e-05, 0.00010088442008272523, 0.0, 0.0006053065204963513], [0.00010088442008272523, 0.0, 0.0, 0.0, 0.0, 0.0008070753606618018, 0.0, 0.0, 0.0, 6.725628005515015e-05, 0.0, 0.0, 0.0, 0.0012442411810202779, 0.0, 0.0, 0.0, 0.0, 6.725628005515015e-05, 0.00030265326024817566, 0.0, 0.0, 0.0, 0.0, 0.00010088442008272523, 0.0005380502404412012, 0.0, 0.0, 0.0, 0.0, 0.0011097286209099774]]}],
                        {"template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Bigrams"}, "xaxis": {"nticks": 31}},
                        {"responsive": true}
                    ).then(function(){
                            
var gd = document.getElementById('b58487bd-9e65-4093-9976-5d49cc70b7d8');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>


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


<div>
        
        
            <div id="f56f2350-d026-48e5-a070-1d7c97823107" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};
                    
                if (document.getElementById("f56f2350-d026-48e5-a070-1d7c97823107")) {
                    Plotly.newPlot(
                        'f56f2350-d026-48e5-a070-1d7c97823107',
                        [{"colorscale": [[0.0, "#fde725"], [0.1111111111111111, "#b5de2b"], [0.2222222222222222, "#6ece58"], [0.3333333333333333, "#35b779"], [0.4444444444444444, "#1f9e89"], [0.5555555555555556, "#26828e"], [0.6666666666666666, "#31688e"], [0.7777777777777778, "#3e4989"], [0.8888888888888888, "#482878"], [1.0, "#440154"]], "type": "heatmap", "x": [" ", "&", "'", "-", "?", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"], "y": ["  ", " &", " '", " -", " ?", " A", " B", " C", " D", " E", " F", " G", " H", " I", " J", " K", " L", " M", " N", " O", " P", " Q", " R", " S", " T", " U", " V", " W", " X", " Y", " Z", "& ", "&&", "&'", "&-", "&?", "&A", "&B", "&C", "&D", "&E", "&F", "&G", "&H", "&I", "&J", "&K", "&L", "&M", "&N", "&O", "&P", "&Q", "&R", "&S", "&T", "&U", "&V", "&W", "&X", "&Y", "&Z", "' ", "'&", "''", "'-", "'?", "'A", "'B", "'C", "'D", "'E", "'F", "'G", "'H", "'I", "'J", "'K", "'L", "'M", "'N", "'O", "'P", "'Q", "'R", "'S", "'T", "'U", "'V", "'W", "'X", "'Y", "'Z", "- ", "-&", "-'", "--", "-?", "-A", "-B", "-C", "-D", "-E", "-F", "-G", "-H", "-I", "-J", "-K", "-L", "-M", "-N", "-O", "-P", "-Q", "-R", "-S", "-T", "-U", "-V", "-W", "-X", "-Y", "-Z", "? ", "?&", "?'", "?-", "??", "?A", "?B", "?C", "?D", "?E", "?F", "?G", "?H", "?I", "?J", "?K", "?L", "?M", "?N", "?O", "?P", "?Q", "?R", "?S", "?T", "?U", "?V", "?W", "?X", "?Y", "?Z", "A ", "A&", "A'", "A-", "A?", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ", "B ", "B&", "B'", "B-", "B?", "BA", "BB", "BC", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BK", "BL", "BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT", "BU", "BV", "BW", "BX", "BY", "BZ", "C ", "C&", "C'", "C-", "C?", "CA", "CB", "CC", "CD", "CE", "CF", "CG", "CH", "CI", "CJ", "CK", "CL", "CM", "CN", "CO", "CP", "CQ", "CR", "CS", "CT", "CU", "CV", "CW", "CX", "CY", "CZ", "D ", "D&", "D'", "D-", "D?", "DA", "DB", "DC", "DD", "DE", "DF", "DG", "DH", "DI", "DJ", "DK", "DL", "DM", "DN", "DO", "DP", "DQ", "DR", "DS", "DT", "DU", "DV", "DW", "DX", "DY", "DZ", "E ", "E&", "E'", "E-", "E?", "EA", "EB", "EC", "ED", "EE", "EF", "EG", "EH", "EI", "EJ", "EK", "EL", "EM", "EN", "EO", "EP", "EQ", "ER", "ES", "ET", "EU", "EV", "EW", "EX", "EY", "EZ", "F ", "F&", "F'", "F-", "F?", "FA", "FB", "FC", "FD", "FE", "FF", "FG", "FH", "FI", "FJ", "FK", "FL", "FM", "FN", "FO", "FP", "FQ", "FR", "FS", "FT", "FU", "FV", "FW", "FX", "FY", "FZ", "G ", "G&", "G'", "G-", "G?", "GA", "GB", "GC", "GD", "GE", "GF", "GG", "GH", "GI", "GJ", "GK", "GL", "GM", "GN", "GO", "GP", "GQ", "GR", "GS", "GT", "GU", "GV", "GW", "GX", "GY", "GZ", "H ", "H&", "H'", "H-", "H?", "HA", "HB", "HC", "HD", "HE", "HF", "HG", "HH", "HI", "HJ", "HK", "HL", "HM", "HN", "HO", "HP", "HQ", "HR", "HS", "HT", "HU", "HV", "HW", "HX", "HY", "HZ", "I ", "I&", "I'", "I-", "I?", "IA", "IB", "IC", "ID", "IE", "IF", "IG", "IH", "II", "IJ", "IK", "IL", "IM", "IN", "IO", "IP", "IQ", "IR", "IS", "IT", "IU", "IV", "IW", "IX", "IY", "IZ", "J ", "J&", "J'", "J-", "J?", "JA", "JB", "JC", "JD", "JE", "JF", "JG", "JH", "JI", "JJ", "JK", "JL", "JM", "JN", "JO", "JP", "JQ", "JR", "JS", "JT", "JU", "JV", "JW", "JX", "JY", "JZ", "K ", "K&", "K'", "K-", "K?", "KA", "KB", "KC", "KD", "KE", "KF", "KG", "KH", "KI", "KJ", "KK", "KL", "KM", "KN", "KO", "KP", "KQ", "KR", "KS", "KT", "KU", "KV", "KW", "KX", "KY", "KZ", "L ", "L&", "L'", "L-", "L?", "LA", "LB", "LC", "LD", "LE", "LF", "LG", "LH", "LI", "LJ", "LK", "LL", "LM", "LN", "LO", "LP", "LQ", "LR", "LS", "LT", "LU", "LV", "LW", "LX", "LY", "LZ", "M ", "M&", "M'", "M-", "M?", "MA", "MB", "MC", "MD", "ME", "MF", "MG", "MH", "MI", "MJ", "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "N ", "N&", "N'", "N-", "N?", "NA", "NB", "NC", "ND", "NE", "NF", "NG", "NH", "NI", "NJ", "NK", "NL", "NM", "NN", "NO", "NP", "NQ", "NR", "NS", "NT", "NU", "NV", "NW", "NX", "NY", "NZ", "O ", "O&", "O'", "O-", "O?", "OA", "OB", "OC", "OD", "OE", "OF", "OG", "OH", "OI", "OJ", "OK", "OL", "OM", "ON", "OO", "OP", "OQ", "OR", "OS", "OT", "OU", "OV", "OW", "OX", "OY", "OZ", "P ", "P&", "P'", "P-", "P?", "PA", "PB", "PC", "PD", "PE", "PF", "PG", "PH", "PI", "PJ", "PK", "PL", "PM", "PN", "PO", "PP", "PQ", "PR", "PS", "PT", "PU", "PV", "PW", "PX", "PY", "PZ", "Q ", "Q&", "Q'", "Q-", "Q?", "QA", "QB", "QC", "QD", "QE", "QF", "QG", "QH", "QI", "QJ", "QK", "QL", "QM", "QN", "QO", "QP", "QQ", "QR", "QS", "QT", "QU", "QV", "QW", "QX", "QY", "QZ", "R ", "R&", "R'", "R-", "R?", "RA", "RB", "RC", "RD", "RE", "RF", "RG", "RH", "RI", "RJ", "RK", "RL", "RM", "RN", "RO", "RP", "RQ", "RR", "RS", "RT", "RU", "RV", "RW", "RX", "RY", "RZ", "S ", "S&", "S'", "S-", "S?", "SA", "SB", "SC", "SD", "SE", "SF", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SP", "SQ", "SR", "SS", "ST", "SU", "SV", "SW", "SX", "SY", "SZ", "T ", "T&", "T'", "T-", "T?", "TA", "TB", "TC", "TD", "TE", "TF", "TG", "TH", "TI", "TJ", "TK", "TL", "TM", "TN", "TO", "TP", "TQ", "TR", "TS", "TT", "TU", "TV", "TW", "TX", "TY", "TZ", "U ", "U&", "U'", "U-", "U?", "UA", "UB", "UC", "UD", "UE", "UF", "UG", "UH", "UI", "UJ", "UK", "UL", "UM", "UN", "UO", "UP", "UQ", "UR", "US", "UT", "UU", "UV", "UW", "UX", "UY", "UZ", "V ", "V&", "V'", "V-", "V?", "VA", "VB", "VC", "VD", "VE", "VF", "VG", "VH", "VI", "VJ", "VK", "VL", "VM", "VN", "VO", "VP", "VQ", "VR", "VS", "VT", "VU", "VV", "VW", "VX", "VY", "VZ", "W ", "W&", "W'", "W-", "W?", "WA", "WB", "WC", "WD", "WE", "WF", "WG", "WH", "WI", "WJ", "WK", "WL", "WM", "WN", "WO", "WP", "WQ", "WR", "WS", "WT", "WU", "WV", "WW", "WX", "WY", "WZ", "X ", "X&", "X'", "X-", "X?", "XA", "XB", "XC", "XD", "XE", "XF", "XG", "XH", "XI", "XJ", "XK", "XL", "XM", "XN", "XO", "XP", "XQ", "XR", "XS", "XT", "XU", "XV", "XW", "XX", "XY", "XZ", "Y ", "Y&", "Y'", "Y-", "Y?", "YA", "YB", "YC", "YD", "YE", "YF", "YG", "YH", "YI", "YJ", "YK", "YL", "YM", "YN", "YO", "YP", "YQ", "YR", "YS", "YT", "YU", "YV", "YW", "YX", "YY", "YZ", "Z ", "Z&", "Z'", "Z-", "Z?", "ZA", "ZB", "ZC", "ZD", "ZE", "ZF", "ZG", "ZH", "ZI", "ZJ", "ZK", "ZL", "ZM", "ZN", "ZO", "ZP", "ZQ", "ZR", "ZS", "ZT", "ZU", "ZV", "ZW", "ZX", "ZY", "ZZ"], "z": [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00014657383657017223, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.00014657383657017223, 0.0007328691828508611, 0.0016489556614144375, 0.00047636496885305975, 0.001355807988274093, 0.00021986075485525832, 0.00021986075485525832, 0.0, 0.00036643459142543056, 0.00014657383657017223, 0.00029314767314034447, 0.0005130084279956027, 0.00029314767314034447, 0.00018321729571271528, 0.0, 0.0004030780505679736, 0.000659582264565775, 0.0011359472334188348, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 7.328691828508612e-05, 0.00047636496885305975, 3.664345914254306e-05], [0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0011725906925613779, 7.328691828508612e-05, 3.664345914254306e-05, 0.0008427995602784902, 0.0015756687431293514, 0.00029314767314034447, 0.0011359472334188348, 0.00047636496885305975, 0.00014657383657017223, 0.0, 0.0005130084279956027, 0.00018321729571271528, 0.00018321729571271528, 0.00036643459142543056, 0.0003297911322828875, 0.00014657383657017223, 0.0, 0.00047636496885305975, 0.00021986075485525832, 0.0007328691828508611, 0.00010993037742762916, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.001832172957127153, 3.664345914254306e-05], [0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 3.664345914254306e-05, 0.000622938805423232, 0.0007695126419934042, 0.0003297911322828875, 0.0004030780505679736, 0.00014657383657017223, 0.0, 0.0, 0.00021986075485525832, 0.00021986075485525832, 3.664345914254306e-05, 0.00021986075485525832, 0.00014657383657017223, 0.00014657383657017223, 0.0, 0.00014657383657017223, 0.00014657383657017223, 0.00043972150971051665, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0008427995602784902, 0.0], [0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 3.664345914254306e-05, 0.0003297911322828875, 0.00043972150971051665, 0.0, 0.00029314767314034447, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.00018321729571271528, 0.00014657383657017223, 0.00010993037742762916, 0.00010993037742762916, 0.00010993037742762916, 7.328691828508612e-05, 0.0, 0.00025650421399780137, 0.00014657383657017223, 0.00036643459142543056, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0005862953462806889, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.00021986075485525832, 0.00010993037742762916, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0007695126419934042, 0.00014657383657017223, 0.0, 0.0009893733968486624, 0.0008427995602784902, 0.0003297911322828875, 0.0005862953462806889, 0.00029314767314034447, 0.00021986075485525832, 0.0, 0.00029314767314034447, 0.00025650421399780137, 0.00010993037742762916, 0.000622938805423232, 0.00036643459142543056, 7.328691828508612e-05, 0.0, 0.00021986075485525832, 7.328691828508612e-05, 0.000622938805423232, 0.0, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.001209234151703921, 3.664345914254306e-05], [0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0005130084279956027, 0.0, 7.328691828508612e-05, 0.0005862953462806889, 0.001209234151703921, 0.00029314767314034447, 0.00025650421399780137, 0.00029314767314034447, 0.0003297911322828875, 0.0, 0.00010993037742762916, 0.0004030780505679736, 0.00014657383657017223, 0.00025650421399780137, 0.00021986075485525832, 0.0, 0.0, 0.00021986075485525832, 0.00010993037742762916, 0.00036643459142543056, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0008061561011359472, 3.664345914254306e-05], [0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0011725906925613779, 0.0, 0.0, 0.0005496518871381459, 0.0009160864785635764, 0.0005130084279956027, 0.0007328691828508611, 0.00018321729571271528, 7.328691828508612e-05, 0.0, 0.00025650421399780137, 0.00021986075485525832, 0.00018321729571271528, 0.00025650421399780137, 0.00025650421399780137, 0.00018321729571271528, 0.0, 0.00047636496885305975, 0.0, 0.0003297911322828875, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0007328691828508611, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00036643459142543056, 0.0009160864785635764, 0.00014657383657017223, 0.0004030780505679736, 0.0003297911322828875, 0.0, 0.0, 0.00021986075485525832, 0.00014657383657017223, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.00014657383657017223, 0.00047636496885305975, 0.0, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.00021986075485525832, 0.0], [0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0, 0.00010993037742762916, 0.00021986075485525832, 0.0005496518871381459, 7.328691828508612e-05, 0.00014657383657017223, 0.00018321729571271528, 7.328691828508612e-05, 0.0, 0.00018321729571271528, 0.0, 0.00010993037742762916, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.00018321729571271528, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.00025650421399780137, 0.0], [0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.00014657383657017223, 0.00043972150971051665, 0.0, 0.00018321729571271528, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 7.328691828508612e-05], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.00025650421399780137, 0.0003297911322828875, 0.00025650421399780137, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0004030780505679736, 3.664345914254306e-05], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 3.664345914254306e-05, 0.0003297911322828875, 0.000659582264565775, 0.00014657383657017223, 0.0004030780505679736, 0.00014657383657017223, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.00014657383657017223, 0.00010993037742762916, 0.0, 0.0, 0.00025650421399780137, 7.328691828508612e-05, 0.0004030780505679736, 7.328691828508612e-05, 0.0, 0.00010993037742762916, 0.0, 0.00047636496885305975, 3.664345914254306e-05], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00018321729571271528, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 7.328691828508612e-05, 0.0007695126419934042, 0.0015023818248442653, 0.00018321729571271528, 0.0005862953462806889, 0.0003297911322828875, 0.0, 0.0, 0.0006962257237083181, 0.0003297911322828875, 0.00018321729571271528, 0.00025650421399780137, 7.328691828508612e-05, 0.00018321729571271528, 0.0, 0.00047636496885305975, 0.0005496518871381459, 0.0016489556614144375, 0.0, 0.0, 0.00018321729571271528, 7.328691828508612e-05, 0.0005130084279956027, 0.0], [0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0004030780505679736, 3.664345914254306e-05, 0.00021986075485525832, 0.0005862953462806889, 0.0015390252839868083, 0.00043972150971051665, 0.0008794430194210333, 0.0003297911322828875, 0.00010993037742762916, 0.0, 0.00047636496885305975, 0.00018321729571271528, 0.00021986075485525832, 0.00036643459142543056, 0.00021986075485525832, 0.00018321729571271528, 0.0, 0.00047636496885305975, 0.00010993037742762916, 0.00043972150971051665, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0008061561011359472, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.00018321729571271528, 0.0005862953462806889, 3.664345914254306e-05, 0.00014657383657017223, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 3.664345914254306e-05, 0.00021986075485525832, 0.00047636496885305975, 0.0005496518871381459, 0.00010993037742762916, 0.0004030780505679736, 0.00021986075485525832, 0.00010993037742762916, 0.0, 0.00010993037742762916, 0.00018321729571271528, 0.00010993037742762916, 0.00025650421399780137, 0.00018321729571271528, 0.00021986075485525832, 0.0, 0.00029314767314034447, 7.328691828508612e-05, 0.0004030780505679736, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0009527299377061195, 0.0], [0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.000659582264565775, 0.000659582264565775, 0.000659582264565775, 0.0004030780505679736, 0.0004030780505679736, 3.664345914254306e-05, 0.0, 0.00036643459142543056, 0.00021986075485525832, 3.664345914254306e-05, 0.001282521069989007, 0.00025650421399780137, 0.0003297911322828875, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0008427995602784902, 0.0, 0.0, 0.00025650421399780137, 0.00010993037742762916, 0.0008794430194210333, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.00036643459142543056, 3.664345914254306e-05, 0.00025650421399780137, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.00010993037742762916, 0.00018321729571271528, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.00010993037742762916, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.00014657383657017223, 0.0004030780505679736, 0.0005130084279956027, 0.00029314767314034447, 0.00021986075485525832, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.00018321729571271528, 0.0, 0.0003297911322828875, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0], [0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0009160864785635764, 0.0, 0.00014657383657017223, 0.0003297911322828875, 0.001245877610846464, 0.00025650421399780137, 0.0006962257237083181, 0.00021986075485525832, 0.00025650421399780137, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 7.328691828508612e-05, 0.00021986075485525832, 0.00010993037742762916, 0.0, 0.0, 0.0003297911322828875, 7.328691828508612e-05, 0.0004030780505679736, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.0011725906925613779, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00021986075485525832, 0.00043972150971051665, 0.00010993037742762916, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.00021986075485525832, 7.328691828508612e-05, 0.00014657383657017223, 0.0, 7.328691828508612e-05, 0.00018321729571271528, 0.00018321729571271528, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.000659582264565775, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0007695126419934042, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.003444485159399047, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.00018321729571271528, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00021986075485525832], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005130084279956027, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0007695126419934042, 0.0003297911322828875, 3.664345914254306e-05, 3.664345914254306e-05, 0.00018321729571271528, 0.00018321729571271528, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.00010993037742762916, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001245877610846464, 0.0, 3.664345914254306e-05, 0.00021986075485525832, 0.0005862953462806889, 0.0, 0.0, 3.664345914254306e-05, 0.0006962257237083181, 0.0, 0.00036643459142543056, 0.00018321729571271528, 3.664345914254306e-05, 0.00014657383657017223, 0.0008061561011359472, 0.0, 0.00043972150971051665, 3.664345914254306e-05, 0.00014657383657017223, 3.664345914254306e-05, 0.00018321729571271528, 3.664345914254306e-05, 0.00014657383657017223, 7.328691828508612e-05, 0.0], [0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.00018321729571271528, 0.0, 0.000622938805423232, 7.328691828508612e-05, 0.00010993037742762916, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 7.328691828508612e-05, 3.664345914254306e-05, 0.0005862953462806889, 0.00021986075485525832, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.00014657383657017223, 0.00014657383657017223, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0], [0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.000622938805423232, 3.664345914254306e-05, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.00014657383657017223, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.00018321729571271528, 0.0003297911322828875, 0.0005130084279956027, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0003297911322828875, 0.00025650421399780137, 0.0003297911322828875, 0.00010993037742762916, 0.00018321729571271528, 0.00029314767314034447, 0.0, 0.00021986075485525832, 0.0], [0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.00036643459142543056, 0.0, 0.0007695126419934042, 0.00029314767314034447, 0.0005496518871381459, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.00029314767314034447, 0.0, 0.0, 0.00043972150971051665, 0.0, 0.00029314767314034447, 3.664345914254306e-05, 7.328691828508612e-05, 7.328691828508612e-05, 7.328691828508612e-05, 0.00047636496885305975, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.00029314767314034447, 0.0, 0.0010260168559912055, 0.0, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0005130084279956027, 0.0, 0.00018321729571271528, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0004030780505679736, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.00014657383657017223, 0.0], [0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.0005130084279956027, 7.328691828508612e-05, 0.00036643459142543056, 0.00010993037742762916, 0.00018321729571271528, 0.0005496518871381459, 0.00047636496885305975, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0004030780505679736, 0.00018321729571271528, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.00018321729571271528, 0.0005862953462806889, 0.0010626603151337487, 0.0004030780505679736, 0.0, 7.328691828508612e-05, 0.0], [0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.00021986075485525832, 0.00043972150971051665, 0.00029314767314034447, 0.0003297911322828875, 7.328691828508612e-05, 0.00014657383657017223, 0.0, 0.00018321729571271528, 0.0, 0.00014657383657017223, 0.00018321729571271528, 0.0, 0.0, 0.00025650421399780137, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 7.328691828508612e-05, 3.664345914254306e-05, 0.0], [0.0022718944668376696, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0008794430194210333, 0.00021986075485525832, 7.328691828508612e-05, 0.00036643459142543056, 0.00047636496885305975, 0.00036643459142543056, 0.0010260168559912055, 0.0005496518871381459, 0.0, 7.328691828508612e-05, 0.0006962257237083181, 0.00029314767314034447, 7.328691828508612e-05, 3.664345914254306e-05, 0.00036643459142543056, 0.0, 0.00047636496885305975, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.00021986075485525832, 0.00018321729571271528, 0.0, 0.00010993037742762916, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005862953462806889, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 7.328691828508612e-05, 0.0, 0.00010993037742762916, 0.0005130084279956027, 0.0, 0.0, 0.0, 0.00010993037742762916, 7.328691828508612e-05, 0.0, 0.00029314767314034447, 0.0003297911322828875, 0.0, 0.000659582264565775, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.000622938805423232, 0.0, 0.0007328691828508611, 0.00043972150971051665, 0.00021986075485525832, 0.0006962257237083181, 0.00021986075485525832, 0.00025650421399780137, 0.00010993037742762916, 0.00029314767314034447, 0.0004030780505679736, 0.00018321729571271528, 0.000659582264565775, 0.0008427995602784902, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0003297911322828875, 0.0005130084279956027, 0.00029314767314034447, 0.0010626603151337487, 0.0, 0.00025650421399780137, 7.328691828508612e-05], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.00014657383657017223, 3.664345914254306e-05, 0.00018321729571271528, 0.00010993037742762916, 0.00010993037742762916, 0.00014657383657017223, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.00025650421399780137, 0.00021986075485525832, 7.328691828508612e-05, 0.0, 0.00010993037742762916, 0.0, 0.00021986075485525832, 0.0, 0.00010993037742762916, 7.328691828508612e-05, 7.328691828508612e-05, 0.00036643459142543056, 0.0, 3.664345914254306e-05, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.00018321729571271528, 0.00018321729571271528, 0.0005862953462806889, 7.328691828508612e-05, 0.0, 0.0006962257237083181, 0.00014657383657017223, 0.0, 0.0, 0.00010993037742762916, 0.00043972150971051665, 0.00018321729571271528, 0.0005130084279956027, 0.0007328691828508611, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.00018321729571271528, 7.328691828508612e-05, 0.00021986075485525832, 0.00036643459142543056, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.00021986075485525832, 0.00014657383657017223, 0.00018321729571271528, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0005496518871381459, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0], [0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0006962257237083181, 0.0004030780505679736, 0.00010993037742762916, 0.0005496518871381459, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0003297911322828875, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.00047636496885305975, 0.0, 0.0, 0.0], [0.0004030780505679736, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.00014657383657017223, 0.0, 0.0, 0.0003297911322828875, 0.0, 7.328691828508612e-05, 0.0, 0.00018321729571271528, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.00036643459142543056, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.00018321729571271528, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0006962257237083181, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0006962257237083181, 0.00036643459142543056, 0.0, 0.0, 0.00047636496885305975, 0.0, 0.00018321729571271528, 7.328691828508612e-05, 0.00010993037742762916, 7.328691828508612e-05, 0.0, 0.002015390252839868, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.00021986075485525832, 0.0, 0.00014657383657017223, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00029314767314034447, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0021986075485525836, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 0.0, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00047636496885305975, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005862953462806889, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0009893733968486624, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 0.00018321729571271528, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0009527299377061195, 0.0, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.00014657383657017223, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.00029314767314034447, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.000659582264565775, 0.0, 0.0, 0.0, 0.0, 0.0005130084279956027, 0.00043972150971051665, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0006962257237083181, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.002711615976548186, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.000622938805423232, 0.00018321729571271528, 0.0, 0.00010993037742762916, 0.00029314767314034447, 0.0, 3.664345914254306e-05, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.00025650421399780137, 0.00014657383657017223, 0.00014657383657017223, 3.664345914254306e-05, 0.00010993037742762916, 0.00018321729571271528, 0.0, 0.00025650421399780137, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.00018321729571271528, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0015023818248442653, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.001832172957127153, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0006962257237083181, 0.00047636496885305975, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.001355807988274093, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0006962257237083181, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0005130084279956027, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.00036643459142543056, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0009160864785635764, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0021619640894100403, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.00025650421399780137, 0.0, 0.0, 0.00025650421399780137, 3.664345914254306e-05, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.001282521069989007, 0.0, 0.0, 0.0, 0.0, 0.0007695126419934042, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0007695126419934042, 3.664345914254306e-05, 0.0, 0.0, 0.00021986075485525832, 0.00018321729571271528, 0.0011725906925613779, 0.0004030780505679736, 0.0, 0.0, 7.328691828508612e-05, 0.00029314767314034447, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0005862953462806889, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0029314767314034445, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0021619640894100403, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001209234151703921, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0006962257237083181, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0015390252839868083, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005130084279956027, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0007328691828508611, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005496518871381459, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0, 0.0, 0.0, 0.0022718944668376696, 0.0, 0.0, 0.0, 0.0010260168559912055, 0.0, 0.0, 0.0010260168559912055, 0.0, 0.0028948332722609016, 0.001282521069989007, 0.0, 0.0, 0.0006962257237083181, 0.0, 0.0, 0.00021986075485525832, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00043972150971051665, 0.0, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 7.328691828508612e-05, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00025650421399780137, 7.328691828508612e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0021253206302674975, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.00021986075485525832, 0.00021986075485525832, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008061561011359472, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.00029314767314034447, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.00014657383657017223, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00131916452913155, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0, 0.0, 0.00010993037742762916, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005862953462806889, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 3.664345914254306e-05, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00043972150971051665, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.00043972150971051665, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0009893733968486624, 0.00047636496885305975, 7.328691828508612e-05, 7.328691828508612e-05, 0.001282521069989007, 0.005020153902528399, 0.0005862953462806889, 0.0, 0.0013924514474166361, 0.0016123122022718944, 0.0010626603151337487, 0.0005862953462806889, 7.328691828508612e-05, 0.00014657383657017223, 0.0, 0.0008061561011359472, 0.0003297911322828875, 0.0007695126419934042, 0.0005130084279956027, 0.0017222425796995235, 0.00018321729571271528, 0.0, 0.0, 0.00014657383657017223], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0006962257237083181, 0.00010993037742762916, 0.0005862953462806889, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 0.0015023818248442653, 0.0, 0.00010993037742762916, 0.0, 0.00029314767314034447, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0005130084279956027, 0.0, 0.0011359472334188348, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 0.00029314767314034447, 0.0, 0.00010993037742762916, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.00018321729571271528, 0.0, 0.0, 7.328691828508612e-05], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.00021986075485525832, 0.00014657383657017223, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00029314767314034447, 0.00010993037742762916, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.00018321729571271528, 3.664345914254306e-05, 7.328691828508612e-05, 0.00018321729571271528, 0.00025650421399780137, 0.00025650421399780137, 3.664345914254306e-05, 0.00043972150971051665, 0.0003297911322828875, 0.00036643459142543056, 0.00014657383657017223, 0.0, 0.00025650421399780137, 0.0, 0.00018321729571271528, 0.00014657383657017223, 0.00018321729571271528, 0.0, 0.00021986075485525832, 0.00018321729571271528, 0.00021986075485525832, 0.00010993037742762916, 0.00018321729571271528], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0], [0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0003297911322828875, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0], [0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00025650421399780137, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 3.664345914254306e-05, 7.328691828508612e-05, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.00018321729571271528, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 3.664345914254306e-05, 0.00010993037742762916, 0.00018321729571271528, 7.328691828508612e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.00014657383657017223, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 7.328691828508612e-05, 0.00025650421399780137, 0.0, 3.664345914254306e-05, 0.0004030780505679736, 0.00021986075485525832, 0.00025650421399780137, 0.0, 0.00021986075485525832, 0.0, 0.0005496518871381459, 3.664345914254306e-05, 3.664345914254306e-05, 0.00036643459142543056, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0005130084279956027, 0.0, 0.0, 0.0, 0.00010993037742762916], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0004030780505679736, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.00021986075485525832, 0.00010993037742762916, 0.0005862953462806889, 0.0, 0.00036643459142543056, 0.00036643459142543056, 0.0010626603151337487, 0.00014657383657017223, 0.0, 0.0008794430194210333, 0.00010993037742762916, 0.00014657383657017223, 0.00021986075485525832, 3.664345914254306e-05, 0.0016489556614144375, 0.0, 0.0, 0.00010993037742762916, 0.00047636496885305975, 0.0, 0.0016123122022718944, 0.0008794430194210333, 7.328691828508612e-05, 0.00021986075485525832, 0.00018321729571271528], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.00014657383657017223, 0.0, 3.664345914254306e-05, 0.0003297911322828875, 0.00010993037742762916, 0.000659582264565775, 0.0, 0.00018321729571271528, 0.0003297911322828875, 0.00010993037742762916, 0.00021986075485525832, 7.328691828508612e-05, 0.00018321729571271528, 0.0, 0.00010993037742762916, 0.0, 7.328691828508612e-05, 0.00036643459142543056, 0.0005862953462806889, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.00014657383657017223, 0.0004030780505679736, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0008427995602784902, 7.328691828508612e-05, 0.00014657383657017223, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.00025650421399780137, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.00014657383657017223, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.00029314767314034447, 3.664345914254306e-05, 0.00014657383657017223, 0.0005862953462806889, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.00014657383657017223, 0.00014657383657017223, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00025650421399780137, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0009160864785635764, 0.00014657383657017223, 0.0, 0.00043972150971051665, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.00043972150971051665, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.004067423964822279, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0022352510076951264, 0.0, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00036643459142543056, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0005862953462806889, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001942103334554782, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0010626603151337487, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0010993037742762918, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0007695126419934042, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0010626603151337487, 0.0, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.002418468303407842, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00043972150971051665, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0006962257237083181, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005862953462806889, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0003297911322828875, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0005862953462806889, 0.0, 0.0, 0.0, 0.0, 0.008208134847929644, 0.0005130084279956027, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0009893733968486624, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0, 0.00018321729571271528, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.00025650421399780137, 0.0, 0.0, 0.00025650421399780137, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 0.0021986075485525836, 0.0, 0.0, 0.001282521069989007, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0005130084279956027, 3.664345914254306e-05, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.004250641260534995, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001942103334554782, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.00018321729571271528, 0.0, 0.00018321729571271528, 0.0, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.00018321729571271528, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00047636496885305975, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.001978746793697325, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 7.328691828508612e-05, 0.0, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.001282521069989007, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.00047636496885305975, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0009527299377061195, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00047636496885305975, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.00029314767314034447, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0008427995602784902, 0.0, 0.0, 0.0, 0.002015390252839868, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0010993037742762918, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.001978746793697325, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008427995602784902, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.00010993037742762916, 0.0007328691828508611, 0.00010993037742762916, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0009527299377061195, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0009527299377061195, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 0.005423231953096372, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0009160864785635764, 0.0, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.001209234151703921, 0.0, 0.00036643459142543056, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.0004030780505679736, 0.0008794430194210333, 0.0, 0.0, 0.0008427995602784902, 0.00029314767314034447, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0022718944668376696, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0009527299377061195, 0.00010993037742762916, 0.00025650421399780137, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0009160864785635764, 0.0, 3.664345914254306e-05, 0.0011725906925613779, 0.00043972150971051665, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.00021986075485525832, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0029681201905459877, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0010260168559912055, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 0.00014657383657017223, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.00018321729571271528, 7.328691828508612e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00036643459142543056, 0.00047636496885305975, 0.0, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00018321729571271528, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.00021986075485525832, 0.0, 0.00014657383657017223, 0.0, 0.00014657383657017223, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.00018321729571271528, 0.0, 0.0], [0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.00018321729571271528, 0.0, 0.0008427995602784902, 0.00036643459142543056, 0.000622938805423232, 0.0, 0.0, 0.0004030780505679736, 0.0008061561011359472, 0.00021986075485525832, 0.0003297911322828875, 0.0007695126419934042, 0.0007695126419934042, 0.0, 0.000622938805423232, 0.00043972150971051665, 0.00043972150971051665, 0.0009893733968486624, 0.0005496518871381459, 0.00018321729571271528, 0.0, 0.0, 0.0], [0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.00014657383657017223, 3.664345914254306e-05, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.00047636496885305975, 0.0004030780505679736, 0.00010993037742762916, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0005496518871381459, 0.00014657383657017223, 0.00010993037742762916, 0.0005496518871381459, 0.0007328691828508611, 0.00043972150971051665, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.00025650421399780137, 0.0, 0.00029314767314034447, 7.328691828508612e-05, 0.00010993037742762916, 0.0, 0.0, 0.00029314767314034447, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.0, 0.0005130084279956027, 0.0, 0.0007328691828508611, 3.664345914254306e-05, 0.00021986075485525832, 0.00014657383657017223, 0.0007328691828508611, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0003297911322828875, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 0.00047636496885305975, 0.0, 0.0004030780505679736, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0007695126419934042, 0.0, 0.00018321729571271528, 0.0007695126419934042, 0.0005862953462806889, 0.00014657383657017223, 0.0014657383657017222, 0.0, 3.664345914254306e-05, 0.0, 0.0008061561011359472, 0.00018321729571271528, 0.00029314767314034447, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.000659582264565775, 0.0005496518871381459, 0.00018321729571271528, 0.0, 3.664345914254306e-05, 0.00021986075485525832, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0005862953462806889, 0.00029314767314034447, 3.664345914254306e-05, 7.328691828508612e-05, 3.664345914254306e-05, 0.00025650421399780137, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0004030780505679736, 0.0, 0.00014657383657017223, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0004030780505679736, 0.00010993037742762916, 0.0004030780505679736, 3.664345914254306e-05, 0.0, 3.664345914254306e-05], [0.00043972150971051665, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.00010993037742762916, 0.0004030780505679736, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 0.0, 0.0], [0.0011725906925613779, 0.0, 0.0, 0.0, 0.0, 0.0009160864785635764, 0.00036643459142543056, 0.00025650421399780137, 0.0004030780505679736, 0.00010993037742762916, 0.0008061561011359472, 0.000659582264565775, 0.0015023818248442653, 0.0, 0.00010993037742762916, 0.0022718944668376696, 0.0006962257237083181, 0.0005496518871381459, 0.0004030780505679736, 0.0015756687431293514, 0.0011725906925613779, 0.0, 0.00047636496885305975, 0.0004030780505679736, 0.0005862953462806889, 3.664345914254306e-05, 0.001245877610846464, 0.0016123122022718944, 0.00029314767314034447, 0.0007695126419934042, 0.00021986075485525832], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 7.328691828508612e-05, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0004030780505679736, 0.0, 3.664345914254306e-05, 0.0, 0.0003297911322828875, 0.00029314767314034447, 0.0016123122022718944, 0.0, 0.00021986075485525832, 0.0, 7.328691828508612e-05, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 3.664345914254306e-05, 0.0003297911322828875, 0.0, 3.664345914254306e-05, 0.0, 0.00029314767314034447, 0.0, 0.00018321729571271528, 0.00018321729571271528, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 0.00010993037742762916], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.001209234151703921, 0.00029314767314034447, 0.0, 7.328691828508612e-05, 0.0, 0.00029314767314034447, 0.00010993037742762916, 0.00014657383657017223, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.00010993037742762916, 0.00010993037742762916, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.00018321729571271528, 3.664345914254306e-05, 0.0003297911322828875, 0.0, 0.00021986075485525832, 0.0, 0.00036643459142543056, 0.0, 0.0, 7.328691828508612e-05, 0.00014657383657017223, 0.00018321729571271528, 0.00029314767314034447, 0.00010993037742762916, 7.328691828508612e-05, 0.0, 0.00047636496885305975, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.000622938805423232, 0.0, 7.328691828508612e-05, 0.0], [0.0015023818248442653, 0.0, 0.0, 0.0, 0.0, 0.000659582264565775, 0.0008794430194210333, 0.00036643459142543056, 3.664345914254306e-05, 0.0, 0.0003297911322828875, 0.00010993037742762916, 0.0005130084279956027, 0.0, 3.664345914254306e-05, 0.00014657383657017223, 0.0005862953462806889, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.0, 0.00036643459142543056, 0.00043972150971051665, 0.00010993037742762916, 0.0010993037742762918, 0.00014657383657017223, 0.0007328691828508611, 0.00014657383657017223, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.00018321729571271528, 0.0, 0.00018321729571271528, 0.000659582264565775, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0005130084279956027, 3.664345914254306e-05, 0.00036643459142543056, 0.0, 0.00018321729571271528, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005496518871381459, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 0.00025650421399780137, 0.0, 0.00036643459142543056, 0.00014657383657017223, 3.664345914254306e-05, 0.00018321729571271528, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0008794430194210333, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0013924514474166361, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.000659582264565775, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.001905459875412239, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0009160864785635764, 0.0004030780505679736, 0.0, 0.0, 0.00036643459142543056, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00021986075485525832, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0016855991205569805, 0.0, 0.0013924514474166361, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008061561011359472, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0011359472334188348, 0.0, 0.0, 3.664345914254306e-05, 0.00018321729571271528, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0010260168559912055, 0.0, 0.0, 0.0, 0.0, 0.0007695126419934042, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.00047636496885305975, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005496518871381459, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00036643459142543056, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.00014657383657017223, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.00043972150971051665, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.001355807988274093, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.000622938805423232, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0008061561011359472, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0006962257237083181, 0.00018321729571271528, 0.0, 3.664345914254306e-05, 0.0008061561011359472, 0.00018321729571271528, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.0011359472334188348, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0009160864785635764, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0016123122022718944, 0.00036643459142543056, 0.00010993037742762916, 3.664345914254306e-05, 0.0003297911322828875, 0.0004030780505679736, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.00010993037742762916, 0.0, 0.0, 0.00047636496885305975, 0.00021986075485525832, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.00018321729571271528, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.00021986075485525832], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00047636496885305975, 0.0, 0.0, 0.0, 0.0, 0.0009160864785635764, 0.0007328691828508611, 0.00036643459142543056, 3.664345914254306e-05, 7.328691828508612e-05, 0.0005496518871381459, 0.00010993037742762916, 3.664345914254306e-05, 0.000659582264565775, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0009527299377061195, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.00010993037742762916, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0005496518871381459, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0006962257237083181, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0005862953462806889, 0.00036643459142543056, 7.328691828508612e-05, 0.00018321729571271528, 0.00047636496885305975, 0.0005496518871381459, 0.0, 0.00014657383657017223, 0.0, 3.664345914254306e-05, 0.00018321729571271528, 0.0, 7.328691828508612e-05, 0.00029314767314034447, 0.00014657383657017223, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.00014657383657017223, 0.00036643459142543056, 0.0, 0.0, 0.00029314767314034447, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 0.0, 0.00010993037742762916, 7.328691828508612e-05, 0.00010993037742762916, 0.0, 0.00014657383657017223, 0.0005130084279956027, 0.0, 3.664345914254306e-05, 0.0003297911322828875, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.00018321729571271528, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0007695126419934042, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0010626603151337487, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.00025650421399780137, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0009160864785635764, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0015390252839868083, 7.328691828508612e-05, 0.0, 0.00010993037742762916, 0.0, 0.00010993037742762916, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005862953462806889, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0004030780505679736, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0005130084279956027, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00043972150971051665, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.00029314767314034447, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008427995602784902, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.000622938805423232, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00018321729571271528, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.000659582264565775, 0.0, 0.0, 0.0, 0.0006962257237083181, 0.0, 0.00014657383657017223, 0.0, 0.0023451813851227557, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.001282521069989007, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.00047636496885305975, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0003297911322828875, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.000622938805423232, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0031513374862587027, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0015023818248442653, 0.0, 0.0, 0.0, 0.0, 0.0, 0.000622938805423232, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0011725906925613779, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008061561011359472, 0.0, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0009160864785635764, 0.0, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.00018321729571271528, 0.0, 0.00018321729571271528, 0.0, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0009527299377061195, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.009857090509344081, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008427995602784902, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00021986075485525832, 0.0, 7.328691828508612e-05, 0.0, 0.00043972150971051665, 0.0, 0.00010993037742762916, 7.328691828508612e-05, 0.0007328691828508611, 0.0, 0.00014657383657017223, 0.0, 0.0, 7.328691828508612e-05, 0.00014657383657017223, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0007328691828508611, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008427995602784902, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.000659582264565775, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.0, 0.0005862953462806889, 0.0, 0.0, 0.0, 0.001209234151703921, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.00014657383657017223, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00021986075485525832, 7.328691828508612e-05, 0.0, 0.0006962257237083181, 0.0, 0.0003297911322828875, 0.00014657383657017223, 0.0, 7.328691828508612e-05, 0.0, 0.00021986075485525832, 0.00010993037742762916, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.001282521069989007, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008794430194210333, 0.00025650421399780137, 0.0, 0.0, 0.00018321729571271528, 0.00018321729571271528, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.00029314767314034447, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00029314767314034447, 0.0, 0.0007328691828508611, 3.664345914254306e-05, 0.00018321729571271528, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0, 0.0003297911322828875, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.00029314767314034447, 3.664345914254306e-05, 7.328691828508612e-05, 3.664345914254306e-05, 0.00021986075485525832, 0.0, 0.00021986075485525832, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0021253206302674975, 0.00010993037742762916, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.004946866984243312, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.00021986075485525832, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0005130084279956027, 0.00010993037742762916, 0.00043972150971051665, 7.328691828508612e-05, 0.00036643459142543056, 0.00010993037742762916, 0.00018321729571271528, 0.0, 0.0008427995602784902, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.00025650421399780137, 0.0, 0.00018321729571271528, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.00010993037742762916, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.00021986075485525832, 3.664345914254306e-05, 0.0, 0.0, 0.00029314767314034447, 0.00025650421399780137, 0.0, 0.0003297911322828875, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0006962257237083181, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.000622938805423232, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00036643459142543056, 3.664345914254306e-05, 0.0, 0.00018321729571271528, 0.0, 0.002052033711982411, 0.00025650421399780137, 0.0, 0.00018321729571271528, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00018321729571271528, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0004030780505679736, 0.0006962257237083181, 0.0009893733968486624, 0.00010993037742762916, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0005496518871381459, 0.0005496518871381459, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.00021986075485525832, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0009893733968486624, 0.00014657383657017223, 0.0, 3.664345914254306e-05, 0.0, 0.0008794430194210333, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.00010993037742762916, 0.0005130084279956027, 0.0, 0.0, 0.00014657383657017223, 0.00021986075485525832, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0005862953462806889, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.00025650421399780137, 0.00025650421399780137, 0.00010993037742762916, 0.00010993037742762916, 0.00025650421399780137, 0.000622938805423232, 0.0021619640894100403, 3.664345914254306e-05, 0.0, 0.00018321729571271528, 0.00036643459142543056, 0.00010993037742762916, 0.00018321729571271528, 0.00014657383657017223, 0.0, 0.00029314767314034447, 7.328691828508612e-05, 0.00010993037742762916, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.00018321729571271528, 0.00010993037742762916], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0017222425796995235, 0.00047636496885305975, 0.0003297911322828875, 0.0, 0.0007695126419934042, 0.0013924514474166361, 0.000622938805423232, 0.0, 0.0, 0.0, 0.000622938805423232, 0.00029314767314034447, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0009160864785635764, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0006962257237083181, 0.0, 0.0, 0.00018321729571271528], [0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0009527299377061195, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 7.328691828508612e-05, 0.00018321729571271528, 0.0, 0.0005130084279956027, 0.00010993037742762916, 0.0005130084279956027, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.00025650421399780137, 7.328691828508612e-05, 7.328691828508612e-05, 0.0023085379259802125, 0.00010993037742762916, 0.0009527299377061195, 0.00010993037742762916, 0.00021986075485525832, 0.0, 0.00021986075485525832, 0.0005496518871381459, 7.328691828508612e-05, 0.0004030780505679736, 0.00021986075485525832, 0.0, 0.0, 0.00010993037742762916, 0.0005130084279956027, 0.0, 0.0007695126419934042, 0.002674972517405643, 0.0, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.00025650421399780137, 0.00010993037742762916, 7.328691828508612e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.00010993037742762916, 7.328691828508612e-05, 7.328691828508612e-05, 0.00029314767314034447, 0.0004030780505679736, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0011725906925613779, 3.664345914254306e-05, 0.0, 0.0, 0.00018321729571271528, 3.664345914254306e-05, 0.00025650421399780137, 0.0009893733968486624, 0.00018321729571271528, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00021986075485525832, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0], [0.001245877610846464, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0007695126419934042, 0.0005496518871381459, 0.0004030780505679736, 7.328691828508612e-05, 0.00025650421399780137, 0.00018321729571271528, 0.00131916452913155, 0.0004030780505679736, 0.00021986075485525832, 0.00014657383657017223, 0.0004030780505679736, 0.00043972150971051665, 0.00014657383657017223, 0.0, 0.00021986075485525832, 0.0, 0.0016123122022718944, 0.00018321729571271528, 0.0009527299377061195, 0.0, 0.00018321729571271528, 7.328691828508612e-05, 0.0, 0.0028948332722609016, 0.0], [0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0003297911322828875, 0.0005130084279956027, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0], [0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.000622938805423232, 0.00021986075485525832, 0.0010260168559912055, 3.664345914254306e-05, 0.0, 0.00029314767314034447, 0.0008061561011359472, 0.00010993037742762916, 0.0, 0.0, 0.0011359472334188348, 0.0, 0.0005862953462806889, 0.0, 0.0007328691828508611, 0.0, 0.00131916452913155, 0.0, 0.00021986075485525832, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008061561011359472, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0007328691828508611, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.00018321729571271528, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.0008427995602784902, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0022718944668376696, 0.0, 0.0, 0.00010993037742762916, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0003297911322828875, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.0, 3.664345914254306e-05, 0.0, 0.0003297911322828875, 0.0, 0.0009893733968486624, 0.000622938805423232, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.00014657383657017223, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00021986075485525832, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0008427995602784902, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.00018321729571271528, 0.0, 0.0, 3.664345914254306e-05, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0005496518871381459, 0.00025650421399780137, 0.0, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0007328691828508611, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.001832172957127153, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.00014657383657017223, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.001209234151703921, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0010993037742762918, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.0, 0.00021986075485525832, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.00029314767314034447, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0], [0.000659582264565775, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.00018321729571271528, 0.0005130084279956027, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0010626603151337487, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0007328691828508611, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0007328691828508611, 0.0, 0.0, 0.0, 0.0015756687431293514, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001245877610846464, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001355807988274093, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00025650421399780137, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00029314767314034447, 0.0005862953462806889, 0.00029314767314034447, 0.0004030780505679736, 0.00036643459142543056, 0.00010993037742762916, 0.001245877610846464, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0021253206302674975, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008794430194210333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0004030780505679736, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00047636496885305975, 0.0008061561011359472, 0.00014657383657017223, 0.00014657383657017223, 7.328691828508612e-05, 7.328691828508612e-05, 0.00010993037742762916, 0.0, 0.00043972150971051665, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.0007695126419934042, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0011359472334188348, 7.328691828508612e-05, 0.00018321729571271528, 0.00036643459142543056, 0.00018321729571271528, 0.00021986075485525832, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0007328691828508611, 0.000659582264565775, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.00021986075485525832, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.000622938805423232, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0015756687431293514, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0005862953462806889, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00036643459142543056, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0004030780505679736, 0.0008427995602784902, 0.0005130084279956027, 0.00025650421399780137, 0.0005130084279956027, 0.00047636496885305975, 0.0013924514474166361, 0.00018321729571271528, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0016855991205569805, 0.0, 3.664345914254306e-05, 0.0, 0.00021986075485525832, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0005496518871381459, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0005862953462806889, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008061561011359472, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 7.328691828508612e-05, 3.664345914254306e-05, 0.00029314767314034447, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0005496518871381459, 3.664345914254306e-05, 0.00010993037742762916, 3.664345914254306e-05, 0.00036643459142543056, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0005496518871381459, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0003297911322828875, 0.00010993037742762916, 3.664345914254306e-05, 0.0003297911322828875, 0.00014657383657017223, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0003297911322828875, 3.664345914254306e-05, 0.0, 0.00018321729571271528, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.00018321729571271528, 0.0006962257237083181, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.00010993037742762916, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00036643459142543056, 0.00010993037742762916, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0010993037742762918, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0010260168559912055, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0008427995602784902, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0010993037742762918, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0004030780505679736, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.00025650421399780137, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.00029314767314034447, 7.328691828508612e-05, 0.00043972150971051665, 0.0, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0007328691828508611, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005130084279956027, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.00029314767314034447, 0.0, 3.664345914254306e-05, 0.0, 0.0005496518871381459, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.00029314767314034447, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0008061561011359472, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0], [0.0005496518871381459, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00025650421399780137, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0005130084279956027, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0010260168559912055, 0.0, 0.00036643459142543056, 0.0, 0.00047636496885305975, 0.00036643459142543056, 0.0, 0.0011359472334188348, 0.001905459875412239, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0005862953462806889, 0.001245877610846464, 0.0, 0.0, 0.00036643459142543056, 0.0008427995602784902, 0.0, 0.0010626603151337487, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0005496518871381459, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.000622938805423232, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0005862953462806889, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00014657383657017223, 0.0008061561011359472, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.004507145474532796, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0009160864785635764, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.000659582264565775, 0.0, 3.664345914254306e-05, 0.00021986075485525832, 0.0, 7.328691828508612e-05, 0.00047636496885305975, 0.0, 0.0, 0.0005496518871381459, 0.0, 0.0, 0.00047636496885305975, 0.0, 0.00010993037742762916, 0.0, 0.00014657383657017223, 0.0], [0.00047636496885305975, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0009160864785635764, 0.0, 0.0003297911322828875, 3.664345914254306e-05, 0.00018321729571271528, 3.664345914254306e-05, 0.0, 0.0, 0.000659582264565775, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.00021986075485525832, 0.00018321729571271528, 0.0004030780505679736, 0.0, 3.664345914254306e-05, 0.00047636496885305975, 3.664345914254306e-05, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.001942103334554782, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00021986075485525832, 0.0, 0.00025650421399780137, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.00029314767314034447, 0.0003297911322828875, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0003297911322828875, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00029314767314034447, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.00029314767314034447, 0.0, 0.00021986075485525832, 0.001355807988274093, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.00029314767314034447, 3.664345914254306e-05, 0.00018321729571271528, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00047636496885305975, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0010626603151337487, 0.0, 0.00010993037742762916, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.00021986075485525832, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0004030780505679736, 0.0004030780505679736, 0.0, 0.00014657383657017223, 0.00029314767314034447, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00025650421399780137, 3.664345914254306e-05, 0.0, 0.00036643459142543056, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.00043972150971051665, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 7.328691828508612e-05, 0.0, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00021986075485525832, 0.0, 7.328691828508612e-05, 0.0005862953462806889, 0.0, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0011359472334188348, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0008427995602784902, 0.00021986075485525832, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0007695126419934042, 0.0, 0.00010993037742762916, 0.0, 0.00010993037742762916, 0.00010993037742762916, 0.00010993037742762916, 0.00131916452913155, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.000622938805423232, 0.0, 0.0, 0.00043972150971051665, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.001832172957127153, 0.00029314767314034447, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.00029314767314034447, 0.0, 0.00029314767314034447, 0.0, 0.0008794430194210333, 0.00010993037742762916, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00025650421399780137, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 7.328691828508612e-05, 0.00010993037742762916, 0.0005862953462806889, 0.00018321729571271528, 0.0004030780505679736, 0.0, 0.00018321729571271528, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00025650421399780137, 0.0, 0.00010993037742762916, 0.0, 0.0003297911322828875, 3.664345914254306e-05, 0.0005496518871381459, 0.0, 0.0003297911322828875, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.001942103334554782, 0.00029314767314034447, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0015023818248442653, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.00010993037742762916, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00029314767314034447, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.00014657383657017223, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0026383290582631, 0.00036643459142543056, 0.0, 0.0, 0.00018321729571271528, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0007328691828508611, 0.00021986075485525832, 7.328691828508612e-05, 0.0, 0.00018321729571271528, 0.00018321729571271528, 0.00010993037742762916, 0.00025650421399780137, 0.00047636496885305975, 0.0, 0.00018321729571271528, 0.00029314767314034447, 3.664345914254306e-05, 0.0015390252839868083, 7.328691828508612e-05, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.00010993037742762916, 0.00021986075485525832, 0.00025650421399780137, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0026383290582631, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0007695126419934042, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00029314767314034447, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0014290949065591792, 0.0, 0.0, 3.664345914254306e-05, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.00131916452913155, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.002418468303407842, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0010993037742762918, 0.0, 0.0, 0.0, 0.0, 0.000659582264565775, 3.664345914254306e-05, 0.0, 0.00029314767314034447, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0009160864785635764, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00047636496885305975, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0011359472334188348, 0.0, 0.0, 0.0, 0.0, 0.0008427995602784902, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0005862953462806889, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0011725906925613779, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.002052033711982411, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0007695126419934042, 0.00010993037742762916, 0.0, 0.00018321729571271528, 0.00021986075485525832, 0.00010993037742762916, 3.664345914254306e-05, 0.00014657383657017223, 0.0, 0.0, 0.00014657383657017223, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 0.00010993037742762916, 0.0, 0.00021986075485525832, 0.00014657383657017223, 7.328691828508612e-05, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0003297911322828875, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0006962257237083181, 0.0, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0008061561011359472, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.001832172957127153, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00010993037742762916, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005130084279956027, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.002015390252839868, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0016123122022718944, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00014657383657017223, 0.00010993037742762916, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 3.664345914254306e-05], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00043972150971051665, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.00036643459142543056, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0013924514474166361, 0.0010993037742762918, 0.0004030780505679736, 0.00036643459142543056, 0.0007328691828508611, 0.0003297911322828875, 0.00025650421399780137, 0.0004030780505679736, 0.0, 0.0, 0.0008427995602784902, 0.0015390252839868083, 0.0009527299377061195, 0.0004030780505679736, 0.00029314767314034447, 0.0005496518871381459, 0.0, 0.0010626603151337487, 0.0005130084279956027, 0.0014657383657017222, 7.328691828508612e-05, 0.00043972150971051665, 7.328691828508612e-05, 0.0, 0.0, 0.00043972150971051665], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.00014657383657017223, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.00010993037742762916, 0.00010993037742762916, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 7.328691828508612e-05, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.00025650421399780137, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 3.664345914254306e-05, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.00021986075485525832, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0017588860388420666, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 3.664345914254306e-05, 0.0, 7.328691828508612e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00047636496885305975, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.328691828508612e-05], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00025650421399780137], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00010993037742762916, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.664345914254306e-05], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00029314767314034447, 0.0, 0.0, 0.0, 3.664345914254306e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00018321729571271528, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00014657383657017223], [0.0, 0.0, 0.0, 0.0, 0.0, 0.00021986075485525832, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004030780505679736, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005862953462806889, 0.0, 0.0, 0.0, 0.0, 0.0]]}],
                        {"template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Trigrams"}, "xaxis": {"nticks": 961}},
                        {"responsive": true}
                    ).then(function(){
                            
var gd = document.getElementById('f56f2350-d026-48e5-a070-1d7c97823107');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>


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


<div>
        
        
            <div id="8b6dc234-c4d7-4205-9333-9e9ce721ec1d" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};
                    
                if (document.getElementById("8b6dc234-c4d7-4205-9333-9e9ce721ec1d")) {
                    Plotly.newPlot(
                        '8b6dc234-c4d7-4205-9333-9e9ce721ec1d',
                        [{"alignmentgroup": "True", "hoverlabel": {"namelength": 0}, "hovertemplate": "Symbol=%{x}<br>Frequency=%{y}", "legendgroup": "", "marker": {"color": "#636efa"}, "name": "", "offsetgroup": "", "orientation": "v", "showlegend": false, "textposition": "auto", "type": "bar", "x": ["A", "THE", "OF", "AND", "IT", "IN", "UP", "OUT", "I", "YOUR", "ON", "TO", "GOOD", "HIGH", "FOR", "YOU", "HOT", "BACK", "WAY", "I'M", "MY", "JOB", "OFF", "ME", "&", "BIG", "TOUGH", "GO", "POINT", "BY", "YOUNG"], "xaxis": "x", "y": [196, 138, 106, 54, 47, 45, 39, 34, 33, 30, 26, 26, 23, 23, 22, 22, 22, 21, 21, 21, 21, 19, 18, 18, 18, 18, 17, 16, 16, 16, 15], "yaxis": "y"}],
                        {"barmode": "relative", "legend": {"tracegroupgap": 0}, "margin": {"t": 60}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "xaxis": {"anchor": "y", "domain": [0.0, 1.0], "title": {"text": "Symbol"}}, "yaxis": {"anchor": "x", "domain": [0.0, 1.0], "title": {"text": "Frequency"}}},
                        {"responsive": true}
                    ).then(function(){
                            
var gd = document.getElementById('8b6dc234-c4d7-4205-9333-9e9ce721ec1d');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>


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


<div>
        
        
            <div id="63e26e6b-f47c-47cb-bf4d-a170edb6b33b" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};
                    
                if (document.getElementById("63e26e6b-f47c-47cb-bf4d-a170edb6b33b")) {
                    Plotly.newPlot(
                        '63e26e6b-f47c-47cb-bf4d-a170edb6b33b',
                        [{"alignmentgroup": "True", "hoverlabel": {"namelength": 0}, "hovertemplate": "Tag=%{x}<br>Frequency=%{y}", "legendgroup": "", "marker": {"color": "#636efa"}, "name": "", "offsetgroup": "", "orientation": "v", "showlegend": false, "textposition": "auto", "type": "bar", "x": [".", "CC", "CD", "DT", "FW", "IN", "JJ", "MD", "NN", "NNP", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RP", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WP", "WRB"], "xaxis": "x", "y": [0.000164446637066272, 0.00493339911198816, 0.0059200789343857915, 0.037658279888176285, 0.000328893274132544, 0.020226936359151456, 0.02548922874527216, 0.001151126459463904, 0.1738200953790495, 0.6666666666666666, 0.007071205393849696, 0.001151126459463904, 0.00082223318533136, 0.010360138135175136, 0.0014800197335964479, 0.006248972208518336, 0.004604505837855616, 0.000164446637066272, 0.013320177602368031, 0.001315573096530176, 0.002302252918927808, 0.00082223318533136, 0.009209011675711231, 0.001808913007728992, 0.00164446637066272, 0.001315573096530176], "yaxis": "y"}],
                        {"barmode": "relative", "legend": {"tracegroupgap": 0}, "margin": {"t": 60}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "xaxis": {"anchor": "y", "domain": [0.0, 1.0], "title": {"text": "Tag"}}, "yaxis": {"anchor": "x", "domain": [0.0, 1.0], "title": {"text": "Frequency"}}},
                        {"responsive": true}
                    ).then(function(){
                            
var gd = document.getElementById('63e26e6b-f47c-47cb-bf4d-a170edb6b33b');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>


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


<div>
        
        
            <div id="3efab538-3fe3-47fc-8003-6de5d6be8982" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};
                    
                if (document.getElementById("3efab538-3fe3-47fc-8003-6de5d6be8982")) {
                    Plotly.newPlot(
                        '3efab538-3fe3-47fc-8003-6de5d6be8982',
                        [{"alignmentgroup": "True", "hoverlabel": {"namelength": 0}, "hovertemplate": "Tag=%{x}<br>Frequency_=%{y}", "legendgroup": "", "marker": {"color": "#636efa"}, "name": "", "offsetgroup": "", "orientation": "v", "showlegend": false, "textposition": "auto", "type": "bar", "x": [".", "CC", "CD", "DT", "FW", "IN", "JJ", "JJR", "JJS", "MD", "NN", "NNS", "POS", "PRP", "PRP$", "RB", "RP", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WP", "WRB"], "xaxis": "x", "y": [0.000164446637066272, 0.0123334977799704, 0.003124486104259168, 0.05837855615852656, 0.000164446637066272, 0.052458477224140765, 0.11264594639039632, 0.000657786548265088, 0.000493339911198816, 0.001973359644795264, 0.5357671435619141, 0.06018746916625555, 0.000493339911198816, 0.017595790166091103, 0.008715671764512416, 0.02548922874527216, 0.014142410787699391, 0.0042756125637230715, 0.000164446637066272, 0.025818122019404702, 0.005426739023186976, 0.031902647590856766, 0.011346817957572768, 0.01068903140930768, 0.002302252918927808, 0.001973359644795264, 0.001315573096530176], "yaxis": "y"}],
                        {"barmode": "relative", "legend": {"tracegroupgap": 0}, "margin": {"t": 60}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "xaxis": {"anchor": "y", "domain": [0.0, 1.0], "title": {"text": "Tag"}}, "yaxis": {"anchor": "x", "domain": [0.0, 1.0], "title": {"text": "Frequency_"}}},
                        {"responsive": true}
                    ).then(function(){
                            
var gd = document.getElementById('3efab538-3fe3-47fc-8003-6de5d6be8982');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>


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


<div>
        
        
            <div id="f0f3640f-1037-434d-87f1-2454d3ada26f" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};
                    
                if (document.getElementById("f0f3640f-1037-434d-87f1-2454d3ada26f")) {
                    Plotly.newPlot(
                        'f0f3640f-1037-434d-87f1-2454d3ada26f',
                        [{"name": "Uppercase", "type": "bar", "x": [".", "CC", "CD", "DT", "FW", "IN", "JJ", "MD", "NN", "NNP", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RP", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WP", "WRB", "JJR", "JJS", "TO"], "y": [0.000164446637066272, 0.00493339911198816, 0.0059200789343857915, 0.037658279888176285, 0.000328893274132544, 0.020226936359151456, 0.02548922874527216, 0.001151126459463904, 0.1738200953790495, 0.6666666666666666, 0.007071205393849696, 0.001151126459463904, 0.00082223318533136, 0.010360138135175136, 0.0014800197335964479, 0.006248972208518336, 0.004604505837855616, 0.000164446637066272, 0.013320177602368031, 0.001315573096530176, 0.002302252918927808, 0.00082223318533136, 0.009209011675711231, 0.001808913007728992, 0.00164446637066272, 0.001315573096530176, 0.0, 0.0, 0.0]}, {"name": "Lower", "type": "bar", "x": [".", "CC", "CD", "DT", "FW", "IN", "JJ", "MD", "NN", "NNP", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RP", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WP", "WRB", "JJR", "JJS", "TO"], "y": [0.000164446637066272, 0.0123334977799704, 0.003124486104259168, 0.05837855615852656, 0.000164446637066272, 0.052458477224140765, 0.11264594639039632, 0.001973359644795264, 0.5357671435619141, 0.0, 0.06018746916625555, 0.0, 0.000493339911198816, 0.017595790166091103, 0.008715671764512416, 0.02548922874527216, 0.014142410787699391, 0.000164446637066272, 0.025818122019404702, 0.005426739023186976, 0.031902647590856766, 0.011346817957572768, 0.01068903140930768, 0.002302252918927808, 0.001973359644795264, 0.001315573096530176, 0.000657786548265088, 0.000493339911198816, 0.0042756125637230715]}],
                        {"barmode": "stack", "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "xaxis": {"categoryorder": "category ascending"}},
                        {"responsive": true}
                    ).then(function(){
                            
var gd = document.getElementById('f0f3640f-1037-434d-87f1-2454d3ada26f');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>
