#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ormtest import *
from flask import Flask
from flask_restful import reqparse, Api, Resource


app=Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object. """
    json = {}
    # json['fields'] = {}
    # json['pk'] = getattr(model, 'id')
    for col in model._sa_class_manager.mapper.mapped_table.columns:
        # json['fields'][col.name] = getattr(model, col.name)
        json[col.name] = getattr(model, col.name)
    # return dumps([json])
    return json


def to_json_list(model_list):
    json_list = []
    for model in model_list:
        json_list.append(to_json(model))
    return json_list


def message(record):
    if record:
        return to_json(record), 200
    return {"message": "not exit"}, 400



class userResource2(Resource):
    def get(self, id):
        record = Usr.query.outerjoin(Phone).group_by(Usr.id)
        sql = "select  usr.id from usr left join phone on usr.id=phone.userId group by usr.id"
        rs = db.session.connection().execute(sql)

        #return to_json_list(record.phone.first())
        for row in rs:
            print row[0]


class userResource(Resource):
    def get(self, id):
        record = Usr.query.filter_by(id=id).first()
        print '-----'
        print  record.phone.first()
        return to_json(record.phone.first())
        #return to_json_list(record.phone.first())

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        args = parser.parse_args(strict=True)
        record = Usr.query.filter_by(id=id).first()
        if record:
            record.username = args['username']
            db.session.commit()
            return {"status": "updated"}, 201
        return {"message": "not exit"}, 400

    def delete(self, id):
        record = Usr.query.filter_by(id=id).first()
        if record:
            db.session.delete(record)
            db.session.commit()
            return {"status": "deleted"}, 204
        return {"message": "not exit"}, 400

class AtrrResource(Resource):
    def get(self, id):
        record = Atttr.query.filter_by(id=id).first()
        return message(record.phone.user)
api.add_resource(HelloWorld, '/')
api.add_resource(userResource, '/user/<int:id>')
api.add_resource(userResource2, '/test/<int:id>')
api.add_resource(AtrrResource, '/atrr/<int:id>')


if __name__=='__main__':
    app.run(debug=False)