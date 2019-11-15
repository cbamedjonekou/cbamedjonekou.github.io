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
import seaborn as sns
import string
from os import listdir
from os.path import isfile, join

# Special methods/'magic' functions for the visualizations
sns.set()
%matplotlib inline
```
<h2 id= "DWC">Data Wrangling/Cleaning</h2>

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
filepath = '/Users/Chris/Desktop/WoF Final Round Puzzles/WoF_Merged.csv'
with open(filepath, 'w') as f:
    WoF_DF.to_csv(path_or_buf= f, index= False)
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

<h2 id="EDA">Exploratory Data Analysis</h2>

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

# Print our corpus for a quick view
# print(corpus)
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
wof_Letter_dist = pd.DataFrame.from_dict({'Symbol': letters,'Frequency': frequency})

# First 10 rows
wof_Letter_dist.head(10)
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



We'll also use the `sns.barplot()` function to visualize the frequency distribution


```python
sns.barplot(letters, frequency)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x11000f978>




![png](output_43_1.png)


For probabilities we'll modifying the line above by dividing each element by total corpus length. We'll also sort the plot by descending order (highest to lowest)


```python
# Sorts dataframe before plotting
wof_Letter_dist = wof_Letter_dist.sort_values(by= ['Frequency'], ascending= False)
sns.barplot(wof_Letter_dist['Symbol'], wof_Letter_dist['Frequency']/len(corpus))
```




    <matplotlib.axes._subplots.AxesSubplot at 0x112840c88>




![png](output_45_1.png)


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
    
    # Step 3: Plotting temp dataframes
    sns.barplot(tempDF['Symbol'], tempDF['Frequency']/length_holder[i], ax= axs.flatten()[i])
```


![png](output_54_0.png)


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

# Optional: print the new dictionary
# print(bigram_counter)
```

We'll search each element in our `WoF_DF['PUZZLE']` array and count how many times the bigram appears.


```python
# Step 3: Begins the counting, adding 1 for each key match
for elem in WoF_DF['PUZZLE']:
    for bigram in bigrams:
        if bigram in elem:
            bigram_counter[bigram] += 1
```

There are bigrams with a count of zero


