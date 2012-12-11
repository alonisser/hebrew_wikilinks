#requirements: installing sqlalchemy and requests.. easily done with pip install
import requests,json
from datetime import datetime,date
from sqlalchemy import create_engine,String,Unicode,Integer,Boolean, Column, func,distinct, desc

connectstring = 'sqlite:///wikilink.db' #using sqlite for simplicy sake
engine = create_engine(connectstring)
#engine = create_engine(connectstring) #created the engine connecting sqlalchemy to the db

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
Base  = declarative_base()


def init_db():

    engine = create_engine(connectstring) #created the engine connecting sqlalchemy to the db
    return engine

def load_session():

    Session = sessionmaker(bind = engine)
    session = Session() #the session used to communicate with the db
    return session

session = load_session()

class Wikilink(Base):

    __tablename__='Wikilinks'


    id = Column(Integer,autoincrement=True,primary_key=True)
    title = Column(String(350))
    is_hebrew = Column(Boolean)
    hebrew_title=Column(Unicode(350))
    is_error = Column(Boolean)


    def to_dict(self):
        try:
            title = self.title.encode('utf-8')
        except:
            title = self.title

        return {'title':title,'hebrew_title':self.hebrew_title, 'is_hebrew':self.is_hebrew}

    def __str__(self):
        return self.to_dict().get('title') + ' has hebrew link: '+str(self.to_dict().get('is_hebrew'))

def wiki_populate():
    '''a function to populate the db with wikipedia links
    initializing the db and creating the tables if needed.'''

    Wikilink.metadata.create_all(engine)
    #uncomment the next block to enable db delete on each run
    # session.query(Wikilink).delete()
    # session.commit()



    with open("titles.txt") as f:
        for title in f.readlines():

            try:
                wikifetch(title = title.rstrip("\n"))
            except:
                link = Wikilink(title = title, is_error = True)
                session.add(link)
                session.flush()
    session.commit()


def wikifetch(title, more = None):
    '''A function that does the actuall fetching hebrew titles from wikipedia api'''


    headers = {'User-Agent':'wikipedia_getting_hebrew_title'}

    print "fetching..%s" % title
    query = 'http://en.wikipedia.org/w/api.php?action=query&format=json&lllimit=500&titles=%s&prop=langlinks' % title

    try:
        r = requests.get(query,headers=headers)
        print r.url
    except:
        print "raising error from title %s" % title
        raise
    if r.ok:
        content = json.loads(r.content)
        value = content['query']['pages'].keys()[0]
        is_hebrew = False
        hebrew_title = None
        links = content['query']['pages'][value]['langlinks']

        for lang in links:

            if lang['lang'] == 'he':
                is_hebrew = True
                hebrew_title = lang[r'*'][0:350]
                break
            else:
                is_hebrew = False
                hebrew_title = None


        link = Wikilink(is_hebrew  = is_hebrew,
                        title = title,
                        hebrew_title = hebrew_title)
        session.add(link)
        session.commit()

        # if content.get('query-continue',False):
        #     wikifetch(ip,more =content['query-continue']['usercontribs']["uccontinue"])#recursive call to the function if there is more data in the same Ip
if __name__ == '__main__':
    wiki_populate()
    engine = init_db()
    session = load_session()
    db = session.query(Wikilink).all()
    with open('results.txt','w') as f:
        for line in db:
            line = str(line) + '\n'
            f.write(line)