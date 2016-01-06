from flask import Flask, render_template, request
from db import DB
import feedparser
import json

app = Flask(__name__)


@app.route('/',methods=['GET', 'POST'])
def index():
    db = DB()
    feeds = db.selectall()
    return render_template('index.html',feeds=feeds)




@app.route('/add',methods=['POST'])
def add():
    output = {"title":"",'id':'',"response":""}
    url = request.form['url']
    feed = feedparser.parse(url)
    try:
        title = feed['feed']['title']
        
        db = DB()
        output['id'] = db.insert(url,title)
        
        output['title'] = title
        output['response'] = 'ok'
    except IndexError : 
        output['response'] = 'Wrong feed address'
    except KeyError : 
        output['response'] = 'Wrong feed address'
    
    return json.dumps(output)  



@app.route('/fetch',methods=['POST'])
def fetch():
    url = request.form['url']
    feed = feedparser.parse(url)
    output = {'response':'','result':''}
    body = ''
    for post in feed.entries:
        body += u'<div class="post">'
        body += u'<h3 class="post-title"><a href="{}">{}</a></h3>'.format(post.link,post.title)
        body += u'<div class="post-body">{}</div>'.format(post.summary_detail.value)
        body += u'</div>'
        
    output['response'] = 'ok'
    output['result'] =   body.encode('utf8')   
    return json.dumps(output, ensure_ascii=False) 
    
    
    


@app.route('/delete',methods=['POST'])
def delete():
    id = request.form['id']
    output = {'response':'','result':'','ID':id}
    # return json.dumps(output)
    db = DB()
    db.delete(id)
    output['response'] = 'ok'
    return json.dumps(output)  