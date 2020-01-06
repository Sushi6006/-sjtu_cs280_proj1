import os
import re
import string
from math import log
from datetime import datetime
from bs4 import BeautifulSoup

# for word processing
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
# comment out these two lines if already downloaded
# nltk.download('punkt')
# nltk.download('stopwords')

# for calculation
from collections import Counter

# numbers of words to be calculated
NUM_TO_CALC = 10

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
    files_read = []
    file_count = 0
    fail_count = 0
    content = ""  # stores all the text combined
    for f in files:
        with open(f, "r") as f:
            try:
                content += BeautifulSoup(f.read(), "lxml").text
                file_count += 1
                files_read.append(f.name)
            except UnicodeDecodeError:
                # print("UnicodeDecodeError: {}".format(f))
                fail_count += 1

    return (content, files_read, file_count, fail_count)


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


def output(no_string_identified, no_string_filtered, no_word, counter, file_count, fail_count, title):
    NUM_TO_SHOW = NUM_TO_CALC
    file_name = "_".join(title.lower().split()) + "_output.txt"
    with open(file_name, "w") as output_file:
        title = ("\n{0}\n"
                 "{4}{5:^20}{4}\n"
                 "FILES FOUND: {1};\n"
                 "READ SUCCESSFULLY: {2};   FAILED TO READ: {3};\n"
                 "{0}\n").format('='*50, fail_count + file_count, file_count, fail_count, '='*15, title.upper())
        data_info = ("Number of strings identified:       {}\n"
                     "Number of strings after filtration: {}\n"
                     "Number of individual words:         {}\n\n\n").format(no_string_identified, no_string_filtered, no_word)
        list_title = "      {0:20}   | {1:20}\n".format("MOST COMMON", "LEAST COMMON")
        output_txt = title + data_info + list_title

        num_listed = min(NUM_TO_SHOW, len(counter))
        for i in range(num_listed):
            word_1 = counter[i]
            word_2 = counter[-(num_listed-i)]
            output_txt += "{0:6}{1:15}{2:>5}   | {3:15}{4:>5}\n".format(str(i + 1) + ".", word_1[0], word_1[1], word_2[0], word_2[1])

        output_file.write(output_txt)


def tf_output(tf_train, tf_test):

    train_output_file = open("train_tf.txt", "w")
    test_output_file = open("test_tf.txt", "w")

    title = ("\n\n{0}\n"
             "{1:^50}\n{0}\n\n").format('='*50, "Term Frequency")
    table = "{0:>5}|".format("")
    for i in range(NUM_TO_CALC):
        table += "{0:>8}".format("word_" + str(i + 1))
    train_output = test_output = title + table + "\n"

    for i in range(len(tf_train)):
        train_output += "{0:<5}|".format("d" + str(i + 1))
        doc = tf_train[i]
        for f in doc:
            train_output += "{0:>8}".format(f'{f:.2f}')
        train_output += "\n"

    for i in range(len(tf_test)):
        test_output += "{0:<5}|".format("d" + str(i + 1))
        doc = tf_test[i]
        for f in doc:
            test_output += "{0:>8}".format(f'{f:.2f}')
        test_output += "\n"

    train_output_file.write(train_output)
    test_output_file.write(test_output)

    train_output_file.close()
    test_output_file.close()


def idf_output(idf_train, word_train, idf_test, word_test):
    output_file = open("idf.txt", "w")

    output = ("\n\n{0}\n{1:^50}\n{0}\n\n"
              "{2:>8}{2:>10}{3:>8}{2:>10}{4:>8}\n").format('='*50, "Inverse Document Frequency", "", "train", "test")

    for i in range(NUM_TO_CALC):
        output += ("{0:>8}{3:>10}{1:>8}{4:>10}{2:>8}\n").format("word_" + str(i + 1), f'{idf_train[i]:.2f}', f'{idf_test[i]:.2f}', word_train[i][0], word_test[i][0])

    output_file.write(output)
    output_file.close()


def test_output(info, msg):
    # {"str_identified", "str_filtered", "word_count", "sorted_freqs", "file_count", "fail_count"}
    print(f'{"="*10}{msg.upper():^12}{"="*10}')
    print("str_identified:", info["str_identified"])
    print("str_filtered:  ", info["str_filtered"])
    print("word_count:    ", info["word_count"])
    print("file_count:    ", info["file_count"])
    print("fail_count:    ", info["fail_count"])
    print(f'{"="*32}')


