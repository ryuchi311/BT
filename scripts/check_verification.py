import os
import sys

# Ensure project root is on sys.path so imports like `import app` work when running from scripts/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import Quest, UserQuest, db

code_to_check = 'hidden123'

with app.app_context():
    print('Looking up quest id=8 (common test id)')
    q8 = Quest.query.filter_by(id=8).first()
    if q8:
        print(f'Quest id=8 -> title="{q8.title}" verification_code={q8.verification_code}')
    else:
        print('No quest with id=8 found.')

    print('\nLooking for any quest with code exactly "{}"...'.format(code_to_check))
    match = Quest.query.filter(Quest.verification_code == code_to_check).limit(10).all()
    if not match:
        print('No quest found with that verification code.')
    else:
        for q in match:
            print(f'Found matching quest id={q.id} title="{q.title}"')
            uqs = UserQuest.query.filter_by(quest_id=q.id).all()
            if not uqs:
                print('  No user submissions for this quest yet.')
            else:
                for uq in uqs:
                    print(f'  UserQuest id={uq.id} user_id={uq.user_id} status={uq.status} submitted_at={uq.submitted_at}')

    print('\nAlso dumping all quests (id, title, verification_code) for manual check:')
    allq = Quest.query.order_by(Quest.id).all()
    for q in allq:
        print(f'id={q.id} | title="{q.title}" | code={q.verification_code}')
