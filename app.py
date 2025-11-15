import json # import the json library


from openai import OpenAI

from flask import ( # importing all the necessarily libraries and functions for the flask work 
    Flask, #It is used to create the website application
    render_template, #It is used to open the HTML file (front-end)
    redirect, #It is used to transfer to another pages through the "/..." URL 
    request, #It is used to request information from HTML file
    make_response, #It is used to create from response an object to castomize it
    jsonify, #It is used for easily returning JSON data with proper headers in Flask apps  
    flash, #It is used to send messages to the user
    url_for #It is used to create a URL for the specified endpoint
)

host = "0.0.0.0" #This tells your operating system to listen on all public IPs.
port = 29077 #It is is a number assigned to uniquely identify a connection endpoint
app = Flask(__name__, template_folder='./templates', static_folder='./static') #creates a Flask application in the current Python file.

num = 0 
lyrc = ""
username = ""
dic = {} #It is required for the json file to have before adding anything
app.secret_key= "secret key" #It is used to keep the client-side sessions secure
openai = OpenAI(api_key="Your-Key") #It is used to create the object of the OpenAI class

def loadsetting():
    with open("./appsetting.json", "r") as file: #Opens the json file with AI settings, read only
        data = json.load(file) #Loads everzthing to data
        return data["API_KEY"],data["AI"]["Model"], data["AI"]["SystemRole"] #Returns all the content of the Translator settings 
    
def loadsetting1():
    with open("./appsetting.json", "r") as file: #Opens the json file with AI settings, read only
        data = json.load(file) #Loads everzthing to data
        return data["API_KEY"],data["AI1"]["Model"], data["AI1"]["SystemRole"] #Returns all the content of the Meaning settings
    
def create_Image(respo):
    model = "dall-e-3" # Set the model to use for image generation
    # Generate an image based on the prompt
    response = openai.images.generate(prompt=respo, model=model) # Generate an image based on the prompt

    # Extract the URL of the generated image (adjust based on the response structure)
    return response.data[0].url # Extract the URL of the generated image (adjust based on the response structure)

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST": #It is used to send data to a server to create/update a resource
        ... #It is used to skip the code
    if request.method == "GET": #It is used to request data from a specified resource
        Cookies = request.cookies.get('Username') #Gets information of cookie under name Username
        
        if Cookies is not None: #Checks if the cookie is not empty
            global lyrc #Allows to change variable outside of the local scope
            lyrc = f"{Cookies}.json" #Sets the personal database for the user
            return redirect("/homepage") #If yes it allows to enter the website
        else:
            return redirect("/login") #If no it will send person to the login page
        
@app.route("/signup", methods=["GET", "POST"])  
def singup():
    if request.method == "POST": #It is called when user creates account
        username = request.form.get("username") #Gets the information from HTML file (Frontend)
        password = request.form.get("password") #Gets the information from HTML file (Frontend)
        conpassword = request.form.get("conpassword") #Gets the information from HTML file (Frontend)

        with open("data.json", "r") as file: #Open file with passwords and usernames
            data = json.load(file) 
        data = list(data)
        for jsonObj in data: #It is going through whole dictionary and check every ones 
            if jsonObj["username"] == username: #If password and username is verified
                    flash("Username is already taken", 'error') #If the username is already taken, it will ask to fill everything one more time
                    return redirect(url_for('singup'))
        if conpassword == password: #Check if the password and conpassword are same
                js = f"{username}.json" #Sets the name for the JSON file
                with open(js, "w") as outfile: #Create the json file under name js
                    json.dump(dic, outfile) #Adds dic to the new json file
                with open("data.json", "r") as file: #Opens the json file with usernames and passwords for read only
                    data = json.load(file) #It loads information from json to data
                data = list(data) #Makes the data a list
                with open("data.json", "r") as file: #Open file with passwords and usernames
                    data = json.load(file) 
                data = list(data) #creating from data the list
                data.append({
                    "username": username, #Sets the dictionary username
                    "password" : password #Sets the dictionary password
                })

                with open("data.json","w") as file: #Allows to change the jsonfile
                    json.dump(data,file) #Adds the new user information to the database
                return redirect("/login") #Sends back to the login page
        else:
            flash("Passwords are not equal", 'error') #If the password and conpassword isn't equal, it will ask to fill everything one more time
            return redirect("/signup") #If the password and conpassword isn't equal, ask to fill everything one more time 
    if request.method == "GET": #It is called when Singup page is opened
        return render_template("signup.html") #Opens the HTML file 

