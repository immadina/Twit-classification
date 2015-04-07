import sys, re


#features = {"First person": 0, "Second person": 0, "Third person": 0, "Coordinating conjunctions": 0, "Past-tense verbs": 0, "Future-tense verbs": 0, "Commas": 0, "Colons and semi-colons": 0, "Dashes": 0, "Parentheses": 0, "Ellipses": 0, "Common nouns": 0, "Proper nouns": 0, "Adverbs": 0, "wh-words": 0, "Modern slang": 0, "All upper case": 0, "Avg sentence length": 0, "Avg token length": 0, "Number of sentences": 0, "twit": ""}


attributes = ["First_person", "Second_person", "Third_person", "Coordinating_conjunctions", "Past-tense_verbs", "Future-tense_verbs", "Commas", "Colons_and_semi-colons", "Dashes", "Parentheses", "Ellipses", "Common_nouns", "Proper_nouns", "Adverbs", "wh-words", "Modern_slang", "All_upper_case", "Avg_sentence_length", "Avg_token_length", "Number_of_sentences", "twit"]

def get_tweets(filename):
    f = open(filename, "r")
    tweets = f.read()
    tweets = tweets.split("|\n")
    tweets.pop(0)
    tweets.pop()
    
    for tweet in tweets:
        tweet = tweet.split("\n")
    return tweets  
    
    
def uppercase_words(tweet):
    '''
    Number of words with all upper-case letters.
    '''
    
    count = 0
    
    words = tweet.split()
    #print words
    for word in words:
        #word = tweet[i]
        word = word.partition("/")[0]
        if len(word) > 1 and word.isupper():
            count += 1
            #print word
    return count
            
        
def avg_sent_len(tweet):
    '''
    Average length of sentence.
    '''
    sentences = tweet.split("\n")
    words = []
    for i in sentences:
        words += i.split()
    #print words
    #print sentences
    if len(words) != 0:
        return float(len(words)) / len(sentences)
    else: return 0


def avg_token_len(tweet):
    '''
    Average length of tokens.
    '''
    sentences = tweet.split("\n")
    words = []
    for i in sentences:
        words += i.split()
    s = 0
    for i in words:
        w = i.partition("/")
        if not w[0] in '#$..,;:()"<':
            s += len(w[0]) #the word itself
    if len(words) != 0:
        return float(s) / len(words)
    else: return 0


def count_words(tweet, lst):
    '''
    Count the number of occurences of words from lst in tweet.
    '''
    
    count = 0
    words = tweet.split()
    for word in words:
        word = word.partition("/")[0]
        if word.lower() in lst:
            count += 1
    return count  


def count_tags(tweet, lst):
    '''
    Count the number of occurences of tags from lst in tweet.
    '''
    
    count = 0
    words = tweet.split()
    for word in words:
        word = word.partition("/")[0]
        tag = word.partition("/")[2]
        if lst == [":"]:
            if (word.endswith("..") and tag in lst):
                count += 1
        elif tag in lst:
            count += 1
    return count


def build_vect(tweets, classname):
    '''
    Return list of features for each given tweet.
    '''
    tweets_features = []
    features = {}
    for tweet in tweets:
    
        features["First_person"] = count_words(tweet, first_pro)
        features["Second_person"] = count_words(tweet, second_pro)
        features["Third_person"] = count_words(tweet, third_pro)
        features["Coordinating_conjunctions"] = count_tags(tweet, ["CC"])
        features["Past-tense_verbs"] = count_tags(tweet, ["VBD", "VBN"])
        features["Future-tense_verbs"] = count_words(tweet, future_tense)
        features["Commas"] = count_tags(tweet, [","])
        features["Colons_and_semi-colons"] = count_words(tweet, ["-"])
        features["Dashes"] = count_words(tweet, [";", ":"])
        features["Parentheses"] = count_words(tweet, ["(", ")"])
        features["Ellipses"] = count_tags(tweet, [":"])
        features["Common_nouns"] = count_tags(tweet, common_nouns)
        features["Proper_nouns"] = count_tags(tweet, prop_nouns)
        features["Adverbs"] = count_tags(tweet, adv)
        features["wh-words"] = count_tags(tweet, wh_words)
        features["Modern_slang"] = count_words(tweet, slang)
        features["All_upper_case"] = uppercase_words(tweet)
        features["Avg_sentence_length"] = "%.2f" % avg_sent_len(tweet)
        features["Avg_token_length"] = "%.2f" % avg_token_len(tweet)
        features["Number_of_sentences"] = len(tweet.split("\n"))
        features["twit"] = classname
            
        tweets_features.append(features)
        features = {}    
    return tweets_features


