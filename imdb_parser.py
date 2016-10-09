# import library here
import requests
import sqlite3
from bs4 import *
from bs4 import NavigableString
import sys


# add_tv function definition

def add_tv(title):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # sqlite3 connection creation

    connect = sqlite3.connect("imdb.db")
    conn = connect.cursor()
    tb_create = '''CREATE TABLE tv_series
                 (id INTEGER PRIMARY KEY, name text unique)'''
    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='tv_series'"
    if not conn.execute(tb_exists).fetchone():
            conn.execute(tb_create)
            connect.commit()

    tb_create = '''CREATE TABLE episodes
                 (id INTEGER, name text, airdate text)'''
    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='episodes'"
    if not conn.execute(tb_exists).fetchone():
            conn.execute(tb_create)
            connect.commit()

    # after creating a connection have done some regular check and tasks

    # main code starts from here

    # base url for the site
    base ='http://www.imdb.com/title/'

    url=base+title
    # header is needed for http request
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # recieve the response for the request generated

    response = requests.get(url, headers=headers)
    
    # modifying for usage using beautifulsoup
    soup=BeautifulSoup(response.content)

    # find all h1 tag which got an itemprop attribute  that has a value of
    # name

    tags=soup.find("h1",{"itemprop":"name"})
    
    # query for inserting the tv series name in database
    insert_tv = 'INSERT INTO tv_series VALUES (null,?)'

    # query for get the id of the latest inserted tv series
    get_id = 'SELECT * FROM tv_series WHERE name = ?'
    series_id = "";
    if tags is None:
        return None
    for tag in tags:
        name=tag.string
        name = name.strip()
        # print name
        # inserting tv_series name
        conn.execute("SELECT id FROM tv_series WHERE name = ?", (name,))
        data=conn.fetchone()
        if data is None:
            conn.execute(insert_tv,(name,))
            connect.commit()
            # getting the latest tv series's id
            tv_id = conn.execute(get_id,(name,)).fetchone()
            series_id=tv_id[0]
            # print series_id 

        else:
            return False
    tags = soup.find("a",{"class":"bp_item np_episode_guide np_right_arrow"})
    for tag in tags:
        #print tag.parent
        if isinstance(tag.parent, NavigableString):
            continue
        else:
            l = list()
            if tag.parent.has_attr('href'):
                new_url=tag.parent['href']
                new_url="http://www.imdb.com"+new_url
                #print(new_url)
                response = requests.get(new_url,headers=headers)
                soup=BeautifulSoup(response.content)
                tagsss = soup.find("div",{"class":"list detail eplist"})
                for tagss in tagsss:
                    #print tagss.parent
                    ep_name = tagss.parent.find_all("a",{"itemprop":"name"})
                    air = tagss.parent.find_all("div",{"class":"airdate"})
                    counter = 0
                    for ep_nam in ep_name:
                        name = ep_nam.string
                        tv_series = dict()
                        name = name.strip()
                        tv_series["name"] = name
                        tv_series["air"]=""
                        l.append(tv_series)
                        counter=counter+1
                    counter=0
                    for air_dat in air:
                        air_date = air_dat.string
                        air_date = air_date.strip()
                        tv_series = l[counter]
                        tv_series["air"] = air_date
                        l[counter]=tv_series
                        counter = counter + 1
                    break
                insert_ep = "INSERT INTO episodes VALUES(?,?,?)"
                for li in l:
                    # print li["name"]
                    # print li["air"]
                    conn.execute(insert_ep,(series_id,li["name"],li["air"],))
                    connect.commit()
        break
    # fetch_all = "SELECT * FROM episodes WHERE id = ?"
    # rows = conn.execute(fetch_all,(series_id,)).fetchall()
    # conn.close()
    # for row in rows:
    #     print row[0]
    #     print row[1]
    #     print row[2]
    print "successfully saved data"
    conn.close()
    return "successfully saved data"


def get_all():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # sqlite3 connection creation

    connect = sqlite3.connect("imdb.db")
    conn = connect.cursor()
    tb_create = '''CREATE TABLE tv_series
                 (id INTEGER PRIMARY KEY, name text unique)'''
    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='tv_series'"
    if not conn.execute(tb_exists).fetchone():
            conn.execute(tb_create)
            connect.commit()

    tb_create = '''CREATE TABLE episodes
                 (id INTEGER, name text, airdate text)'''
    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='episodes'"
    if not conn.execute(tb_exists).fetchone():
            conn.execute(tb_create)
            connect.commit()


    l = list()
    select_all = "SELECT * FROM tv_series"
    data = conn.execute(select_all).fetchall()
    for tv in data:
        rows=dict()
        rows["id"]=tv[0]
        rows["name"]=tv[1]
        rows["episodes"]=""
        series_id = tv[0]
        print rows["name"]
        print series_id
        sel_ep = "SELECT * FROM episodes where id = ?"
        res = conn.execute(sel_ep,(series_id,)).fetchall()
        rows["episodes"]=res
        l.append(rows)
    conn.close()
    return l

