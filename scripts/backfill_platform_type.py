import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models import Quest, db

if __name__ == '__main__':
    updated = 0
    with app.app_context():
        qs = Quest.query.filter(Quest.quest_type == 'telegram').all()
        for q in qs:
            pc = q.platform_config or {}
            # platform_config may be a string in some broken rows; ensure dict
            if not isinstance(pc, dict):
                try:
                    import json
                    pc = json.loads(pc)
                except Exception:
                    pc = {}
            if not pc.get('platform_type'):
                pc['platform_type'] = 'channel'
                q.platform_config = pc
                db.session.add(q)
                updated += 1
        if updated:
            db.session.commit()
    print(f'Backfilled platform_type for {updated} Telegram quests')
