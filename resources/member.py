import datetime

from flask import request, render_template, Blueprint, json
from flask_restplus import Resource, fields, Namespace, inputs, reqparse

from models.member import MemberModel

MEMBER_NOT_FOUND = "Member not found."

viewer = Blueprint('viewer', __name__, template_folder="templates")


member_ns = Namespace('member', description='member namespace')
members_ns = Namespace('members', description='member namespace')

member = members_ns.model('Member', {
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'profile_image': fields.Raw,
    'dues_paid': fields.Boolean,
    'last_dues_payment': fields.Date(format="%m/%d/%Y"),
    'chapter_name': fields.String
})


@member_ns.route('/<int:id>')
@member_ns.response(404, 'Member not found')
@member_ns.param('id', 'Member identifier')
class Member(Resource):
    @member_ns.doc('get_member')
    def get(self, id):
        member_data = MemberModel.find_by_id(id)
        if member_data:
            return member_data.json()
        return {'message': MEMBER_NOT_FOUND}, 404

    @member_ns.doc('update_member')
    def put(self, id):
        member_data = MemberModel.find_by_id(id)
        member_json = request.get_json()

        new_member_data = {}

        new_member_data['first_name'] = member_data.first_name
        new_member_data['last_name'] = member_data.last_name
        new_member_data['email'] = member_data.email
        new_member_data['profile_image'] = member_data.profile_image
        new_member_data['dues_paid'] = member_data.dues_paid
        new_member_data['last_dues_payment'] = member_data.last_dues_payment
        new_member_data['chapter_name'] = member_data.chapter_name

        merged_member_data = new_member_data | member_json

        member_data.first_name = merged_member_data['first_name']
        member_data.last_name = merged_member_data['last_name']
        member_data.email = merged_member_data['email']
        member_data.profile_image = merged_member_data['profile_image']
        member_data.dues_paid = bool(merged_member_data['dues_paid'])
        member_data.last_dues_payment = datetime.datetime.strptime(
            merged_member_data['last_dues_payment'], '%m/%d/%Y').date()
        member_data.chapter_name = merged_member_data['chapter_name']

        member_data.save_to_db()
        return member_data.json, 200

    @member_ns.doc('delete_member')
    @member_ns.response(204, 'Member deleted')
    def delete(self, id):
        member_data = MemberModel.find_by_id(id)
        if member_data:
            member_data.delete_from_db()
            return {'message': "Member Deleted successfully"}, 204
        return {'message': MEMBER_NOT_FOUND}, 404


@members_ns.route('/')
class MemberList(Resource):
    @members_ns.doc('list_members')
    @member_ns.marshal_list_with(member)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('chapter_filter', type=str)
        parser.add_argument('sort_by', type=inputs.boolean)
        parser.add_argument('order', type=str)
        parser.add_argument('invert', type=inputs.boolean)
        args = parser.parse_args()

        member_list = []
        if args['chapter_filter']:
            member_list = MemberModel.find_by_chapter(args['chapter_filter'])
        elif args['sort_by']:
            member_list = MemberModel.find_all(args['order'], args['invert'])
        else:
            member_list = MemberModel.find_all()
        return member_list

    @members_ns.doc('create_member')
    def post(self):
        member_json = request.get_json()
        new_member = MemberModel(
            member_json['first_name'],
            member_json['last_name'],
            member_json['email'],
            member_json['profile_image'],
            bool(member_json['dues_paid']),
            datetime.datetime.strptime(
                member_json['last_dues_payment'], '%m/%d/%Y').date(),
            member_json['chapter_name']
        )
        new_member.save_to_db()

        return new_member.json(), 201


@viewer.route('/', methods=['GET', 'POST'])
def get_members():
    if request.method == 'GET':
        return render_template('members.html', members=MemberModel.find_all())
    elif request.method == 'POST':
        chapter_name = request.form['filter']
        return render_template('members.html', members=MemberModel.find_by_chapter(chapter_name))
