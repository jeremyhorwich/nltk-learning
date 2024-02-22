Using this as a catch all repository for any various NLP learning projects that make use of or are based off of principles from the NLTK library.

1. complexityDetection.py:

- Created this as a wrap-up to my reading of this page: https://www.nltk.org/book/ch08.html. I intentionally did not use the NLTK library for this as I wanted to test my understanding of concepts behind library functions discussed in the aforementioned link.
- Originally the goal of this algorithm was to be able to detect if a sentence had ambiguity without constructing the full sentence. However, I quickly realized that ambiguity is a meaningless term without the construction of a full sentence as a prerequisite - in other words, saying a phrase is ambiguous doesn't make sense unless you know the sentence can be fully parsed successfully at least two different ways
- Modifying WFST would work very well, but using that would be too obvious for it to be of any real value to me as an exercise
- Ultimately I didn't want to simply abandon the work so I refactored into a less ambitious algorithm which detects if a sentence is anything more than extremely simple from a syntactic standpoint. It uses a bottom up approach similar to shift-reduce parsing
- Test cases: "I shot an elephant" should return False. "I shot an elephant in my pajamas" should return True.
