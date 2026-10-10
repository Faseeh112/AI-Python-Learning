from flask import request, jsonify
from PersonalDiaryforVisualImpared.db import db, app
from flask_cors import CORS
# IMPORT CONTROLLERS - Names updated to match your snake_case filenames
from PersonalDiaryforVisualImpared.Controller.User import UserController
from PersonalDiaryforVisualImpared.Controller.Item_location import ItemLocationController
from PersonalDiaryforVisualImpared.Controller.Event import EventController
from PersonalDiaryforVisualImpared.Controller.Detail_event import  DetailEventController
from PersonalDiaryforVisualImpared.Controller.Reminders import ReminderController
from PersonalDiaryforVisualImpared.Controller.Play import PlayController
from PersonalDiaryforVisualImpared.Controller.Attachments import AttachmentsController

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


@app.route('/signup', methods=['POST'])
def signup():
    return UserController.signup()

@app.route('/login', methods=['POST'])
def login_user():
    return UserController.login()

@app.route('/user/change-password/<int:user_id>', methods=['PUT'])
def change_password(user_id):
    return UserController.change_password(user_id)

@app.route('/event/add', methods=['POST'])
def add_event():
    return EventController.add_event()

@app.route('/event/update/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    return EventController.update_event(event_id)

@app.route('/event/delete/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    return EventController.delete_event(event_id)

@app.route('/reminder/add', methods=['POST'])
def add_reminder():
    return ReminderController.add_reminder()

@app.route('/remainder/delete/<int:rem_id>', methods=['DELETE'])
def delete_remainder(rem_id):
    return ReminderController.delete_reminder(rem_id)

@app.route('/event/detail/add', methods=['POST'])
def add_detail_event():
    return DetailEventController.add_detail_event()

@app.route('/event/detail/update/<int:detail_id>', methods=['PUT'])
def update_detailevent(detail_id):
    return DetailEventController.update_detail_event(detail_id)

@app.route('/event/detail/delete/<int:detail_id>', methods=['DELETE'])
def delete_detailevent(detail_id):
    return DetailEventController.delete_detail_event(detail_id)

@app.route('/quran_play/add', methods=['POST'])
def add_play():
    return PlayController.add_play_audio()

@app.route('/quran_play/update/<int:play_id>', methods=['PUT'])
def update_play(play_id):
    return PlayController.update_play_audio(play_id)

@app.route('/quran_play/delete/<int:play_id>', methods=['DELETE'])
def delete_play(play_id):
    return PlayController.delete_play_audio(play_id)

@app.route('/reminder/update/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    return ReminderController.update_reminder(reminder_id)

@app.route('/reminder/sort_date/<int:user_id>', methods=['GET'])
def sort_reminder(user_id):
    return ReminderController.get_reminders_sorted(user_id)

@app.route('/attachment/add', methods=['POST'])
def attach_add():
    return AttachmentsController.upload_attachment()

@app.route('/attachment/update/<int:attac_id>', methods=['PuT'])
def attach_update(attac_id):
    return AttachmentsController.upload_attachment(attac_id)

@app.route('/attachment/delete/<int:attac_id>', methods=['DELETE'])
def delete_attachment(attac_id):
    return AttachmentsController.delete_attachment(attac_id)

@app.route('/itemlocation/add', methods=['POST'])
def item_add():
    return ItemLocationController.add_location()

@app.route('/itemlocation/update/<int:loc_id>', methods=['PUT'])
def item_update(loc_id):
    return ItemLocationController.update_location(loc_id)

@app.route('/itemlocation/delete/<int:loc_id>', methods=['DELETE'])
def delete_location(loc_id):
    return ItemLocationController.delete_location(loc_id)

if __name__ == '__main__':
    with app.app_context():
        print("Note: Not creating tables (they already exist in database)")
        print("Connected to existing database")
    app.run(debug=True)