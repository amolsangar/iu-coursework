# SeekTruth.py : Classify text objects into two categories
#
# Name - Amol Dattatray Sangar
# User ID - asangar
#
# Based on skeleton code by D. Crandall, October 2021

# Reference - https://www.kdnuggets.com/2020/07/spam-filter-python-naive-bayes-scratch.html

import sys
import re
import pandas as pd
import math

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!

def cleanData(l):
    temp_res = []
    stopwords = ['would','will','just','wasn','what','been','ll','could','that','but','ed','hadn','isn','didn','some','however','there','need','therefore','where','all','had','while','were','did','have','are','so','much','very','at','the','my','in','with','for','and','am','an','to','on','as','it','has','is','can','was','which','when','they','by','from','this','since','be','if','or','of']
    for w in l:
        if(len(w) > 1 and w.lower() not in stopwords and not w.isnumeric()):
            temp_res.append(w.lower())
    return temp_res

def classifier(train_data, test_data):
    deceptive_train_data = [train_data["objects"][i] for i in range(0,len(train_data["objects"])) if(train_data["labels"][i] == "deceptive")]
    deceptive_data_2D_arr = [re.split('\W+', review) for review in deceptive_train_data]
    deceptive_data_2D_arr = [cleanData(i) for i in deceptive_data_2D_arr]
    
    truthful_train_data = [train_data["objects"][i] for i in range(0,len(train_data["objects"])) if(train_data["labels"][i] == "truthful")]
    truthful_data_2D_arr = [re.split('\W+', review) for review in truthful_train_data]
    truthful_data_2D_arr = [cleanData(i) for i in truthful_data_2D_arr]

    deceptive_1D_corpus = [j for sub in deceptive_data_2D_arr for j in sub]
    truthful_1D_corpus = [j for sub in truthful_data_2D_arr for j in sub]
    
    n_deceptive = len(deceptive_1D_corpus)
    n_truthful = len(truthful_1D_corpus)

    vocabulary = deceptive_1D_corpus + truthful_1D_corpus
    vocab_len = len(set(vocabulary))    # unique words count

    word_counts_per_decp_review = {unique_word: [0] * len(deceptive_data_2D_arr) for unique_word in vocabulary}
    for index, review in enumerate(deceptive_data_2D_arr):
        for word in review:
            word_counts_per_decp_review[word][index] += 1
    
    word_counts_per_trth_review = {unique_word: [0] * len(truthful_data_2D_arr) for unique_word in vocabulary}
    for index, review in enumerate(truthful_data_2D_arr):
        for word in review:
            word_counts_per_trth_review[word][index] += 1

    # Calculate Prior Probability
    prob_deceptive = len(deceptive_data_2D_arr) / (len(deceptive_data_2D_arr) + (len(truthful_data_2D_arr)))
    prob_truthful = len(truthful_data_2D_arr) / (len(deceptive_data_2D_arr) + (len(truthful_data_2D_arr)))

    # Calculate likelihood - words|truthful and words|deceptive
    parameters_deceptive = {unique_word:0 for unique_word in vocabulary}
    parameters_truthful = {unique_word:0 for unique_word in vocabulary}
    alpha = 1

    for word in vocabulary:
        word_freq_in_deceptive = sum(word_counts_per_decp_review[word])
        prob_word_given_deceptive = (word_freq_in_deceptive + alpha) / (n_deceptive + (alpha * vocab_len))
        parameters_deceptive[word] = prob_word_given_deceptive
        
        word_freq_in_truthful = sum(word_counts_per_trth_review[word])
        prob_word_given_truthful = (word_freq_in_truthful + alpha) / (n_truthful + (alpha * vocab_len))
        parameters_truthful[word] = prob_word_given_truthful

    # Test Data Classification 
    result = []
    for review in test_data["objects"]:
        temp_res = []
        review_arr = re.split('\W+', review)
        review_arr = cleanData(review_arr)

        # Formula: Naive Bayes afte applyting log function
        # prob_deceptive_given_word = log(P(deceptive)) + log(P(word1_given_deceptive) + log(P(word2_given_deceptive)) + ...

        prob_deceptive_given_word = math.log(prob_deceptive)
        prob_truthful_given_word = math.log(prob_truthful)
        
        for word in review_arr:
            if word in parameters_deceptive:
                prob_deceptive_given_word += (math.log(parameters_deceptive[word]))
            
            if word in parameters_truthful:
                prob_truthful_given_word += (math.log(parameters_truthful[word]))
                    
        if(prob_deceptive_given_word > prob_truthful_given_word):
            result.append("deceptive")
        else:
            result.append("truthful")
        
    return result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
