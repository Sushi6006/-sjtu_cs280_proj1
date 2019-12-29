# SJTU CS280 Project 1
##### Group No. 05
##### Leyan Lin, Fei Peng, Qina Wu, Zexu Huang, Yiyun Xiao, Xubin Zou

### Libraries Used
- [os](https://docs.python.org/3/library/os.html)
- [re](https://docs.python.org/3/library/re.html)
- [string](https://docs.python.org/3/library/string.html)
- [Beautiful Soup 4 (bs4)](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [Natural Language Toolkit (nltk)](https://www.nltk.org/)

### Code Explained
- [Reading Files](#reading-files)
- [Convert to processable types (tokenisation)](#tokenisation)
- [Filter (remove numbers, punctuations and stop words)](#filtering-words)
- Stemming
- Count frequency
- Output

#### Reading Files
Steps:
1. Set working directory to current working directory `os.getcwd()`
2. Walk through all the files in the directory and store ones with "http" in their names in a list
3. Loop through the list, open up each file
4. Use BeautifulSoup to get rid of all the tags, and add all the content/text to a string. `BeautifulSoup(f.read(), "lxml").text`, where f is the file currently being read
5. return all the text read, number of files successfully read and failed to read (due to utf-8 error `UnicodeDecodeError`)

#### Tokenisation
Convert string into list of words. That's it.

#### Filtering Words
The filtering rules have been changed many times in order to increase the quality of our result. At first, all the words with punctuations (`string.punctuation`) are removed. However, there are strings with "-", "'", "\_" or "." that might still be helpful. Then the rule was justified so that these characters have been excluded from all other punctuation. All the strings with alphabetical characters that contains those special characters would be kept. It has then be found out that there are a lot of strings like "'ve", "a.", "s." left in the list. All the strings like those have been added to the filter. Lastly, after completing the next step, we realised that all the "least common" words are actually random numbers such as 1.0, 29 and dates like 1985-Dec-05. Therefore, all the words that contain punctuations or numbers are completely removed.
