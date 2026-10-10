# PersonalDairyforVisualImpared/Model/__init__.py
# This file imports all models in the correct order to handle dependencies

# 1. Import base models (No foreign keys)
from PersonalDiaryforVisualImpared.Model.User import User
from PersonalDiaryforVisualImpared.Model.Quran_Audio import Quran_Audio
from PersonalDiaryforVisualImpared.Model.Event import Event

# 2. Import models depending on User
from PersonalDiaryforVisualImpared.Model.Query import Query
from PersonalDiaryforVisualImpared.Model.Reminders import Reminders
from PersonalDiaryforVisualImpared.Model.Attachments import Attachments
from PersonalDiaryforVisualImpared.Model.Item_location import Item_location
from PersonalDiaryforVisualImpared.Model.Detail_event import Detail_event

# 3. Import associative models with multiple dependencies
from PersonalDiaryforVisualImpared.Model.Play import Play
from PersonalDiaryforVisualImpared.Model.Attend import Attend

__all__ = [
    'User',
    'Query',
    'Reminders',
    'Attachments',
    'Item_location',
    'Quran_Audio',
    'Play',
    'Event',
    'Detail_event',
    'Attend'
]