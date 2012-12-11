#Fetch hebrew links
----

getting a list of english [wikipedia][d1] titles in a simple plain txt **titles.txt** and returning a simple sqlite Db containing a table with the
original titles, if there is a hebrew

##technology:
very simple: using the [Mediawiki Api][d2], kennethrize magical [Requests][d3] and what is probably the best orm in town:[sqlalchemy][d4] (which is probably a huge overkill for a project like this).
##Installing:

you need to have python installed. I did only try this with python 2.7x, not sure if sqlalchemy or requests would work with python 3.x.

just run:

    pip install -r require.txt

##running:
set a **titles.txt** (currently containing sample info) file with all the english titles(every title in a different line) and run:

    python fetch_hebrew_links.py

##play with the Db and enjoy

you can also use the _results.txt_ plain text file with the result

##Notice!

this only checks if there is a hebrew link for the english title! counting that between wikimedia algorithms and volunteers the common case is that this is a True indication.  there can be an english Title that **has a hebrew article which isn't registered in the english title**.  I don't have a way to know that..

[d1]:http://en.wikipedia.org
[d2]:http://www.mediawiki.org/wiki/API%3aQuery_-_Properties#langlinks_.2F_ll
[d3]:http://docs.python-requests.org/en/latest/
[d4]:http://www.sqlalchemy.org/