```python
# Empty list to hold bigram with frequency of zero
zero_freq_list = []

# Searches for bigrams with frequency of zero
for bigram in bigrams:
    if bigram_counter[bigram] == 0:
        zero_freq_list.append(bigram)

# Prints list
print(zero_freq_list)
```

    ['  ', " '", ' -', ' ?', ' X', '&&', "&'", '&-', '&?', '&A', '&B', '&C', '&D', '&E', '&F', '&G', '&H', '&I', '&J', '&K', '&L', '&M', '&N', '&O', '&P', '&Q', '&R', '&S', '&T', '&U', '&V', '&W', '&X', '&Y', '&Z', "' ", "'&", "''", "'-", "'?", "'A", "'B", "'C", "'D", "'E", "'F", "'G", "'H", "'I", "'J", "'K", "'L", "'N", "'O", "'P", "'Q", "'U", "'W", "'X", "'Y", "'Z", '- ', '-&', "-'", '--', '-?', '-I', '-J', '-Q', '-V', '-X', '-Z', '? ', '?&', "?'", '?-', '??', '?A', '?B', '?C', '?D', '?E', '?F', '?G', '?H', '?I', '?J', '?K', '?L', '?M', '?N', '?O', '?P', '?Q', '?R', '?S', '?T', '?U', '?V', '?W', '?X', '?Y', '?Z', 'A&', "A'", 'A-', 'A?', 'AA', 'B&', "B'", 'B?', 'BF', 'BG', 'BK', 'BM', 'BN', 'BP', 'BQ', 'BX', 'BZ', 'C&', "C'", 'C-', 'C?', 'CB', 'CD', 'CF', 'CG', 'CJ', 'CM', 'CP', 'CQ', 'CV', 'CW', 'CX', 'CZ', 'D&', "D'", 'D?', 'DC', 'DN', 'DQ', 'DX', 'DZ', 'E&', 'E?', 'F&', "F'", 'F?', 'FC', 'FD', 'FG', 'FH', 'FJ', 'FK', 'FN', 'FP', 'FQ', 'FV', 'FX', 'FZ', 'G&', "G'", 'GC', 'GD', 'GF', 'GJ', 'GQ', 'GV', 'GX', 'GZ', 'H&', "H'", 'H?', 'HC', 'HJ', 'HQ', 'HV', 'HX', 'HZ', 'I&', 'I-', 'I?', 'IH', 'IW', 'IY', 'J ', 'J&', "J'", 'J-', 'J?', 'JB', 'JC', 'JD', 'JF', 'JG', 'JH', 'JJ', 'JK', 'JL', 'JM', 'JN', 'JP', 'JQ', 'JR', 'JS', 'JT', 'JV', 'JW', 'JX', 'JY', 'JZ', 'K&', "K'", 'K?', 'KD', 'KJ', 'KQ', 'KR', 'KV', 'KX', 'KZ', 'L&', "L'", 'L?', 'LH', 'LJ', 'LN', 'LQ', 'LX', 'LZ', 'M&', "M'", 'M?', 'MC', 'MG', 'MH', 'MJ', 'MK', 'ML', 'MQ', 'MR', 'MT', 'MV', 'MW', 'MX', 'MZ', 'N&', 'N?', 'NM', 'O&', "O'", 'O?', 'P&', "P'", 'P?', 'PJ', 'PN', 'PQ', 'PV', 'PX', 'PZ', 'Q ', 'Q&', "Q'", 'Q-', 'Q?', 'QA', 'QB', 'QC', 'QD', 'QE', 'QF', 'QG', 'QH', 'QI', 'QJ', 'QK', 'QL', 'QM', 'QN', 'QO', 'QP', 'QQ', 'QR', 'QS', 'QT', 'QV', 'QW', 'QX', 'QY', 'QZ', 'R&', "R'", 'R?', 'RX', 'RZ', 'S&', "S'", 'S-', 'S?', 'SB', 'SF', 'SR', 'SV', 'SX', 'SZ', 'T&', 'T?', 'TJ', 'TK', 'TN', 'TQ', 'TX', 'U&', 'U-', 'U?', 'UH', 'V&', "V'", 'V-', 'V?', 'VB', 'VC', 'VD', 'VF', 'VG', 'VH', 'VJ', 'VK', 'VL', 'VM', 'VN', 'VP', 'VQ', 'VR', 'VS', 'VT', 'VU', 'VW', 'VX', 'VZ', 'W&', "W'", 'W?', 'WC', 'WG', 'WJ', 'WM', 'WQ', 'WU', 'WV', 'WW', 'WX', 'WZ', 'X&', "X'", 'X?', 'XB', 'XD', 'XG', 'XJ', 'XK', 'XL', 'XM', 'XN', 'XQ', 'XR', 'XS', 'XV', 'XW', 'XX', 'XZ', 'Y&', 'Y?', 'YJ', 'YK', 'YQ', 'YV', 'YX', 'YY', 'YZ', 'Z&', "Z'", 'Z-', 'Z?', 'ZB', 'ZC', 'ZD', 'ZF', 'ZG', 'ZH', 'ZJ', 'ZK', 'ZM', 'ZN', 'ZP', 'ZQ', 'ZR', 'ZS', 'ZT', 'ZU', 'ZV', 'ZX']


We'll remove these so we can visualize our frequency distribution better


```python
for item in zero_freq_list:
    del bigram_counter[item]
```

Now we'll table the counts and visualize the results. Click the image to get a larger view.


