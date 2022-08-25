from flask import Flask,request,render_template,redirect,make_response
import os,json

app=Flask(__name__)

def uidgen():
	import string
	import random
	characters = list(string.ascii_letters + string.digits)
	length = 25
	random.shuffle(characters)
	password = []
	for i in range(length):
		password.append(random.choice(characters))
	random.shuffle(password)
	return "".join(password)

def get_user_details(user):
    dets=open(f"users/{user}").read().split(",,")
    return dets

@app.route('/')
def home():
    args=request.args.to_dict()
    if request.cookies.get('id')==None or request.cookies.get('password')==None or os.path.exists(f'users/{request.cookies.get("id")}')==False:
        if "login" in list(args.keys()) and args["login"]=="true":
            return render_template("login.html")
        return render_template("reg.html")
    name = request.cookies.get('id')
    return make_response(open("templates/landing.html").read().replace('<!--insert-->','Welcome ' + str(name)))

@app.route('/login')
def login():
    args=request.args.to_dict()
    if open(f"users/{args['id']}").read().split(",,")[0]==args["password"]:
        resp=make_response("You have successfully logged in ! <script>window.location.href='/'</script>")
        resp.set_cookie("id",args["id"])
        resp.set_cookie("password",args["password"])
        return resp
    return make_response("Unsuccessful Login!")

@app.route('/register')
def reg():
    args=request.args.to_dict()
    if os.path.exists(f"users/{args['id']}")==False:
        subjects=[]
        for x in args["subjects"].split(","):
            subjects.append(x)
        open(f"users/{args['id']}","a").write(f'{args["password"]},,{subjects},,{json.dumps(json.loads(args["teacher"]))}')
        resp=make_response("done")
        resp.set_cookie("id",args['id'])
        resp.set_cookie("password",args['password'])
        return resp
    return redirect('/')

@app.route('/test')
def test():
    return make_response(str(request.args.to_dict()))