# project 1 main, calculate frequency related stuff
def calc_main(file_dir, is_file=False):

    # file_dir = os.getcwd()

    # read files
    if not is_file:
        content, files_read, file_count, fail_count = read_file(file_dir)
    else:
        with open(file_dir, "r") as f:
            content = BeautifulSoup(f.read(), "lxml").text
        files_read = [file_dir]
        file_count = 1
        fail_count = 0

    tokens = [word.lower() for word in word_tokenize(content)]  # tokenize
    no_string_identified = len(tokens)

    # filter tokens (stopwords, numbers etc.)
    tokens = filter_words(tokens)
    no_string_filtered = len(tokens)

    # stemming
    ps = PorterStemmer()
    tokens = [ps.stem(word) for word in tokens]

    c = dict(Counter(tokens))
    sorted_freqs = sorted(c.items(), key=lambda a: (-a[1], a[0]))
    no_word = len(c.keys())

    result = {"str_identified": no_string_identified,
              "str_filtered": no_string_filtered,
              "word_count": no_word,
              "sorted_freqs": sorted_freqs,
              "file_count": file_count,
              "fail_count": fail_count,
              "files_read": files_read}

    return result


def calc_tf(word, freqs):

    for w, f in freqs:
        if w == word:
            return f / freqs[0][1]
    return 0


#====================================#
#========== STARTS HERE!!! ==========#
#====================================#
def main():

    begin_time = datetime.now().replace(microsecond=0)

    # get results from files
    train_result = calc_main("projectdataset/train")
    test_result = calc_main("projectdataset/test")
    output(train_result["str_identified"], train_result["str_filtered"], train_result["word_count"],
           train_result["sorted_freqs"], train_result["file_count"], train_result["fail_count"], "TRAINING SET")
    output(test_result["str_identified"], test_result["str_filtered"], test_result["word_count"],
           test_result["sorted_freqs"], test_result["file_count"], test_result["fail_count"], "TESTING SET")

    test_output(train_result, "train set")
    test_output(test_result, "test set")

    time_at_mark1 = datetime.now().replace(microsecond=0)
    print("===== TIME USED SO FAR: {}\n".format(time_at_mark1 - begin_time))

    # read the following print statement :)
    print("===== Calculating TF...")
    tf_train = [[0 for j in range(NUM_TO_CALC)] for i in range(train_result["file_count"])]
    tf_test = [[0 for j in range(NUM_TO_CALC)] for i in range(test_result["file_count"])]
    train_fileset = train_result["files_read"]
    test_fileset = test_result["files_read"]
    for i in range(NUM_TO_CALC):
        curr_time = datetime.now().replace(microsecond=0)
        print("===== WORD no.{0:0>4d} ===== TIME USED: {1:<8} =====".format(i, str(curr_time - begin_time)))
        train_word = train_result["sorted_freqs"][i][0]
        test_word = train_result["sorted_freqs"][i][0]
        for j in range(train_result["file_count"]):
            result = calc_main(train_fileset[j], is_file=True)
            tf_train[j][i] = calc_tf(train_word, result["sorted_freqs"])
        for j in range(test_result["file_count"]):
            result = calc_main(test_fileset[j], is_file=True)
            tf_test[j][i] = calc_tf(test_word, result["sorted_freqs"])

    # read the following print statement !!!
    print("===== Calculating IDF...")
    idf_train = [0 for i in range(NUM_TO_CALC)]
    idf_test = [0 for i in range(NUM_TO_CALC)]
    for i in range(NUM_TO_CALC):
        curr_time = datetime.now().replace(microsecond=0)
        print("===== WORD no.{0:0>4d} ===== TIME USED: {1:<8} =====".format(i, str(curr_time - begin_time)))
        train_word = train_result["sorted_freqs"][i][0]
        test_word = test_result["sorted_freqs"][i][0]
        train_count = 0
        test_count = 0
        for j in range(train_result["file_count"]):
            with open(train_fileset[j], "r") as f:
                if train_word in f.read():
                    train_count += 1
        for j in range(test_result["file_count"]):
            with open(test_fileset[j], "r") as f:
                if test_word in f.read():
                    test_count += 1
        idf_train[i] = 0 if (train_count == 0) else log(train_result["file_count"] / train_count, 2)
        idf_test[i] = 0 if (test_count == 0) else log(test_result["file_count"] / test_count, 2)

    tf_output(tf_train, tf_test)
    idf_output(idf_train, train_result["sorted_freqs"], idf_test, test_result["sorted_freqs"])


if __name__ == "__main__":
    main()
