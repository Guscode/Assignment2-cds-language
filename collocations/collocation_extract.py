'''
Use the function get_collocations to extract how many times
words occur together in a corpus, both in raw frequency, and
In terms of a mutual information score. 

The function takes the following arguments:
Texts: Your corpus in the format of a list of strings.
Word: the target word, for which you wish to find collocations
Window: Defines how closely the target word and the collocation
        has to interact. e.g. a window=5 will search for collocations
        words before and after the target word.

The function returns a pandas dataframe with the columns:
raw_freq: How many times the target word and collocation 
          occured together.
MI: Mutual information score based on calculations from
    http://www.collocations.de/AM/section1.html
            
'''

#Importing packages
import re
import string
import pandas as pd
import math
import os


def get_collocations(texts, word = "", window = 1000): 
    all_collocations = pd.DataFrame(columns=["raw_freq", "MI", "Col"]) #Making empty dataframe to store results

    clean_text = [re.sub(r"\W+", " ", txt) for txt in txts] #Cleaning the texts so they only include letters and spaces
    
    all_words=[] #Creating empty list for all words present in the corpus

    for txt in clean_txt:
        all_words= all_words+txt.split() #Loop through each text and extract all the words
        
    all_words = list(set(all_words)) #Select unique words by making the list into a set, and back
    all_words.remove(word) #Remove the target word from the list
    
    
    for col in all_words: #Loop through all words in the corpus
        res_dict = {'wordcol':0, 'no_wordcol':0, 'no_wordno_col':0, 'wordno_col':0} #Make empty dictionary to store results
                                                                                    
        MI=0 #Set MI score to 0
        
        for text in texts: #Loop through each text in the corpus 
            word_indicator = "no_word" #Create indicator of whether the target word is present
            collocate_indicator ="no_col" #Create indicator of whether the collocate is present
            split_text = text.split() #Split the text
            if word in split_text: #If the target word is in the text do the following
                    word_indicator = "word" #Change target word_indicator from 'no_word' to 'word'
                    start = max(0,split_text.index(word)-window) #Make start variable to indicate the start of the window
                    end = split_text.index(word)+window #Make end variable to indicate the end of the window
                    shortened_text = split_text[start:end] #Make the window
                    if col in shortened_text: #If the collocate is in the window
                        collocate_indicator = "col" #Change collocate_indicator from 'no_col' to 'col'
                        
            if text.find(col)!= -1 & word_indicator=="no_word": #If collocate is in the text and target word isn't do this 
                collocate_indicator = "col" #Change collocate_indicator from 'no_col' to 'col'

            res_dict[word_indicator+collocate_indicator] += 1 #Change value in res_dict (all texts will have a word_indicator
                                                              #of either 'word' or 'no_word' and a collocate_indicator of either
                                                              #'col' or 'no_col'. When they are pasted together, they represent 
                                                              #the four categories in the res_dict 
        
        R1 = res_dict["wordcol"]+res_dict["wordno_col"] #Calculate R1-score
        C1 = res_dict["no_wordcol"]+res_dict["wordcol"] #Calculate C1-score
        C2 = res_dict["wordno_col"]+res_dict["no_wordno_col"] #Calculate C2-score
        E11 = (R1*C1)/(C1+C2) #Calculate E11-score
    
        if E11 > 0: #if statements to avoid dividing by zero
            if res_dict["wordcol"]>0:
                MI = math.log((res_dict["wordcol"]/E11)) #Calculate MI-score

        raw_freq = res_dict["wordcol"] #Extract raw frequency (when word and collocate appear together)
        all_collocations_length = len(all_collocations) #Add info to dataframe
        all_collocations.loc[all_collocations_length] = [raw_freq, MI,col]
    
    return all_collocations #return dataframe

def main():
    print("Import the function get_collocations into your python script and use it to extract collocations from a corpus")
    
if __name__=="__main__":
    main()