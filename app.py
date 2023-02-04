from flask import Flask,render_template,redirect,url_for,request
from pymongo import MongoClient

app=Flask("__name__")

@app.route("/")
def Show():
    client=MongoClient("mongodb://localhost:27017")
    database=client.stu
    collection=database.students
    data=collection.find()
    l=[]
    for i in data:
        l.append(i)
    client.close()

    return render_template("show.html",data=l)

@app.route("/insert",methods=["POST","GET"])
def Insert():
    if request.form.get("regno")!=None:
        regno=request.form.get("regno")
        name=request.form.get("name")
        email=request.form["email"]
        dic={"regno":regno,"name":name,"email":email}

        client=MongoClient("mongodb://127.0.0.1:27017")
        database=client.stu
        collection=database.students
        collection.insert_one(dic)
        client.close()

        return redirect(url_for("Show"))
    
    return render_template("insert.html")

@app.route("/insertBulk",methods=["POST","GET"])
def InsertBulk():
    datas=request.json

    connection=MongoClient("mongodb://localhost:27017")
    database=connection.stu
    collection=database.students
    collection.insert_many(datas)
    connection.close()

    return redirect(url_for('Show'))

@app.route("/update/<id>",methods=["POST","GET"])
def Update(id):
    if request.form.get("regno")!=None:
        regno=request.form["regno"]
        name=request.form["name"]
        email=request.form["email"]

        client=MongoClient("mongodb://localhost:27017")
        database=client.stu
        collection=database.students
        collection.update_one({"regno":regno},{"$set":{"name":name,"email":email}})
        client.close()

        return redirect(url_for("Show"))

    client=MongoClient("mongodb://127.0.0.1:27017")
    database=client.stu
    collection=database.students
    data=collection.find_one({"regno":id})
    l=dict(data)
    client.close()

    return render_template("update.html",data=l)

@app.route("/updateBulk/<name>,<value>")
def UpdateBulk(name,value):
    client=MongoClient("mongodb://localhost:27017")
    database=client.stu
    collection=database.students
    collection.update_many({"name":name},{"$set":{"name":value}})
    return redirect(url_for("Show"))


@app.route("/delete/<id>")
def Delete(id):
    client=MongoClient("mongodb://localhost:27017")
    database=client.stu
    collection=database.students
    collection.delete_one({"regno":id})
    client.close()

    return redirect(url_for("Show"))

@app.route("/deleteBulk/<name>")
def DeleteBulk(name):
    client=MongoClient("mongodb://localhost:27017")
    database=client.stu
    collection=database.students
    collection.delete_many({"name":name})
    client.close()

    return redirect(url_for("Show"))

if __name__=="__main__":
    app.run(debug=True)