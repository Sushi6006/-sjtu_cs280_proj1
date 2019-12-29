import os
import re
import string
from bs4 import BeautifulSoup

# for word processing
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# comment out these three lines if already downloaded
# nltk.download('punkt')
# nltk.download('stopwords')

# for calculation
from collections import Counter

# read all the files to a string
def read_file(path):
    # get all the files (with full path)
    files = []
    for root, _, files_in_dir in os.walk(path):
        for file in files_in_dir:
            # use "http" to filter files instead of ".html" bc some file
            # does not come with the suffix html, but is readable after change
            # the file type to .html
            if "http" in file:
                files.append(os.path.join(root, file))

    # loop through the files
    file_count = 0
    fail_count = 0
    content = ""  # stores all the text combined
    for f in files:
        with open(f, "r") as f:
            file_count += 1
            try:
                content += BeautifulSoup(f.read(), "lxml").text
            except UnicodeDecodeError:
                # print("UnicodeDecodeError: {}".format(f))
                fail_count += 1

    return (content, file_count, fail_count)


# filter out all the words considered not valuable
def filter_words(tokens):
    str_to_remove = set(stopwords.words("english"))
    # add words/chars i found useless in the result
    custom_stopwords = {"else", "would", "much"}
    str_to_remove.update(custom_stopwords)
    # other_str = {".s", "g.", "e.", "k.", "a.", "'ve"}
    # str_to_remove.update(other_str)

    # contains only digits, in stopwords set, or contains only one char
    def is_valid(word):
        if word.isdigit() or (word in str_to_remove) or len(word) == 1:
            return False

        # remove all the strings with random symbols within them
        # but left out ones with "-", ".", "'", "_"
        # bc i think they may still be valuable
        for char in word:
            if char in string.punctuation or char.isdigit():
                return False
            # valid_puncs = ("-", ".", "'", "_")
            # if (char in string.punctuation and char not in valid_puncs):  # False if contains invalid puncs
            #     return False
            # if (char in valid_puncs) and (not re.search('[a-zA-Z0-9]', word)):  # contains only valid puncs
            #     return False

        return True

    return [word for word in tokens if is_valid(word)]


def output(counter, file_count, fail_count):
    NUM_TO_SHOW = 200
    with open("output.txt", "w") as output_file:
        title = "{0}\nFILES FOUND: {1};\nREAD SUCCESSFULLY: {2};   FAILED TO READ: {3};\n{0}\n\n".format('='*50, fail_count + file_count, file_count, fail_count)
        list_title = "    {0:20}   | {1:20}\n".format("MOST COMMON", "LEAST COMMON")
        output_txt = title + list_title

        for i in range(NUM_TO_SHOW):
            word_1 = counter[i]
            word_2 = counter[-(NUM_TO_SHOW-i)]
            output_txt += "{0:4}{1:15}{2:>5}   | {3:15}{4:>5}\n".format(str(i + 1) + ".", word_1[0], word_1[1], word_2[0], word_2[1])

        output_file.write(output_txt)



#====================================#
#========== STARTS HERE!!! ==========#
#====================================#
def main():
    # read files
    content, file_count, fail_count = read_file(os.getcwd())
    tokens = [word.lower() for word in word_tokenize(content)]  # tokenize

    # filter tokens (stopwords, numbers etc.)
    tokens = filter_words(tokens)

    # stemming
    ps = PorterStemmer()
    tokens = [ps.stem(word) for word in tokens]

    c = dict(Counter(tokens))
    sorted_counter = sorted(c.items(), key=lambda a: (-a[1], a[0]))

    output(sorted_counter, file_count, fail_count)


if __name__ == "__main__":
    main()
