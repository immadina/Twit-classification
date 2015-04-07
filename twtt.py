import sys, re
import NLPlib

CLITICS = ["'m", "'re", "'s", "n't", "'ll"]


def clean(line):
    '''
    Remove all html tags and attributes, URLs, user name(@) characters and 
    hash tags(#). Replace html character codes with an ASCII equivalent.
    
    '''
    
    # html tags and attributes
    mo1 = re.findall(r"<a.*?>|</a>", line)
    for i in mo1:
        if i:
            line = line.replace(i, "")         

    # URLs: REDO
    line = re.sub(r"(?:(H|h)ttps?://|ftp://|(W|w){3}\.)?\w+\.(?:\w{2,3})(?:\.\w{2,3})?(?:/\S*)*", '', line)    
      #print line
              
    # user names, hashtags
    mo2 = re.findall(r"#.*?|@.*?", line)
    for i in mo2:
        if i:
            line = line.replace(i, "")
    
    # html character codes
    # TODO: any other???
    line = re.sub(r"&amp;", '&', line)
    line = re.sub(r"&quot;", '"', line)
    line = re.sub(r"&lt;", '<', line)
    line = re.sub(r"&gt;", '>', line)
    
    return line   


def handle_mult_punctuation(line):
    '''
    Ellipsis and other kind of multiple punctuation
    '''
    regex = abbrev()
    #TODO: ??!!
    split_line = re.split("(\.[ \t]?\.(?:[ \t]*\.)*)|(![ \t]?!(?:[ \t]*!)*)|(\?[ \t]?\?(?:[ \t]*\?)*)", line)
    split_line = filter(None, split_line)
    split_line = [x.strip() for x in split_line]
    
    
    
    for i in range(len(split_line)):
        if re.match("(\.[ \t]?\.(?:[ \t]*\.)*)|(![ \t]?!(?:[ \t]*!)*)|(\?[ \t]?\?(?:[ \t]*\?)*)", split_line[i]):
            if (i + 1 < len(split_line) and split_line[i + 1] != ''):
                next_l = split_line[i + 1][0].strip()
                #Assumption: after multiple punctuation everything that doesn't start with a lowercase letter is considered to be a new sentence 
                if (not next_l.isalpha() or next_l.isupper()):
                    split_line[i] += "\n"
        else:
            #print split_line[i]
            split = re.split(r"(\?[ \t]?)|(\.[ \t]?)|(![ \t]?)|(,[ \t]?)|('ll[ \t]?)|('m[ \t]?)|('re[ \t]?)|('s[ \t]?)|(n't[ \t]?)", split_line[i])
            split = filter(None, split)
            split = [x.strip() for x in split]
            
            split_line[i] = split
            
            for j in range(len(split_line[i])):
                if re.match(r"(\?[ \t]?)|(\.[ \t]?)|(![ \t]?)", split_line[i][j]):
                    split_line[i][j] += "\n"
            split_line[i] = " ".join(split_line[i])                             
             
    #return (" ".join(split_line))
    split_line = " ".join(split_line)
    #print split_line.splitlines(True)
    return split_line.splitlines(True)


def abbrev():
    abbrev = open("abbrev.english", "r").read()
    abbrev = abbrev.split('\n')
    abbrev.pop()
    
    pn_abbrev = open("pn_abbrev.english", "r").read()
    pn_abbrev = pn_abbrev.split('\n')
    pn_abbrev.pop()
    
    
    regex = "(" + "|".join(abbrev) + ")"
    
    return regex
    



def split_sentences(input_fname, output_fname):
    '''
    
    '''
    tagger = NLPlib.NLPlib()
    input_f = open(input_fname, "r")
    output_f = open(output_fname, "w+")
    output_f.write("|\n")
    for line in input_f:
        
        line = clean(line)
        
        sentences = handle_mult_punctuation(line);
        #print sentences
        
        for i in range(len(sentences)):
            sent = sentences[i].split()
            tags = tagger.tag(sent)            
            
            for j in range(len(sent)):
                sent[j] += ("/" + tags[j])
        #print sentences
        
            sent_line = " ".join(sent) 
            
            output_f.write(sent_line)
            output_f.write("\n")
        #if line[len(line)-1:] != "\n":
        #   output_f.write("\n")
        output_f.write("|\n")
    input_f.close()
    output_f.close()
    


if __name__ == "__main__":
    
    args = sys.argv
    input_fname = args[1]
    output_fname = args[-1]
    
    split_sentences(input_fname, output_fname)
    print "\nDone."
    