@app.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect("/login"))
    response.set_cookie('Username', "0", expires=0)
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    global username #Allows to change variable outside of the local scope
    if request.method == "POST": #It is called when user tries to login in
        username = request.form.get("username") #Gets information from HTML file (front end) 
        password = request.form.get("password") #Gets information from HTML file (front end)
        response = request.form.get("Cockies") #Gets information from HTML file (front end)
        with open("data.json", "r") as file: #Opens the json file with usernames and passwords for read only
            data = json.load(file) #It loads information from json to data
        data = list(data) #Makes the data a list
        for jsonObj in data: #It is going through whole dictionary and check every ones 
            if jsonObj["username"] == username and jsonObj["password"] == password: #If password and username is verified
                global lyrc #Allows to change variable outside of the local scope
                lyrc = f"{username}.json" #Sets the username for the personal database
                if response == "TRUE": #If the user wants to save the username
                    response = make_response(redirect("/homepage", code=302)) #Allows the return function to be configurated
                    response.set_cookie('Username', username, 600,secure=True) #Sets the cookies with username for the session 
                    return response #Transfer to the homepage and sets coockies
                return redirect("/homepage") #If the user doesn't want to save the username, it will transfer to the homepage
        flash("Invalid Username/Password", 'error') #If there is no matching, it will ask to fill everything one more time
        return redirect("/login") #If there is no matching, it will reload login page

    if request.method == "GET": #It is called when page is open
        return render_template("login.html") #It opens the HTML file
    
@app.route("/homepage", methods=["GET", "POST"])    
def homepage():
    if request.method == "POST":
        user = ""
    if request.method == "GET": 
        global lyrc #Allows to change variable outside of the local scope
        return render_template("homepage.html", username = username) 
    
@app.route("/addnewsong", methods=["GET", "POST"])
def addnewsong():
    if request.method == "POST":
        name = request.form.get("name")
        nameg = request.form.get("nameg")
        lyric = request.form.get("lyric")
        image = request.form.get("image")
        

        with open(lyrc, "r") as file:
            data = json.load(file)
        
        data = list(data) #creating from data the list
        data.append({
            "name": name,
            "nameg": nameg,
            "lyric" : lyric,
            "image" : image
        })

        with open(lyrc,"w") as file:
            json.dump(data,file)#here it is input data to file 
        return redirect("/homepage")
    if request.method == "GET":
        return render_template("addnewsong.html")
    
@app.route("/database", methods=["GET", "POST"])  
def database(): 
    button = 0 #Initialize a variable
    dele = int(4) #Initialize a variable as a variable
    edit = int(4) #Initialize a variable as a variable
    if request.method == "POST":
        if request.form.get('button_id') is not None: #Checks if the user pressed one of the button "Lyrics"
            num = request.form.get('button_id') #Gets the value of the button
            with open("num.json", "r") as file: #
                data = json.load(file)
            data = list(data)
            data.append({"num": num}) #Adds number to the data list

            with open("num.json", "w") as file:
                json.dump(data, file)
            return redirect('/lyric') #Transfer to the lyrics page
        
        elif request.form.get('delet') is not None: #Checks if the user pressed button "delete"
            num = request.form.get('delet') #Gets the value of the button
            
            with open(lyrc, "r") as file: #Opens personal database
                data = json.load(file)
            data = list(data)
            del data[int(num)]
            with open(lyrc, "w") as file:
                json.dump(data, file)
            return redirect('/homepage') #Transfer to the homepage

        elif int(request.form.get('edit')) is not None: #Checks if the user pressed button "edit"
            num = request.form.get('edit') #Gets the value of the button
            with open("edit.json", "r") as file: #
                data = json.load(file)
            data = list(data)
            if len(data) != 0:
                del data[0]
            data.append({"num": num}) #Adds number to the data list

            with open("edit.json", "w") as file:
                json.dump(data, file)
            return redirect('/edit') #Transfer to the lyrics page

    if request.method == "GET":
            with open(lyrc, "r") as file: #Opens personal database
                data = json.load(file) #Loads the data from the json file
            button = len(data) #Assign the ammount of song to the variable button
            return render_template("database.html", username=username, button=button, data=data) #Open HTML file (fronend), and transfer some variables
    
@app.route("/translator", methods=["GET", "POST"])
def translator():
    if request.method == "POST":
        num = int(request.form.get('exampleList'))  
        lang = request.form.get("lang")

        with open(lyrc, "r") as file: #Opens JSON file with lyrics
           data = json.load(file) #Loads it to the data
        lyric = data[num]["lyric"] #It takes the lyrics under position num

        key, Model_Name, System_Role = loadsetting() #Tt loads the settings from the json file
        openai.api_key = key #Sets the apikey
        content = f"mode:0 | translate to {lang}: {lyric}" #Sets the reqeust for the OpenAI
        
        response = openai.chat.completions.create( #Creates the request
            model=Model_Name, #Sets the model of the ChatGPT
            messages=[ #Content of the request
                {"role": "system", "content": System_Role}, #Sets the instruction for the AI
                {"role": "user", "content": content} #The request it self
            ]
        )
        respo = response.choices[0].message.content #Takes only response of the AI
        
        with open("tran.json", "r") as f:
            data = json.load(f)
        data = list(data)
        if len(data) != 0:
            del data[0]
        data.append({"tran": respo})

        with open("tran.json", "w") as f:
           json.dump(data, f)
        
        return redirect('/tran')
    if request.method == "GET":
        with open(lyrc, "r") as file:
            data = json.load(file)
        button = len(data)
        return render_template("translator.html", button=button, data=data)