```python
# Creating a dataframe called bigram_dist
symbols = np.array(list(bigram_counter.keys()))
frequencies = np.array(list(bigram_counter.values()))
bigram_dist = pd.DataFrame.from_dict({'Symbol': symbols,'Frequency': frequencies})

# Sorts dataframe before plotting
bigram_dist = bigram_dist.sort_values(by= ['Frequency'], ascending= False)

# Plots the first 200 entries
fig = plt.figure(figsize= (100, 100))
bigram_chart = sns.barplot(bigram_dist['Symbol'], 
                           bigram_dist['Frequency']/frequencies.sum())
bigram_chart.set_xticklabels(bigram_chart.get_xticklabels(), 
                             rotation=45, 
                             horizontalalignment='right',
                             fontweight='light',
                             fontsize='8');
```


![png](output_64_0.png)


The following line provides the first 20 entries of our sorted dataframe; In other words we have the top 20 most frequent bigrams printed. You can modify this line to view any section of the table (in case it's difficult to make out the axes). 


```python
bigram_dist.iloc[:20]
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
      <th>237</th>
      <td>IN</td>
      <td>510</td>
    </tr>
    <tr>
      <th>135</th>
      <td>E</td>
      <td>465</td>
    </tr>
    <tr>
      <th>526</th>
      <td>Y</td>
      <td>367</td>
    </tr>
    <tr>
      <th>361</th>
      <td>OU</td>
      <td>342</td>
    </tr>
    <tr>
      <th>320</th>
      <td>NG</td>
      <td>326</td>
    </tr>
    <tr>
      <th>2</th>
      <td>B</td>
      <td>295</td>
    </tr>
    <tr>
      <th>358</th>
      <td>OR</td>
      <td>279</td>
    </tr>
    <tr>
      <th>112</th>
      <td>D</td>
      <td>269</td>
    </tr>
    <tr>
      <th>447</th>
      <td>TH</td>
      <td>269</td>
    </tr>
    <tr>
      <th>180</th>
      <td>G</td>
      <td>264</td>
    </tr>
    <tr>
      <th>215</th>
      <td>HO</td>
      <td>262</td>
    </tr>
    <tr>
      <th>437</th>
      <td>T</td>
      <td>261</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>257</td>
    </tr>
    <tr>
      <th>155</th>
      <td>ER</td>
      <td>257</td>
    </tr>
    <tr>
      <th>65</th>
      <td>AN</td>
      <td>250</td>
    </tr>
    <tr>
      <th>206</th>
      <td>HE</td>
      <td>245</td>
    </tr>
    <tr>
      <th>69</th>
      <td>AR</td>
      <td>241</td>
    </tr>
    <tr>
      <th>243</th>
      <td>IT</td>
      <td>239</td>
    </tr>
    <tr>
      <th>227</th>
      <td>IC</td>
      <td>232</td>
    </tr>
    <tr>
      <th>15</th>
      <td>O</td>
      <td>231</td>
    </tr>
  </tbody>
</table>
</div>



We also have the `Symbol` column printed so we can identify when a sequence begins/ends with a space (also in case it's difficult to make out the axes). 


```python
bigram_dist['Symbol'].iloc[:20]
```




    237    IN
    135    E 
    526    Y 
    361    OU
    320    NG
    2       B
    358    OR
    112    D 
    447    TH
    180    G 
    215    HO
    437    T 
    1       A
    155    ER
    65     AN
    206    HE
    69     AR
    243    IT
    227    IC
    15      O
    Name: Symbol, dtype: object



<h3 id='3rd-order-approx'>$3$-$rd$ Order Approximations</h3>

We'll now consider [trigrams](https://en.wikipedia.org/wiki/Trigram), which is the [n-Order Approximation of English text](http://people.seas.harvard.edu/~jones/cscie129/nu_lectures/lecture2/info%20theory/Info_Theory_5.html) where $n = 3$. Trigrams are 3 symbol combinations (including white space) and will be considered next. 

The first steps are to create trigrams and dictionary of the trigrams to initialize our counter. 


```python
# Step 1: We get the cartesian product of corpus_index w/ itself (they're unique pairs)
trigrams = np.array([x+y+z for x in corpus_index for y in corpus_index for z in corpus_index])

# Step 2: Makes a dictionary: Each character in bigrams is a 'key' in the dictionary. 
# Each value is initialized to zero
trigram_counter = dict((character, 0) for character in trigrams)

# Optional: print the new dictionary
#print(trigram_counter.keys)
```

We'll search each element in our `WoF_DF['PUZZLE']` array and count how many times the trigram appears.


```python
# Step 3: Begins the counting, adding 1 for each key match
for elem in WoF_DF['PUZZLE']:
    for trigram in trigrams:
        if trigram in elem:
            trigram_counter[trigram] += 1
```

There are trigrams with a count of zero


```python
# Empty list to hold bigram with frequency of zero
zero_freq_list = []

# Searches for bigrams with frequency of zero
for trigram in trigrams:
    if trigram_counter[trigram] == 0:
        zero_freq_list.append(trigram)

# Prints list
#print(zero_freq_list)
```

We'll remove these so we can visualize our frequency distribution better


```python
for item in zero_freq_list:
    del trigram_counter[item]
```

Now we'll table the counts and visualize the results. Click the image to get a larger view.


```python
# Creating a dataframe called bigram_dist
symbols_ = np.array(list(trigram_counter.keys()))
frequencies_ = np.array(list(trigram_counter.values()))
trigram_dist = pd.DataFrame.from_dict({'Symbol': symbols_,'Frequency': frequencies_})

# Sorts dataframe before plotting
trigram_dist = trigram_dist.sort_values(by= ['Frequency'], ascending= False)
```


```python
# Created ranges for plots
ranges = []
for n in range(0, trigram_dist['Frequency'].size, 550):
    if n == 3300:
        ranges.append(n)
        ranges.append(trigram_dist['Frequency'].size)
    else:
        ranges.append(n)

# Plots the on subplots, increments of 550 entries
fig = plt.figure(figsize= (100, 400))
for i in range(len(holder) - 1):
    plt.subplot(7, 1, i+1)
    start, stop = ranges[i], ranges[i + 1]
    trigram_chart = sns.barplot(trigram_dist['Symbol'].iloc[start:stop], 
                                trigram_dist['Frequency'].iloc[start:stop]/frequencies_.sum())
    plt.ylim(0.000,0.010)
    trigram_chart.set_xticklabels(trigram_chart.get_xticklabels(), 
                                  rotation=45, 
                                  horizontalalignment='right',
                                  fontweight='light',
                                  fontsize='8');
```


![png](output_79_0.png)


The following line provides the first 20 entries of our sorted dataframe; In other words we have the top 20 most frequent bigrams printed. You can modify this line to view any section of the table (in case it's difficult to make out the axes). 


```python
trigram_dist.iloc[:20]
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
      <th>1680</th>
      <td>ING</td>
      <td>269</td>
    </tr>
    <tr>
      <th>2269</th>
      <td>NG</td>
      <td>224</td>
    </tr>
    <tr>
      <th>3213</th>
      <td>THE</td>
      <td>148</td>
    </tr>
    <tr>
      <th>1456</th>
      <td>HE</td>
      <td>137</td>
    </tr>
    <tr>
      <th>112</th>
      <td>OF</td>
      <td>135</td>
    </tr>
    <tr>
      <th>155</th>
      <td>TH</td>
      <td>123</td>
    </tr>
    <tr>
      <th>1636</th>
      <td>IGH</td>
      <td>116</td>
    </tr>
    <tr>
      <th>2438</th>
      <td>OF</td>
      <td>111</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>94</td>
    </tr>
    <tr>
      <th>381</th>
      <td>AND</td>
      <td>86</td>
    </tr>
    <tr>
      <th>1345</th>
      <td>GHT</td>
      <td>81</td>
    </tr>
    <tr>
      <th>284</th>
      <td>ACK</td>
      <td>80</td>
    </tr>
    <tr>
      <th>2237</th>
      <td>ND</td>
      <td>79</td>
    </tr>
    <tr>
      <th>3745</th>
      <td>YOU</td>
      <td>79</td>
    </tr>
    <tr>
      <th>23</th>
      <td>BO</td>
      <td>74</td>
    </tr>
    <tr>
      <th>3621</th>
      <td>WOR</td>
      <td>73</td>
    </tr>
    <tr>
      <th>2602</th>
      <td>OUT</td>
      <td>72</td>
    </tr>
    <tr>
      <th>2600</th>
      <td>OUR</td>
      <td>72</td>
    </tr>
    <tr>
      <th>56</th>
      <td>FO</td>
      <td>66</td>
    </tr>
    <tr>
      <th>2604</th>
      <td>OVE</td>
      <td>66</td>
    </tr>
  </tbody>
</table>
</div>



We also have the `Symbol` column printed so we can identify when a sequence begins/ends with a space (also in case it's difficult to make out the axes). 


```python
trigram_dist['Symbol'].iloc[:20]
```




    1680    ING
    2269    NG 
    3213    THE
    1456    HE 
    112      OF
    155      TH
    1636    IGH
    2438    OF 
    1        A 
    381     AND
    1345    GHT
    284     ACK
    2237    ND 
    3745    YOU
    23       BO
    3621    WOR
    2602    OUT
    2600    OUR
    56       FO
    2604    OVE
    Name: Symbol, dtype: object



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


We'll print the first 20 entries of our sorted dataframe to see the most frequent words in out data.


```python
first_order_dist.iloc[:20]
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
      <th>1</th>
      <td>A</td>
      <td>196</td>
    </tr>
    <tr>
      <th>2284</th>
      <td>THE</td>
      <td>138</td>
    </tr>
    <tr>
      <th>1671</th>
      <td>OF</td>
      <td>106</td>
    </tr>
    <tr>
      <th>61</th>
      <td>AND</td>
      <td>54</td>
    </tr>
    <tr>
      <th>1328</th>
      <td>IT</td>
      <td>47</td>
    </tr>
    <tr>
      <th>1309</th>
      <td>IN</td>
      <td>45</td>
    </tr>
    <tr>
      <th>2374</th>
      <td>UP</td>
      <td>39</td>
    </tr>
    <tr>
      <th>1717</th>
      <td>OUT</td>
      <td>34</td>
    </tr>
    <tr>
      <th>1290</th>
      <td>I</td>
      <td>33</td>
    </tr>
    <tr>
      <th>2649</th>
      <td>YOUR</td>
      <td>30</td>
    </tr>
    <tr>
      <th>1688</th>
      <td>ON</td>
      <td>26</td>
    </tr>
    <tr>
      <th>2311</th>
      <td>TO</td>
      <td>26</td>
    </tr>
    <tr>
      <th>1023</th>
      <td>GOOD</td>
      <td>23</td>
    </tr>
    <tr>
      <th>1181</th>
      <td>HIGH</td>
      <td>23</td>
    </tr>
    <tr>
      <th>896</th>
      <td>FOR</td>
      <td>22</td>
    </tr>
    <tr>
      <th>2645</th>
      <td>YOU</td>
      <td>22</td>
    </tr>
    <tr>
      <th>1247</th>
      <td>HOT</td>
      <td>22</td>
    </tr>
    <tr>
      <th>127</th>
      <td>BACK</td>
      <td>21</td>
    </tr>
    <tr>
      <th>2513</th>
      <td>WAY</td>
      <td>21</td>
    </tr>
    <tr>
      <th>1291</th>
      <td>I'M</td>
      <td>21</td>
    </tr>
  </tbody>
</table>
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
    [nltk_data]   Unzipping taggers/averaged_perceptron_tagger.zip.


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


