# NRCLex

(C) 2019 Mark M. Bailey

## About
NRCLex will generate an affect list from a body of text.  Affect dictionary is based on the National Research Council Canada (NRC) affect lexicon (see link below).

Lexicon source is (C) 2016 National Research Council Canada (NRC) and this package is **for research purposes only**.  Source: [lexicons for research] (http://sentiment.nrc.ca/lexicons-for-research/)

## Affects
Emotional affects measured include the following:

* fear
* anger
* anticipation
* trust
* surprise
* positive
* negative
* sadness
* disgust
* joy

## Sample Usage

from nrclex import NRCLex

*#Instantiate text object.*
text_object = NRCLex('text')

*#Return words list.*
text_object.words

*#Return sentences list.*
text_object.sentences

*#Return affect list.*
text_object.affect_list

*#Return affect dictionary.*
text_object.affect_dict

*#Return affect frequencies.*
text_object.affect_frequencies