# Visual_Impired_Diary/Model/__init__.py
# This file imports all models in the correct order

# First import base models (no foreign keys)
from Visual_Impired_Diary.Model.QuranAudio import QuranAudio
from Visual_Impired_Diary.Model.Event import Event
from Visual_Impired_Diary.Model.User import User

# Then import models that depend on the above
from Visual_Impired_Diary.Model.Reminders import Reminders
from Visual_Impired_Diary.Model.Attachments import Attachments
from Visual_Impired_Diary.Model.ItemLocation import ItemLocation
from Visual_Impired_Diary.Model.DetailEvent import DetailEvent

# Finally import models with multiple dependencies
from Visual_Impired_Diary.Model.Play import Play
from Visual_Impired_Diary.Model.Attend import Attend

__all__ = [
    'User',
    'Reminders',
    'Attachments',
    'ItemLocation',
    'Play',
    'Attend',
    'Event',
    'DetailEvent',
    'QuranAudio'
]