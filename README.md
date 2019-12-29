# SJTU CS280 Project 1
##### Group No. 05
##### Leyan Lin, Fei Peng, Qina Wu, Zexu Huang, Yiyun Xiao, Xubin Zou

#### Libraries Used
- [os](https://docs.python.org/3/library/os.html)
- [re](https://docs.python.org/3/library/re.html)
- [string](https://docs.python.org/3/library/string.html)
- [Beautiful Soup 4 (bs4)](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [Natural Language Toolkit (nltk)](https://www.nltk.org/)

#### Code Explained
- [Reading Files](#reading-files)
- Convert to processable types (tokenisation)
- Filter (remove numbers, punctuations and stop words)
- Stemming
- Count frequency
- Output

##### Reading Files
Steps:
1. Set working directory to current working directory `os.getcwd()`
2. Walk through all the files in the directory and store ones with "http" in their names in a list
3. Loop through the list, open up each file
4. Use BeautifulSoup to get rid of all the tags, and add all the content/text to a string. `BeautifulSoup(f.read(), "lxml").text`, where f is the file currently being read
5. return all the text read, number of files successfully read and failed to read (due to utf-8 error `UnicodeDecodeError`)
