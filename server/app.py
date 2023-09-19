from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages_all = Message.query.order_by(Message.created_at.asc()).all()
    messages_list = []
    for each in messages_all:
        message_dict = each.to_dict()
        messages_list.append(message_dict)
    response = make_response(messages_list,200)
    return response

@app.route("/messages", methods = ["POST"])
def posted():
    if request.is_json:
        data = request.get_json()
        new_message = Message(
            username =  data.get("username"),
            body =  data.get("body"),
        )
        db.session.add(new_message)
        db.session.commit()
    response_body = new_message.to_dict()
    response = make_response(response_body,201)
    return response


    

@app.route('/messages/<int:id>',methods = ["PATCH"])
def messages_by_id(id):
    Post_by_id = Message.query.filter(Message.id == id).first()
    if request.is_json:
        data = request.get_json()
        for key,value in data.items():
            setattr(Post_by_id,key,value)
        db.session.commit()
        
   
    response_body = Post_by_id.to_dict()
    response = make_response(response_body,201)
    return response
@app.route("/messages/<int:id>", methods = ["DELETE"])
def deleted_message(id):
    deleted_by_id = Message.query.filter(Message.id == id).first()
    db.session.delete(deleted_by_id)
    db.session.commit()




        
    

if __name__ == '__main__':
    app.run(port=5555)
