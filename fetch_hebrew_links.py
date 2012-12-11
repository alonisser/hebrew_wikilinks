#requirements: installing sqlalchemy and requests.. easily done with pip install
import requests,json
from datetime import datetime,date


from sqlalchemy import create_engine,String,Unicode,Integer,Boolean, Column, func,distinct, desc

connectstring = 'sqlite:///wikilink.db' #using sqlite for simplicy sake
#engine = create_engine(connectstring) #created the engine connecting sqlalchemy to the db

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
Base  = declarative_base()


def init_db():

    engine = create_engine(connectstring) #created the engine connecting sqlalchemy to the db


def load_session():

    Session = sessionmaker(bind = engine)
    session = Session() #the session used to communicate with the db
    return session



class Wikilink(Base):

    __tablename__='Wikilinks'


    id = Column(Integer,autoincrement=True,primary_key=True)
    title = Column(String(350))
    is_hebrew = Column(Boolean)
    hebrew_title=Column(Unicode(350))


    def to_dict(self):
        try:
            title = self.title.encode('utf-8')
        except:
            title = self.title

        return {'id':self.id, 'title':title, 'is_hebrew':self.is_hebrew,'hebrew_title':self.hebrew_title}

def wiki_populate():
    '''a function to populate the db with wikipedia links
    initializing the db and creating the tables if needed.'''

    init_db()
    Wikilink.metadata.create_all(engine)

    ip_range = []
    for i in range(228,238,1):
        for n in range(0,256,1):
            ip_range.append('147.%d.%d'%(i,n))
    #ip_range = ['147.237.70']#debuggin

    for ip in ip_range:
        try:
            wikifetch(ip)
        except:
            continue

def wikifetch(ip,more = None):
    '''A function that does the actuall fetching of edits from wikipedia api'''

    session = load_session()
    timestamp = datetime.now().isoformat()
    headers = {'User-Agent':'wikipediagovmonitoring'}
    if not more:
        print "fetching..%s" %ip
        query = 'http://he.wikipedia.org/w/api.php?action=query&list=usercontribs&format=json&uclimit=500&ucuserprefix=%s&ucdir=newer&ucprop=title|ids' % ip
    else:
        print 'fetching continues for ip ', ip
        query = 'http://he.wikipedia.org/w/api.php?action=query&list=usercontribs&format=json&uclimit=500&ucuserprefix=%s&uccontinue=%s&ucdir=newer&ucprop=title|ids' % (ip, more)
    #print ip
    try:
        r = requests.get(query,headers=headers)
    except:
        print "raising error from ip:%s" % ip
        raise
    if r.ok:
        content = json.loads(r.content)
        print "number of items from %s is %s" % (ip,len(content['query']['usercontribs']))
        for i in content['query']['usercontribs']:
            link = Wikilink(user_ip=i['user'],
                            title=i['title'][0:350],
                            page=i['pageid'],
                            revision=i['revid'],
                            timestamp=timestamp)

            #print edit
            session.add(link)
            #print link.id,link.title, link.page, link.timestamp, link.revision,link.user_ip
            session.flush()

        # if content.get('query-continue',False):
        #     wikifetch(ip,more =content['query-continue']['usercontribs']["uccontinue"])#recursive call to the function if there is more data in the same Ip
if __name__ == '__main__':
    wiki_populate()