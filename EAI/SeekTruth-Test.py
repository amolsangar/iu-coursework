# SeekTruth.py : Classify text objects into two categories
#
# Name - Amol Dattatray Sangar
# User ID - asangar
#
# Based on skeleton code by D. Crandall, October 2021

import sys

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

def classifier(train_data, test_data):
    # print(train_data["labels"][599], train_data["objects"][599], train_data["classes"])

    deceptive_train_data = [train_data["objects"][i] for i in range(0,len(train_data["objects"])) if(train_data["labels"][i] == "deceptive")]
    truthful_train_data = [train_data["objects"][i] for i in range(0,len(train_data["objects"])) if(train_data["labels"][i] == "truthful")]

    vocab_words_spam = []

    for sentence in deceptive_train_data:
        sentence_as_list = sentence.split()
        for word in sentence_as_list:
            vocab_words_spam.append(word)     
            
    # print(vocab_words_spam)

    vocab_unique_words_spam = list(dict.fromkeys(vocab_words_spam))
    #print(vocab_unique_words_spam)

    dict_spamicity = {}
    for w in vocab_unique_words_spam:
        emails_with_w = 0     # counter
        for sentence in deceptive_train_data:
            if w in sentence:
                emails_with_w+=1
                
        # print(f"Number of spam emails with the word {w}: {emails_with_w}")
        total_spam = len(deceptive_train_data)
        spamicity = (emails_with_w+1)/(total_spam+2)
        # print(f"Spamicity of the word '{w}': {spamicity} \n")
        dict_spamicity[w.lower()] = spamicity

    # ========================================
    vocab_words_ham = []

    for sentence in truthful_train_data:
        sentence_as_list = sentence.split()
        for word in sentence_as_list:
            vocab_words_ham.append(word)
    
    vocab_unique_words_ham = list(dict.fromkeys(vocab_words_ham))
    # print(vocab_unique_words_ham)

    dict_hamicity = {}
    for w in vocab_unique_words_ham:
        emails_with_w = 0     # counter
        for sentence in truthful_train_data:
            if w in sentence:
                # print(w+":", sentence)
                emails_with_w+=1
                
        # print(f"Number of ham emails with the word '{w}': {emails_with_w}")
        total_ham = len(truthful_train_data)
        Hamicity = (emails_with_w+1)/(total_ham+2)       # Smoothing applied
        # print(f"Hamicity of the word '{w}': {Hamicity} ")
        dict_hamicity[w.lower()] = Hamicity
    


    prob_spam = len(deceptive_train_data) / (len(deceptive_train_data)+(len(truthful_train_data)))
    prob_ham = len(truthful_train_data) / (len(deceptive_train_data)+(len(truthful_train_data)))
    print(prob_spam,prob_ham)


    distinct_words_as_sentences_test = []

    for sentence in test_data["objects"]:
        sentence_as_list = sentence.split()
        senten = []
        for word in sentence_as_list:
            senten.append(word)
        # print(senten)
        distinct_words_as_sentences_test.append(senten)
            
    # print(distinct_words_as_sentences_test[0])

    reduced_sentences_test = []
    for sentence in distinct_words_as_sentences_test:
        words_ = []
        for word in sentence:
            if word in vocab_unique_words_spam:
                # print(f"'{word}', ok")
                words_.append(word)
            elif word in vocab_unique_words_ham:
                # print(f"'{word}', ok")
                words_.append(word)
            else:
                pass
                # print(f"'{word}', word not present in labelled spam training data")
        reduced_sentences_test.append(words_)
    # print(reduced_sentences_test)

    test_stemmed = []
    stopwords = ["","a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"]
    for email in reduced_sentences_test:
        email_stemmed=[]
        for word in email:
            if word in stopwords:
                pass
                # print('remove')
            else:
                email_stemmed.append(word)
        test_stemmed.append(email_stemmed)
                
    # print(test_stemmed)



    def mult(list_) :        # function to multiply all word probs together 
        total_prob = 1
        for i in list_: 
            total_prob = total_prob * i  
        return total_prob

    def Bayes(email):
        probs = []
        for word in email:
            Pr_S = prob_spam
            sum_PR_S = []
            # print('prob of spam in general ',Pr_S)
            try:
                pr_WS = dict_spamicity[word]
                # print(f'prob "{word}"  is a spam word : {pr_WS}')
            except KeyError:
                pr_WS = 1/(total_spam+2)  # Apply smoothing for word not seen in spam training data, but seen in ham training 
                # print(f"prob '{word}' is a spam word: {pr_WS}")
            sum_PR_S.append(pr_WS)
        prob_word_is_spam_BAYES = sum(sum_PR_S)
        prob_S_g_w = Pr_S * prob_word_is_spam_BAYES

        for word in email: 
            Pr_H = prob_ham
            sum_PR_H = []
            # print('prob of ham in general ', Pr_H)
            try:
                pr_WH = dict_hamicity[word]
                # print(f'prob "{word}" is a ham word: ',pr_WH)
            except KeyError:
                pr_WH = (1/(total_ham+2))  # Apply smoothing for word not seen in ham training data, but seen in spam training
                # print(f"WH for {word} is {pr_WH}")
                # print(f"prob '{word}' is a ham word: {pr_WH}")
            sum_PR_H.append(pr_WH)
        prob_word_is_ham_BAYES = sum(sum_PR_H)
        prob_H_g_w = Pr_H * prob_word_is_ham_BAYES

        print(prob_S_g_w, prob_H_g_w)
        # prob_word_is_spam_BAYES = (pr_WS*Pr_S)/((pr_WS*Pr_S)+(pr_WH*Pr_H))
        print('')
        # print(f"Using Bayes, prob of the word '{word}' is spam: {prob_word_is_spam_BAYES}")
        print('###########################')
        # probs.append(prob_word_is_spam_BAYES)
        # print(f"All word probabilities for this sentence: {probs}")
        # final_classification = mult(probs)
        # if final_classification >= 0.5:
        #     print(f'email is SPAM: with spammy confidence of {final_classification*100}%')
        # else:
        #     # pass
        #     print(f'email is HAM: with spammy confidence of {final_classification*100}%')
        return prob_S_g_w > prob_H_g_w
    
    result_test_data = []
    for email in test_stemmed:
        print('')
        # print(f"           Testing stemmed SPAM email {email} :")
        # print('                 Test word by word: ')
        all_word_probs = Bayes(email)
        if(all_word_probs == True):
            result_test_data.append("deceptive")
        else:
            result_test_data.append("truthful")
        print(all_word_probs)
    
    print(result_test_data)
    print(len(result_test_data))
    return result_test_data
    # return [test_data["classes"][0]] * len(test_data["objects"])


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
