# Generic Spell Checker
This repo should serve as the final project of Fall 2016 CS598 from University of Illinois at Urbana-Champaign, lectured by [Prof. Chengxiang Zhai][prof].

## Content
In this repo, you can find a simple design of a generic spell correction framework with sets of predefined datasets, models and evaluation methods. The purpose of this framework is to help researchers and professionals to be more productive in proposing and evaluating their spell correction models. 

The package itself comes with a `setup.py` script, however, it is recomended to use the files directly as these contents are subject to change in future release.

## Acknowledgment
The dataset we incorporated into our corpus are from Google Research, released by [Peter Norvig][peter]. Information about the dataset can be found on its [official website][web].

## Tutorial
To run the default gHMM model with framework default lexicon, go to GenericSpellChecker/spellcorrect/ghmm and run 
```
python algorithm2.py [query to correct] [max number of correction ] [path to lexicon]
```
An example of such run is:
```
python algorithm2.py “a dat saton a door mat” 3 ../../file.txt
```
By default, the result will contain 3 types of errors:
* Transformation: dat->cat
* Splitting: saton-> sat on
* Merging: door mat -> doormat



[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [prof]: http://czhai.cs.illinois.edu/
   [peter]: http://norvig.com/
   [web]: http://norvig.com/ngrams/