@app.route('/logout')
def logout():
    resp=make_response("logged out <script>window.location.href='blog'</script>")
    resp.set_cookie('id', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp

@app.route('/blog')
def blog():
    base="""
    <link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;1,100;1,300;1,400&display=swap" rel="stylesheet">
    <style>
    .parav{
        width:100vw;
        height:100vh;
        display: flex;
        justify-content:center;
        align-items:center;

    }
    .card{
        box-shadow: rgba(99,99,99,0.2) 0px 2px 8px 0px;
        padding: 1em;
        font-family:'Lato', sans-serif;
    }
    </style>
    <div class="parav">
    <div class="card" style="width: 18rem;">
    <div class="card-body">
    <h1 style="font-weight: 700;text-align: center;" class="card-title">_title_</h1>
    <p class="card-text">_text_</p>
    </div>
</div></div>
    """
    if request.cookies.get('id')==None or request.cookies.get('password')==None or os.path.exists(f'users/{request.cookies.get("id")}')==False:
        return redirect('/')
    args=request.args.to_dict()
    blogs=json.loads(open("blogs.json").read())
    for x in blogs:
        if x["uuid"]==args["id"]:
            return make_response(base.replace("_title_",x["title"]).replace("_text_",x["data"]))
    if "eco" in get_user_details(request.cookies.get('id'))[1]:
        blogs=json.loads(open("subjects.json").read())["eco"]
        for x in blogs:
            if x["uuid"]==args["id"]:
                return make_response(base.replace("_title_",x["title"]).replace("_text_",x["data"]))
    if "eng" in get_user_details(request.cookies.get('id'))[1]:
        blogs=json.loads(open("subjects.json").read())["eng"]
        for x in blogs:
            if x["uuid"]==args["id"]:
                return make_response(base.replace("_title_",x["title"]).replace("_text_",x["data"]))
    return make_response("Couldn't find ur blog")

@app.route('/eco')
def eco():
    args=request.args.to_dict()
    if request.cookies.get('id')==None or request.cookies.get('password')==None or os.path.exists(f'users/{request.cookies.get("id")}')==False or "eco" not in get_user_details(request.cookies.get('id'))[1]:
        return make_response("Unauth Access")
    layout='<link rel="stylesheet" href="blog.css"><div class"allposts" style="display:flex;justify-content:space-evenly;align-items:center;flex-wrap:wrap">'
    base='<div class="card"> <h2 class="posttitle">.title.</h2> <div class="author" style="text-align: center;">uname</div><div class="article"> data </div><div class="readmore"> <a href="#" class="open" >Read More</a> </div></div> '
    if request.cookies.get('id')==None or request.cookies.get('password')==None or os.path.exists(f'users/{request.cookies.get("id")}')==False:
        return redirect('/')
    blogs=json.loads(open("subjects.json").read())["eco"]
    blogs.reverse()
    for x in blogs:
        layout+=base.replace("uname",f"@{x['uploader']}").replace("data",x["data"]).replace(".title.",x["title"]).replace("#",f'http://127.0.0.1:5000/blog?id={x["uuid"]}')
    return make_response(layout)

@app.route('/eng')
def eng():
    args=request.args.to_dict()
    if request.cookies.get('id')==None or request.cookies.get('password')==None or os.path.exists(f'users/{request.cookies.get("id")}')==False or "eng" not in get_user_details(request.cookies.get('id'))[1]:
        return make_response("Unauth Access")
    layout='<link rel="stylesheet" href="blog.css"><div class"allposts" style="display:flex;justify-content:space-evenly;align-items:center;flex-wrap:wrap">'
    base='<div class="card"> <h2 class="posttitle">.title.</h2> <div class="author" style="text-align: center;">uname</div><div class="article"> data </div><div class="readmore"> <a href="#" class="open" >Read More</a> </div></div> '
    if request.cookies.get('id')==None or request.cookies.get('password')==None or os.path.exists(f'users/{request.cookies.get("id")}')==False:
        return redirect('/')
    blogs=json.loads(open("subjects.json").read())["eng"]
    blogs.reverse()
    for x in blogs:
        layout+=base.replace("uname",f"@{x['uploader']}").replace("data",x["data"]).replace(".title.",x["title"]).replace("#",f'http://127.0.0.1:5000/blog?id={x["uuid"]}')
    return make_response(layout)

@app.route('/upload')
def blog_upload():
    args=request.args.to_dict()
    if request.cookies.get('id')==None or request.cookies.get('password')==None or os.path.exists(f'users/{request.cookies.get("id")}')==False or get_user_details(request.cookies.get('id'))[2]!="true" or args["subject"] not in get_user_details(request.cookies.get('id'))[1]:
        return make_response("Unauth Access")
    blogs=json.loads(open(f"subjects.json").read())
    blogs[args['subject']].append({"uploader":request.cookies.get('id'),"uuid":uidgen(),"data":args['data'],"title":args["title"]})
    open(f"subjects.json","w+").write(str(blogs).replace("'",'"'))
    return make_response("Blog successfully added!")

@app.route('/general_upload')
def blog_general_upload():
    args=request.args.to_dict()
    if request.cookies.get('id')==None or request.cookies.get('password')==None or os.path.exists(f'users/{request.cookies.get("id")}')==False:
        return make_response("Unauth Access")
    blogs=json.loads(open(f"blogs.json").read())
    blogs.append({"uploader":request.cookies.get('id'),"uuid":uidgen(),"data":args['data'],"title":args["title"]})
    open(f"blogs.json","w+").write(str(blogs).replace("'",'"'))
    return make_response("Blog successfully added!")

@app.route('/blogs')
def blogs():
    layout='<link rel="stylesheet" href="blog.css">'
    layout+="""
    <div class="w3-top">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <style>
    .w3-wide {letter-spacing: 10px;}
    .w3-hover-opacity {cursor: pointer;}
  </style>
  <div class="w3-bar" id="myNavbar">
    <a class="w3-bar-item w3-button w3-hover-black w3-hide-medium w3-hide-large w3-right" href="javascript:void(0);" onclick="toggleFunction()" title="Toggle Navigation Menu">
      <i class="fa fa-bars"></i>
    </a>
    <a href="/blogs" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>BLOGS</p></a>
    <a href="/panel" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>UPLOAD</p></a>
    <a href="/oilspill" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>OIL SPILLS</p></a>
    <a href="/plastic" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>PLASTIC POLLUTION</p></a>
    <a href="/marine_life" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>MARINE LIFE</p></a>
    <a href="/logout" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>LOGOUT</p></a>
  </div>
  <div id="navDemo" class="w3-bar-block w3-white w3-hide w3-hide-large w3-hide-medium">
    <a href="/blogs" class="w3-bar-item w3-button" onclick="toggleFunction()">BLOGS</a>
    <a href="/logout" class="w3-bar-item w3-button" onclick="toggleFunction()">LOGOUT</a>
  </div>
</div>
<p style="height:30px;"></p>
    """
    layout+='<div class"allposts" style="display:flex;justify-content:space-evenly;align-items:center;flex-wrap:wrap;">'
    base='<div class="card"> <h2 class="posttitle">.title.</h2> <div class="author" style="text-align: center;">uname</div><div class="article"> data </div><div class="readmore"> <a href="#" class="open" >Read More</a> </div></div> '
    if request.cookies.get('id')==None or request.cookies.get('password')==None or os.path.exists(f'users/{request.cookies.get("id")}')==False:
        return redirect('/')
    blogs=json.loads(open("blogs.json").read())
    blogs.reverse()
    for x in blogs:
        layout+=base.replace("uname",f"@{x['uploader']}").replace("data",x["data"]).replace(".title.",x["title"]).replace("#",f'http://127.0.0.1:5000/blog?id={x["uuid"]}')
    layout+="</div>"
    return make_response(layout)

@app.route('/panel')
def panel():
    return render_template("upload.html")

@app.route("/blog.css")
def give_blogcss():
    return make_response(open("templates/blog.css").read())

@app.route("/landing.css")
def give_landingcss():
    return make_response(open("templates/landing.css").read())

@app.route('/marine_life')
def marine():
    return make_response(open("templates/marinelife.html").read())
@app.route("/oilspill")
def oil():
    return render_template("oilspill.html")
@app.route("/plastic")
def plastic():
    return render_template("plasticpollution.html")

app.run(debug=True)