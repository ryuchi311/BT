from app import app, db
from models import Reward

with app.app_context():
    rewards = Reward.query.all()
    print(f"Found {len(rewards)} rewards:")
    for r in rewards:
        print(f"ID: {r.id}, Title: {r.title}, Cost: {r.cost}, Stock: {r.stock}, Active: {r.is_active}")