def build_arff(output_fname, tweets_features, twit_attr):
    '''
    Builds an ARFF formated file.
    '''
    
    arff_file = open(output_fname, "w")
    arff_file.write("@relation twit_classification\n")
    arff_file.write("\n")
    for attr in attributes:
        if attr != "twit":
            arff_file.write("@attribute " + attr + " numeric\n")
    
    
    arff_file.write("@attribute twit" + twit_attr + "\n") #twits - set of persons    
    arff_file.write("\n")
    arff_file.write("@data")
   
    
    for ftrs in tweets_features:
        #print ftrs
        arff_file.write("\n")
        for attr in attributes:
            if attr != "twit": 
                arff_file.write(str(ftrs[attr]) + ",")
        #print attr
        arff_file.write(ftrs["twit"])
    
    
    arff_file.close() 
    
    
if __name__ == "__main__":
    tweets_features = []
    
    #definitions of feature categories
    first_pro = ["i", "me", "me", "mine", "we", "us", "our", "ours"]
    second_pro = ["you", "your", "yours", "u", "ur", "urs"]
    third_pro = ["he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs"]
    future_tense = ["'ll", "will", "gonna"]
    common_nouns = ["NN", "NNS"]
    prop_nouns = ["NNP, NNPS"]
    adv = ["RB", "RBR", "RBS"]
    wh_words = ["WDT", "WP", "WP$", "WRB"]
    slang = ["smh", "fwb", "lmfao", "lmao", "lms", "tbh", "rofl", "wtf", "bff",
             "wyd", "lylc", "brb", "atm", "imao", "sml", "btw", "bw", "imho",
             "fyi", "ppl", "sob", "ttyl", "imo", "ltr", "thx", "kk", "omg",
             "ttys", "afn", "bbs", "cya", "ez", "f2f", "gtr", "ic", "jk", 
             "k", "ly", "ya", "nm", "np", "plz", "ru", "so", "tc", "tmi",
             "ym", "ur", "u", "sol"]    
    
    
    
    
    #process args
    args = sys.argv
    twits = [] #twit classes
    tweet_num = 0
    
    if (args[1].startswith("-")):
        tweet_num = int(args[1][1:])
        twits += args[2:-1]
    else:
        twits += args[1:-1]
    
    
    
    #from args identify the class name and .twt files
    classname = ""
    d = {}
    for i in twits:
        if(":" in i and "+" in i):
            classname = i.partition(":")[0]
            i = i.partition(":")[2]
            d[classname] = i.split("+")
        if(":" in i and "+" not in i):
            classname = i.partition(":")[0]
            i = i.partition(":")[2]
            d[classname] = [i]            
        if (classname == "" and "+" in i):
            lst = i.split("+")
            classname = "".join([x.strip(".twt") for x in lst])        
            d[classname] = lst            
        if (classname == "" and "+" not in i):
            classname = i.strip(".twt")
            d[classname] = [i]
        classname = ""

    
    #d is dictionary {classname: files}
    tweets = []
    
    for (k, v) in d.items():
        #print k, v
        all_files = []
        for file in v:
            f = open(file, "r")
            f = f.read()
            f = f.split("|\n")
            f.pop(0)
            f.pop()            
            if tweet_num != 0:
                all_files += f[:tweet_num]
        tweets_features += build_vect(all_files, k)
    
    twit_attr = "{" + ",".join(d.keys()) + "}"
    

    output_fname = args[-1]
    build_arff(output_fname, tweets_features, twit_attr);
    print "\nDone."