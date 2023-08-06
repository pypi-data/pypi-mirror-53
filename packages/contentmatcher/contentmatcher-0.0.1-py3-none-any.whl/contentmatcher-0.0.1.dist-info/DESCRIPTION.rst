# contentmatcher  
A pattern-based content matcher for Python programs  

##### Current state: Under development (alpha)  


It provides:  
  * Match ratios based on amount of pattern that was matched  
  * Fast method for first-pass match
    * Allows filtering out patterns that are unlikely to match  
    * More thorough matching can be performed with patterns that are more likely to match, reducing time requirements  

Original use case:  
  * matching a list of function names from a backtrace to known patterns  

Installation:  
  * pip install contentmatcher  

Tested for Python >=3.6.5 on Linux (Ubuntu) and Windows 7/10  


