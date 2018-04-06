'''
Implementation of Porter's Stemmer 
A text file is taken from Project Gutenberg. The file is converted into lowercase
and tokenize of that file is taken and Porter Stemmer is applied.
'''

import re
import nltk,sys
from collections import Counter
#from __future__import print_function
from nltk import word_tokenize
from nltk.corpus import stopwords

class Stemmer(object):
    '''
    Step 1: CVCV ... C
            CVCV ... V
            VCVC ... C       
            VCVC ... V
    Representing the above form into single form as [C]VCVC...[V]
    [] denotes arbitrary number of content
    V denotes One or more consecutive vowels
    C denotes One or more consecutive consonants
    [C]...VC(m)...[V] is the measure or count of the Vowels followed by Consonants m times
    NOTE: Y is considered a consonant if it's not preceded by a vowel.
    Step 1 deals with plurals and past participles
    '''
    vc_count = re.compile(r'[y]?[^aeiouy]*[aeiouy][aeiou]*[^aeiou]'
            '[^aeiouy]*').findall
    contains_v = re.compile(r'[aeiouy]').search
    double_c = re.compile(r'[^aeiou]{2,}$').search
#Check for Consonants Vowels Consonants ending
    end_cvc = re.compile(r'[^aeiou][aeiouy][^aeiouwxy]$').search

#To calculate and give value of VC 
    def m(self, word):
        return len(self.vc_count(word))

    def stem_m(self, suffix=''):
        if suffix:
            return self.m(self.rep_end(self.stemmed, suffix))
        return self.m(self.stemmed)


# (condition)S1 -> S2
#  Function for replacing the ending character of a word with rep, given that word 
#   ends with given suffixes as given in the document.
    def rep_end(self, word, suffix, rep=''):
        if word.endswith(suffix):
            return word[:len(word)- len(suffix)] + rep
        return word

#Function for Replacing rep with given suffix
    def replace_end(self, suffix, rep, condition = True):
# variable for checking whether the condition which is applicable for that word or not        
        applied = False
        if cond and self.stemmed.endswith(suffix):
            self.stemmed = self.rep_end(self.stemmed, suffix, rep)
            applied = True
        return applied

#Creating a Dictionary or Associative array for Step 2, 3 and 4.
#First character is the penultimate character which to be replaced by the following suffix
    step2_dict = {'a':(('ational','ate'),('tional','tion')),
               'c':(('enci', 'ence'), ('anci', 'ance')),
               'e':(('izer', 'ize')),
               'l':(('bli', 'ble'),('alli', 'al'),('entli', 'ent'),('eli', 'e'),('ousli', 'ous')),
               'o':(('ization', 'ize'),('ation', 'ate'),('ator', 'ate')),
               's':(('alism', 'al'),('iveness', 'ive'),('fulness', 'ful'),('ousness', 'ous')),
               't':(('aliti', 'al'),('iviti', 'ive'),('biliti', 'ble')),
               'g':(('logi', 'log'))
              }

    step3_dict = {'t':(('icate', 'ic'), ('iciti', 'ic')),
               'v' : (('ative', ''),),
               'z' : (('alize', 'al'),),
               'a' : (('ical', 'ic'),),
               'u' : (('ful', ''),),
               's' : (('ness', ''),)
              }

    step4_dict = {'a' : (('al', ''),),
                  'c' : (('ance', ''),('ence', ''),),
                  'e' :(('er', ''),),
                  'i' : (('ic', ''),),
                  'l' : (('able', ''),('ible', '')),
                  'n' : (('ant', ''),('ement', ''),('ment', ''),('ent', '')),
                  'o' : (('ou', ''),),
                  's' : (('ism', ''),),
                  't' : (('ate', ''),('iti', '')),
                  'u' : (('ous', ''),),
                  'v' : (('ive', ''),),
                  'z' : (('ize', ''),)
                }
    def __init__(self):
        self.original_word, self.stemmed='',''
        self.step1b_second_rule, self.step1b_third_rule = False, False

#This function to be used in step 4     
    def longest_match(self, word, tbl):
        longest_match('','')
        try:
             penultimate_ch = word[-2]
        except IndexError:
            return longest_match
        if tbl.has_key(penultimate_ch):
            tbl = tbl[penultimate_ch]
        else:
            return longest_match
        # Now find the longest matching suffix from a single group.
        for suffix, rep in tbl:
            if word.endswith(suffix) and len(suffix) > len(longest_match[0]):
                longest_match = (suffix, rep)
        return longest_match

    def replace_ends_if(self, suffix_tbl, cond = True, m_thresh = 1):
        if not cond:
            return self.stemmed
        longest_match = self.longest_match(self.stemmed, suffix_tbl)
        if longest_match[0] and self.stem_m(longest_match[0]) > m_thresh:
            self.stemmed = self.rep_end(self.stemmed, longest_match[0],
                     longest_match[1])
        return self.stemmed

    def v_in_stem(self, word, suffix = '', rep = ''):
        """Whether or not word contains a vowel."""
        return self.contains_v(self.rep_end(word, suffix, rep))

    def stem_ends_with_dbl_cons(self):
        #Whether or not the stem ends with double consonant.
        return self.double_c(self.stemmed)

    def stem_ends_with_cvc(self, suffix = '', rep = ''):
         # Whether or not the stem ends with doubCVC pattern.
        # If suffix is given, the check is made after suffix is replaced by rep.
        new_stem = self.stemmed
        if suffix and new_stem.endswith(suffix):
            new_stem = self.rep_end(new_stem, suffix, rep)
        return self.ends_cvc(new_stem)

    def remove_dbl_last_char(self, cond = True):
