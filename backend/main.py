from flask import request, jsonify
from models import User, Ticket
from config import app, db

# GET
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_json() for user in users])

@app.route("/api/user/<int:uid>", methods=["GET"])
def get_user(uid):
    user = User.query.filter_by(uid=uid).first()
    if user == None:
        return jsonify({"message":"User not found"}), 404
    return jsonify(user.to_json())

@app.route("/api/tickets", methods=["GET"])
def get_tickets():
    tickets = Ticket.query.all()
    if tickets == []:
        return jsonify({"message":"No tickets exist"})
    return jsonify([ticket.to_json() for ticket in tickets])

@app.route("/api/ticket/<int:tid>", methods=["GET"])
def get_ticket(tid):
    ticket = Ticket.query.filter_by(tid=tid).first()
    if ticket == None:
        return jsonify({"message":"Ticket not found"}), 404
    return jsonify(ticket.to_json())

@app.route("/api/user/<int:uid>/tickets", methods=["GET"])
def get_user_tickets(uid):
    tickets = Ticket.query.filter_by(owner_id=uid).all()
    if tickets == []:
        return jsonify({"message":f"No tickets for uid={uid}"})
    return jsonify([ticket.to_json() for ticket in tickets])


# POST
@app.route("/api/users", methods=["POST"])
def create_user():
    user = User.query.filter_by(uid=data["uid"]).first()
    if user != None:
        return jsonify({"message":"User already exists"}), 409
    
    # validation
    data = request.get_json()
    if not (data["username"] | data["uid"]):
        return jsonify({"message":"Some fields are missing"}), 404
    
    if not data["username"].isalnum():
        return jsonify({"message":"Username must be alphanumeric"}), 404
    elif len(data["username"]) > 50:
        return jsonify({"message":"Max username length is 50 characters"}), 404
    
    
    new_user = User(username=data["username"], uid=data["uid"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"})

@app.route("/api/tickets", methods=["POST"])
def create_ticket():
    data = request.get_json()
    
    user = User.query.filter_by(uid=data["uid"]).first()
    if user == None:
        return jsonify({"message":"User does not exist"}), 404
    
    # validation
    if not (data["title"] | data["description"] | data["ownerId"] ):
        return jsonify({"message":"Some fields are missing"}), 404
    
    if len(data["title"]) > 50:
        return jsonify({"message":"Max title length is 50 characters"}), 404
    
    if len(data["description"]) > 500:
         return jsonify({"message":"Max description length is 500 characters"}), 404
    
    
    new_ticket = Ticket(title=data["title"], description=data["description"], owner_id=data["ownerId"])
    db.session.add(new_ticket)
    db.session.commit()
    return jsonify({"message": "Ticket created"})


# PATCH
@app.route("/api/user/<int:uid>", methods=["PATCH"])
def update_user(uid):
    user = User.query.get(uid)
    
    if not user: 
        return jsonify({"message": "User not found"}), 404
    
    # validation
    data = request.json
    if not data["username"]:
        return jsonify({"message":"Some fields are missing"}), 404
    elif not data["username"].isalnum():
        return jsonify({"message":"Username must be alphanumeric"}), 404
    elif len(data["username"]) > 50:
        return jsonify({"message":"Max username length is 50 characters"}), 404
    
    user.username = data["username"]
    db.session.commit()
    return jsonify({"message": "User updated"})

@app.route("/api/ticket/<int:tid>", methods=["PATCH"])
def update_ticket(tid):
     ticket = Ticket.query.get(tid)
     
     if not ticket:
         return jsonify({"message": "Ticket not found"}), 404
     
     # validation
     data = request.json
     if not (data["title"] | data["description"] | data["completed"]):
        return jsonify({"message":"Some fields are missing"}), 404
     
     if len(data["title"]) > 50:
         return jsonify({"message":"Max title length is 50 characters"}), 404
     
     if len(data["description"]) > 500:
         return jsonify({"message":"Max description length is 500 characters"}), 404
     
     if data["completed"] != True | False:
         return jsonify({"message":"Completed is a boolean field"}), 404
    
     ticket.title = data["title"]
     ticket.description = data["description"]
     ticket.completed = data["completed"]
     db.session.commit()
     return jsonify({"message": "Ticket updated"})
 
@app.route("/api/ticket/<int:tid>/check", methods=["PATCH"])
def check_ticket(tid):
     ticket = Ticket.query.get(tid)
     
     if not ticket:
         return jsonify({"message": "Ticket not found"}), 404
     
     was_completed = ticket.completed
     ticket.completed = not ticket.completed
     db.session.commit()
     
     if was_completed:
         return jsonify({"message": "Ticket uncompleted"})  
     return jsonify({"message": "Ticket completed"})
  

# DELETE
@app.route("/api/user/<int:uid>", methods=["DELETE"])
def delete_user(uid):
    user = User.query.get(uid)
    
    if not uid:
        return jsonify({"message": "user not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User permanently deleted"})

@app.route("/api/ticket/<int:tid>", methods=["DELETE"])
def delete_ticket(tid):
    ticket = Ticket.query.get(tid)
     
    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404
     
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket permanently deleted"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)