@app.route("/lyric", methods=["GET", "POST"])
def lyric():
    nums = int(0)
    if request.method == "POST": 
        ...
    if request.method == "GET": 
        with open("num.json", "r") as f:
            prata = json.load(f)
        nums = int(prata[0]["num"]) 
        del prata[0]
        with open("num.json", "w") as file:
            json.dump(prata,file)
        with open(lyrc, "r") as file:
            data = json.load(file)
        data = list(data)
        lyric = data[nums]["lyric"] 
        return render_template("lyric.html", lyric=lyric)
    
@app.route("/tran", methods=["GET", "POST"])
def translation():
        if request.method == "POST":
            ...
        if request.method == "GET":
                # Load the JSON data
                with open("tran.json", "r") as file:
                    data = json.load(file)
                lyr = data[0]["tran"]
                del data[0]
                with open("tran.json", "w") as file:
                    json.dump(data,file)
                return render_template("translate.html", lyr=lyr)

@app.route("/meaning", methods =["GET", "POST"])
def meaning():
    if request.method == "POST":
        num = int(request.form.get('exampleList')) 

        with open(lyrc, "r") as file:
           data = json.load(file)
        lyric = data[num]["lyric"] #It sets the lyrics under position num

        key, Model_Name, System_Role = loadsetting1() #It loads the settings from the json file
        openai.api_key = key #It sets the apikey
        content = f"Explain lyrics: {lyric}" #It sets the request for the OpenAI
        
        response = openai.chat.completions.create(  #It creates the request
            model=Model_Name, #It sets the model of the ChatGPT
            messages=[  #Content of the request
                {"role": "system", "content": System_Role}, #It sets the instruction for the AI
                {"role": "user", "content": content}    #The request it self
            ]
        )
        respo = response.choices[0].message.content #It takes only response of the AI

        if request.form.get("photo") == "TRUE":   #It checks if the user wants to have a photo
            image = create_Image(respo) #It creates the image
        else:
            image = "" #If the user doesn't want to have a photo, it sets the image as empty
        
        with open("meaning.json", "r") as f: #Allows to read json file
            data = json.load(f) #Import all the information from json file to variable data
        data = list(data) #Create from variable data the list
        data.append({"meaning": respo, "photo": image})  # Add serialized data to the list data

        with open("meaning.json", "w") as f: #Allows to change the json file
            json.dump(data, f) #Add all the changes from list data to the json file
            
        return redirect('/meaning')
    if request.method == "GET":
        with open("meaning.json", "r") as file:
            data = json.load(file)
        if len(data) != 0:
            meaning = data[0]["meaning"]
            photo = data[0]["photo"]
            del data[0]
            with open("meaning.json", "w") as file:
                json.dump(data,file)
        else:
            meaning = ""
            photo = ""
        with open(lyrc, "r") as file:
            data = json.load(file)
        button = len(data)
        if photo == "" or photo == None:
            return render_template("meaning.html", button=button, data=data, meaning=meaning)
        else:
            return render_template("meaning.html", button=button, data=data, meaning=meaning, photo=photo)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    nums = int(0)
    if request.method == "POST":
        name = request.form.get("name")
        nameg = request.form.get("nameg")
        lyric = request.form.get("lyric")
        image = request.form.get("image")

        with open("edit.json", "r") as f:
            data = json.load(f)
        nums = int(data[0]["num"])
        with open(lyrc, "r") as file:
            data = json.load(file)
        
        data[nums]["name"] = name
        data[nums]["nameg"] = nameg
        data[nums]["lyric"] = lyric
        data[nums]["image"] = image

        with open(lyrc,"w") as file:
            json.dump(data,file)
        return redirect("/homepage")
    
    if request.method == "GET":
        with open("edit.json", "r") as f:
            prata = json.load(f)
        nums = int(prata[0]["num"]) 
        with open(lyrc, "r") as file:
            data = json.load(file)
        data = list(data)
        lyric = data[nums]["lyric"]
        nameg = data[nums]["nameg"]
        name = data[nums]["name"]
        image = data[nums]["image"]
        return render_template("edit.html", lyric=lyric, nameg=nameg, name=name, image=image)
    
#webview.create_window('Lyrics', app) #Creates the window with the name "Lyrics"   
if __name__ == "__main__": #it tests if the script is running directly or is imported somewhere else
    app.run(host=host,port=port, debug=True) #this function starts the webpage
    #webview.start()
    