#Removes doubled last charcter if there is one and cond is True.                                
        if cond and self.stemmed[-2] == self.stemmed[-1]:
            self.stemmed = self.stemmed[:-1]

    def step1ab(self):
#-----------------------Step 1a------------------------------------------------
         self.replace_end('sses', 'ss')
         self.replace_end('ies', 'i')
         self.replace_end('ss', 'ss')
         self.replace_end('s', '', not self.stemmed.endswith('ss'))

#--------------------------Step 1b---------------------------------------------
         if self.stemmed.endswith('eed'):
             self.replace_end('eed', 'ee', self.stem_m('eed') > 0)
         elif self.stemmed.endswith('ed'):
             self.step1b_second_rule = self.replace_end('ed', '',self.v_in_stem(self.stemmed, 'ed'))
         else:
             self.step1b_third_rule = self.replace_end('ing', '',
                     self.v_in_stem(self.stemmed, 'ing'))

    def step1b1(self):
        self.replace_end('at', 'ate')
        self.replace_end('bl', 'ble')
        self.replace_end('iz', 'ize')
        if self.stem_m () == 1 and self.stem_ends_with_cvc():
            self.stemmed += 'e'
            self.remove_dbl_last_char(self.stem_ends_with_dbl_cons()
                        and not self.str_ends_with_char(self.stemmed,
                                                        ['l', 's', 'z']))
                                                        
    def step1c(self):
        self.replace_end('y', 'i', self.v_in_stem(self.stemmed, 'y'))
    
    def step23(self):
#------------------------Step 2------------------------------------------------
        self.replace_ends_if(self.step2_dict,                                                                                                                     self.stem_m() > 0,
                m_thresh = 0)

#----------------------Step 3--------------------------------------------------
        self.stemmed = self.replace_ends_if(self.step3_dict, self.stem_m()>0, 
                                m_thresh = 0)

    def step4(self):
        longest_match = self.longest_match(self.stemmed, self.step4_suffix_tbl)
        if self.stemmed.endswith('ion') and len(longest_match[0]) < len('ion'):
            if self.str_ends_with_char(self.rep_end(self.stemmed, 'ion'),
                    ['s', 't']):
                longest_match = ('ion', '')
        if self.stem_m(longest_match[0]) > 1:
            self.stemmed = self.rep_end(self.stemmed, longest_match[0],
                    longest_match[1])

    def step5(self):
        stem_m = self.stem_m('e')
        if stem_m > 1:
            self.replace_end('e', '')
        elif stem_m == 1 and not self.stem_ends_with_cvc('e'):
            self.replace_end('e', '')
        self.remove_dbl_last_char(self.stem_ends_with_dbl_cons()
            and self.stem_m() > 1
            and self.str_ends_with_char(self.stemmed, ['l']))

        def stem(self, word):
#------------Returns the stemmed word.-----------------------------------------
            self.original_word, self.stemmed = word, word
            self.step1b_second_rule, self.step1b_third_rule = False, False

#-----------Strings with length less than 3 don't get stemmed.-----------------
            if len(self.original_word) < 3:
                return self.stemmed
            self.step1ab()
            if self.step1b_second_rule or self.step1b_third_rule:
                self.step1b1()
                self.step1c()
                self.step23()
                self.step4()        
                self.step5()  
                return self.stemmed

if __name__ == '__main__':
    import sys

    def main():
#-----------Converting Text file into Lower case-------------------------------       
#        with open('Unspeakable-Perk.txt', 'a+') as fileinput:
#           for line in fileinput:
#               line = line.lower()
#               print "".join(line)
#        fileinput.close()
#               sys.stdout=open('Unspeakable.txt',"w")
#               print "".join(sys.stdout))

#------------Tokenize the file-------------------------------------------------
        with open ('Unspeakable-Perk.txt','r') as fin:
#            stopset = set(stopwords.words('english'))
          for line in fin:
#             if not fin in stopset:
                  tokens = word_tokenize(line)
                  print("\n".join(tokens))
                  appendFile=open('Unspeakable-Perk.txt','a')
                  #appendFile.write(""+ )
        fin.close()
#--------Applying Porter Stemmer on given tokenize file------------------------
        stemmer = Stemmer()
        if len(sys.argv) > 1:
             output = []
             for file_ in sys.argv[1:]:
                 for line in file('Unspeakable-Perk.txt', 'r'):
                     output += [stemmer.stem(word) for word in line.split()]
                     print "**************************************************"
                     print "\n".join(output)

main()

