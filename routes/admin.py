from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Quest, SystemSetting, UserQuest, User, Reward, UserReward
import os
import hashlib
import requests
from flask import current_app
from datetime import datetime

# Telethon (user client) for Option B
try:
    from telethon.sync import TelegramClient
    TELETHON_AVAILABLE = True
except Exception:
    TELETHON_AVAILABLE = False

admin_bp = Blueprint('admin', __name__)


def _detect_telegram_chat(chat_id, timeout=8):
    """Call Telegram getChat to determine type/title/username for a chat identifier.
    Returns a dict with keys: platform_type ('channel'|'group'), chat_title, chat_username
    or empty dict on failure.
    """
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN') or os.environ.get('BOT_TOKEN')
    if not bot_token or not chat_id:
        return {}
    try:
        get_chat_url = f'https://api.telegram.org/bot{bot_token}/getChat'
        resp = requests.get(get_chat_url, params={'chat_id': chat_id}, timeout=timeout)
        data = resp.json()
    except Exception:
        current_app.logger.exception('Failed to call Telegram getChat')
        return {}

    if not data or not data.get('ok'):
        current_app.logger.info('Telegram getChat returned not ok for %s: %s', chat_id, data)
        return {}

    result = data.get('result', {})
    t = result.get('type')
    if t in ('group', 'supergroup'):
        platform_type = 'group'
    elif t == 'channel':
        platform_type = 'channel'
    else:
        platform_type = t or None

    out = {}
    if platform_type:
        out['platform_type'] = platform_type
    if result.get('title'):
        out['chat_title'] = result.get('title')
    if result.get('username'):
        out['chat_username'] = result.get('username')

    return out


def _validate_image_url(url, timeout=5):
    """Return True if the URL points to an image (via HEAD or GET headers), False otherwise."""
    try:
        resp = requests.head(url, allow_redirects=True, timeout=timeout)
        if resp.status_code >= 400:
            raise ValueError(f'HEAD status {resp.status_code}')
        ctype = resp.headers.get('content-type', '')
        if ctype and ctype.split(';', 1)[0].strip().lower().startswith('image'):
            return True
    except Exception:
        try:
            resp = requests.get(url, stream=True, allow_redirects=True, timeout=timeout)
            if resp.status_code >= 400:
                return False
            ctype = resp.headers.get('content-type', '')
            return bool(ctype and ctype.split(';', 1)[0].strip().lower().startswith('image'))
        except Exception:
            return False
    return False


def _form_checkbox(form, name, default=True):
    """Interpret checkbox submissions that may include hidden fallback inputs."""
    try:
        values = form.getlist(name)
    except AttributeError:
        values = []
    if not values:
        return default
    truthy = {'1', 'true', 'on', 'yes', 'y', 'checked'}
    for value in values:
        if isinstance(value, str) and value.strip().lower() in truthy:
            return True
        if isinstance(value, (int, float)) and value == 1:
            return True
    return False

@admin_bp.route('/')
def dashboard():
    quests = Quest.query.order_by(Quest.id.desc()).all()
    quests_data = [q.to_dict() for q in quests]
    return render_template('admin_dashboard.html', quests=quests, quests_data=quests_data)

@admin_bp.route('/quest/add', methods=['POST'])
def add_quest():
    title = request.form.get('title')
    description = request.form.get('description')
    points = int(request.form.get('points'))
    platform = request.form.get('platform')
    category = request.form.get('category')
    action_url = request.form.get('action_url')
    verification_data = request.form.get('verification_data')
    starts_at_str = request.form.get('starts_at')
    expires_at_str = request.form.get('expires_at')
    
    # Parse start and expiration date if provided
    starts_at = None
    if starts_at_str:
        try:
            starts_at = datetime.fromisoformat(starts_at_str)
        except ValueError:
            starts_at = None

    expires_at = None
    if expires_at_str:
        try:
            expires_at = datetime.fromisoformat(expires_at_str)
        except ValueError:
            expires_at = None
    
    platform_config = {}
    if platform == 'telegram':
        use_bot_verification = _form_checkbox(request.form, 'telegram_bot_verify', default=True)
        platform_config['telegram_bot_verify'] = use_bot_verification
    # If platform-specific type provided (e.g., telegram group/channel)
    platform_type = request.form.get('platform_type')
    if platform_type:
        platform_config['platform_type'] = platform_type
    # store chat id if provided in verification_data for telegram
    if platform == 'telegram' and verification_data:
        platform_config['chat_id'] = verification_data

    # Attempt automatic detection of telegram chat type/title when possible
    if platform == 'telegram' and platform_config.get('chat_id'):
        try:
            detected = _detect_telegram_chat(platform_config['chat_id'])
            if detected:
                # do not override explicit form value
                if not platform_config.get('platform_type') and detected.get('platform_type'):
                    platform_config['platform_type'] = detected.get('platform_type')
                if detected.get('chat_title'):
                    platform_config['chat_title'] = detected.get('chat_title')
                if detected.get('chat_username'):
                    platform_config['chat_username'] = detected.get('chat_username')
        except Exception:
            current_app.logger.exception('Failed to auto-detect telegram chat for %s', platform_config.get('chat_id'))

    # Ensure a sensible default for telegram platform_type when missing
    if platform == 'telegram' and (not platform_config.get('platform_type')):
        platform_config['platform_type'] = 'channel'

    # Admin-provided image URL (store the URL directly, validate with HEAD)
    image_url_form = request.form.get('image_url')
    if image_url_form and image_url_form.strip():
        img = image_url_form.strip()
        # ensure platform_config exists
        if not platform_config:
            platform_config = {}
        platform_config['image'] = img
        try:
            is_img = _validate_image_url(img)
            platform_config['image_valid'] = bool(is_img)
            if not is_img:
                current_app.logger.warning('Image URL did not validate as image: %s', img)
        except Exception:
            platform_config['image_valid'] = False
            current_app.logger.exception('Error validating image URL: %s', img)

    quest = Quest(
        title=title,
        description=description,
        points=points,
        quest_type=platform,
        category=category,
        action_url=action_url,
        verification_data=verification_data,
        verification_code=request.form.get('verification_code') or None,
        starts_at=starts_at,
        expires_at=expires_at,
        is_active=True
    )
    if platform_config:
        quest.platform_config = platform_config
    
    db.session.add(quest)
    db.session.commit()
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/quest/edit/<int:quest_id>', methods=['POST'])
def edit_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    
    quest.title = request.form.get('title')
    quest.description = request.form.get('description')
    quest.points = int(request.form.get('points'))
    quest.quest_type = request.form.get('platform')
    quest.category = request.form.get('category')
    quest.action_url = request.form.get('action_url')
    quest.verification_data = request.form.get('verification_data')
    # Save verification_code (used for YouTube quests)
    quest.verification_code = request.form.get('verification_code') or None
    # Work with a copy of platform_config so SQLAlchemy notices changes reliably
    current_config = {}
    if quest.platform_config and isinstance(quest.platform_config, dict):
        current_config = dict(quest.platform_config)
    # Platform-specific type
    platform_type = request.form.get('platform_type')
    if platform_type:
        current_config['platform_type'] = platform_type
    if quest.quest_type == 'telegram':
        default_bot_setting = True
        if current_config:
            default_bot_setting = current_config.get('telegram_bot_verify', True)
        use_bot_verification = _form_checkbox(request.form, 'telegram_bot_verify', default=default_bot_setting)
        current_config['telegram_bot_verify'] = use_bot_verification
    elif quest.platform_config:
        current_config.pop('telegram_bot_verify', None)
    # If saving a telegram quest and no platform_type provided, default to 'channel'
    if quest.quest_type == 'telegram' and not current_config.get('platform_type'):
        current_config['platform_type'] = 'channel'
    # update chat id if provided
    if quest.quest_type == 'telegram' and request.form.get('verification_data'):
        current_config['chat_id'] = request.form.get('verification_data')

    # Attempt automatic detection of telegram chat type/title when possible (do not override explicit form)
    if quest.quest_type == 'telegram' and current_config.get('chat_id'):
        try:
            detected = _detect_telegram_chat(current_config['chat_id'])
            if detected:
                if not current_config.get('platform_type') and detected.get('platform_type'):
                    current_config['platform_type'] = detected.get('platform_type')
                if detected.get('chat_title'):
                    current_config['chat_title'] = detected.get('chat_title')
                if detected.get('chat_username'):
                    current_config['chat_username'] = detected.get('chat_username')
        except Exception:
            current_app.logger.exception('Failed to auto-detect telegram chat for %s', current_config.get('chat_id'))
    
    expires_at_str = request.form.get('expires_at')
    if expires_at_str:
        try:
            quest.expires_at = datetime.fromisoformat(expires_at_str)
        except ValueError:
            quest.expires_at = None
    else:
        quest.expires_at = None
    # parse optional start date
    starts_at_str = request.form.get('starts_at')
    if starts_at_str:
        try:
            quest.starts_at = datetime.fromisoformat(starts_at_str)
        except ValueError:
            quest.starts_at = None
    else:
        # if not provided, leave existing value or None
        pass
    # Admin-provided image URL only: store URL directly (no download)
    image_url_form = request.form.get('image_url')
    if image_url_form and image_url_form.strip():
        img = image_url_form.strip()
        current_config['image'] = img
        try:
            is_img = _validate_image_url(img)
            current_config['image_valid'] = bool(is_img)
            if not is_img:
                current_app.logger.warning('Image URL did not validate as image: %s', img)
        except Exception:
            current_config['image_valid'] = False
            current_app.logger.exception('Error validating image URL: %s', img)

    # Assign back the possibly updated configuration
    quest.platform_config = current_config if current_config else None

    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/quest/fetch_telegram_image/<int:quest_id>', methods=['POST'])
def fetch_telegram_image(quest_id):
    """Fetch chat/channel photo from Telegram and save to static/images.
    Expects the quest to have `platform_config.chat_id` or `verification_data` containing the chat identifier (e.g., @channelusername or -1001234567890).
    """
    quest = Quest.query.get_or_404(quest_id)
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN') or os.environ.get('BOT_TOKEN')
    if not bot_token:
        current_app.logger.error('Telegram bot token missing')
        return jsonify({'success': False, 'error': 'Telegram bot token not configured.'}), 400

    # Accept chat_id from JSON body, form data, or query param; fallback to quest.platform_config or verification_data
    body = {}
    try:
        body = request.get_json(silent=True) or {}
    except Exception:
        body = {}

    chat_id = body.get('chat_id') or request.form.get('chat_id') or request.args.get('chat_id')
    if not chat_id and quest.platform_config and isinstance(quest.platform_config, dict):
        chat_id = quest.platform_config.get('chat_id')
    if not chat_id:
        chat_id = quest.verification_data or quest.action_url
    if not chat_id:
        current_app.logger.error('No chat identifier provided for quest %s', quest_id)
        return jsonify({'success': False, 'error': 'No chat identifier found on quest.'}), 400

    current_app.logger.info('Fetching Telegram chat info for chat_id=%s (quest=%s)', chat_id, quest_id)

    # Call getChat
    get_chat_url = f'https://api.telegram.org/bot{bot_token}/getChat'
    try:
        resp = requests.get(get_chat_url, params={'chat_id': chat_id}, timeout=10)
        data = resp.json()
    except Exception as e:
        current_app.logger.exception('Failed to contact Telegram API getChat')
        return jsonify({'success': False, 'error': f'Failed to contact Telegram API: {e}'}), 500

    if not data or not data.get('ok'):
        desc = data.get('description') if isinstance(data, dict) else 'no response'
        current_app.logger.error('Telegram getChat failed: %s', desc)
        return jsonify({'success': False, 'error': f'Telegram API error: {desc}'}), 400

    chat = data.get('result', {})
    photo = chat.get('photo')
    if not photo:
        current_app.logger.info('Chat has no photo for chat_id=%s', chat_id)
        return jsonify({'success': False, 'error': 'Chat has no profile photo.'}), 400

    # prefer big_file_id
    file_id = photo.get('big_file_id') or photo.get('small_file_id')
    if not file_id:
        current_app.logger.error('No file_id for chat photo for chat_id=%s', chat_id)
        return jsonify({'success': False, 'error': 'No file_id available for chat photo.'}), 400

    # getFile
    get_file_url = f'https://api.telegram.org/bot{bot_token}/getFile'
    try:
        resp2 = requests.get(get_file_url, params={'file_id': file_id}, timeout=10)
        file_data = resp2.json()
    except Exception as e:
        current_app.logger.exception('Failed to call getFile')
        return jsonify({'success': False, 'error': f'Failed to get file info: {e}'}), 500

    if not file_data or not file_data.get('ok'):
        desc = file_data.get('description') if isinstance(file_data, dict) else 'no response'
        current_app.logger.error('Telegram getFile failed: %s', desc)
        return jsonify({'success': False, 'error': f'Telegram API getFile error: {desc}'}), 400

    file_path = file_data.get('result', {}).get('file_path')
    if not file_path:
        current_app.logger.error('No file_path in getFile result for chat_id=%s', chat_id)
        return jsonify({'success': False, 'error': 'No file path returned by Telegram.'}), 400

    file_url = f'https://api.telegram.org/file/bot{bot_token}/{file_path}'
    try:
        fresp = requests.get(file_url, timeout=15)
        fresp.raise_for_status()
        content = fresp.content
    except Exception as e:
        current_app.logger.exception('Failed to download file from Telegram')
        return jsonify({'success': False, 'error': f'Failed to download file: {e}'}), 500

    # compute hash to avoid duplicates
    sha = hashlib.sha256(content).hexdigest()
    _, ext = os.path.splitext(file_path)
    if not ext:
        ext = '.jpg'

    images_dir = os.path.join(current_app.root_path, 'static', 'images')
    os.makedirs(images_dir, exist_ok=True)
    filename = f'telegram_{sha}{ext}'
    filepath = os.path.join(images_dir, filename)

    # if file doesn't exist, write
    if not os.path.exists(filepath):
        with open(filepath, 'wb') as fh:
            fh.write(content)

    # save relative url to quest.platform_config
    if not quest.platform_config or not isinstance(quest.platform_config, dict):
        quest.platform_config = {}
    # allow platform_type via JSON body or existing config
    body = {}
    try:
        body = request.get_json(force=False) or {}
    except Exception:
        body = {}
    quest.platform_config['platform_type'] = quest.platform_config.get('platform_type', body.get('platform_type') or request.form.get('platform_type') or 'channel')
    quest.platform_config['image'] = f'/static/images/{filename}'
    db.session.commit()

    return jsonify({'success': True, 'image_url': quest.platform_config['image']})


@admin_bp.route('/quest/fetch_telegram_image_telethon/<int:quest_id>', methods=['POST'])
def fetch_telegram_image_telethon(quest_id):
    """Fetch chat photo using a Telegram user client (Telethon).
    This requires API_ID and API_HASH in env and first-run sign-in to create a session file.
    """
    if not TELETHON_AVAILABLE:
        return jsonify({'success': False, 'error': 'Telethon not installed on the server.'}), 500

    quest = Quest.query.get_or_404(quest_id)

    # Accept chat_id from JSON body, form, or fallback to quest fields
    body = request.get_json(silent=True) or {}
    chat_id = body.get('chat_id') or request.form.get('chat_id') or request.args.get('chat_id')
    if not chat_id and quest.platform_config and isinstance(quest.platform_config, dict):
        chat_id = quest.platform_config.get('chat_id')
    if not chat_id:
        chat_id = quest.verification_data or quest.action_url
    if not chat_id:
        return jsonify({'success': False, 'error': 'No chat identifier found on quest.'}), 400

    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    if not api_id or not api_hash:
        return jsonify({'success': False, 'error': 'API_ID/API_HASH not configured in environment.'}), 500

    # session file path (stored in instance or project root)
    session_name = os.path.join(current_app.instance_path or current_app.root_path, f'telethon_session')
    os.makedirs(os.path.dirname(session_name), exist_ok=True)

    try:
        client = TelegramClient(session_name, int(api_id), api_hash)
    except Exception as e:
        current_app.logger.exception('Failed to create TelegramClient')
        return jsonify({'success': False, 'error': f'Failed to initialize Telegram client: {e}'}), 500

    try:
        # Avoid calling client.start() on the server (it may prompt interactively).
        # Instead connect and check authorization. If not authorized, return instructive error.
        client.connect()
        if not client.is_user_authorized():
            current_app.logger.warning('Telethon session not authorized; interactive sign-in required')
            return jsonify({'success': False, 'error': 'Telethon session not signed in. Run scripts/telethon_signin.py interactively to create a session.'}), 500
    except Exception as e:
        current_app.logger.exception('Telethon connect/start failed')
        return jsonify({'success': False, 'error': f'Telethon connect/start failed: {e}'}), 500

    try:
        # get entity and download profile photo
        entity = client.get_entity(chat_id)
    except Exception as e:
        current_app.logger.exception('Failed to get entity for %s', chat_id)
        return jsonify({'success': False, 'error': f'Failed to resolve chat: {e}'}), 400

    try:
        # download_profile_photo returns path on disk when file param is a path
        images_dir = os.path.join(current_app.root_path, 'static', 'images')
        os.makedirs(images_dir, exist_ok=True)

        # use temporary name first; Telethon saves original extension
        tmp_path = os.path.join(images_dir, f'telegram_tmp_{quest_id}')
        saved_path = client.download_profile_photo(entity, file=tmp_path)
        if not saved_path:
            return jsonify({'success': False, 'error': 'No profile photo available for this chat.'}), 400

        # read content and compute sha
        with open(saved_path, 'rb') as fh:
            content = fh.read()
        sha = hashlib.sha256(content).hexdigest()
        _, ext = os.path.splitext(saved_path)
        ext = ext if ext else '.jpg'
        filename = f'telegram_{sha}{ext}'
        final_path = os.path.join(images_dir, filename)
        if not os.path.exists(final_path):
            # move temporary file to final path
            os.replace(saved_path, final_path)
        else:
            # remove temporary saved_path if duplicate
            try:
                os.remove(saved_path)
            except Exception:
                pass

        # update quest.platform_config
        if not quest.platform_config or not isinstance(quest.platform_config, dict):
            quest.platform_config = {}
        quest.platform_config['image'] = f'/static/images/{filename}'
        quest.platform_config['chat_id'] = chat_id
        # preserve/overwrite platform_type if provided in body
        if body.get('platform_type'):
            quest.platform_config['platform_type'] = body.get('platform_type')
        db.session.commit()

        return jsonify({'success': True, 'image_url': quest.platform_config['image']})
    except Exception as e:
        current_app.logger.exception('Failed to download or process profile photo')
        return jsonify({'success': False, 'error': f'Failed to download/process photo: {e}'}), 500

@admin_bp.route('/quest/delete/<int:quest_id>', methods=['POST'])
def delete_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    db.session.delete(quest)
    db.session.commit()
    return jsonify({'status': 'success'})

@admin_bp.route('/quest/toggle/<int:quest_id>', methods=['POST'])
def toggle_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    quest.is_active = not quest.is_active
    db.session.commit()
    return jsonify({'success': True})

# Verification Queue Routes
@admin_bp.route('/verification-queue')
def verification_queue():
    # Get all submitted quests pending review
    pending_submissions = db.session.query(UserQuest, User, Quest).join(
        User, UserQuest.user_id == User.id
    ).join(
        Quest, UserQuest.quest_id == Quest.id
    ).filter(
        UserQuest.status == 'submitted'
    ).order_by(
        UserQuest.submitted_at.desc()
    ).all()
    
    return render_template('verification_queue.html', submissions=pending_submissions)

@admin_bp.route('/verify/approve/<int:submission_id>', methods=['POST'])
def approve_submission(submission_id):
    submission = UserQuest.query.get_or_404(submission_id)
    quest = Quest.query.get(submission.quest_id)
    user = User.query.get(submission.user_id)
    
    # Update submission status
    submission.status = 'approved'
    submission.completed_at = datetime.utcnow()
    submission.reviewed_at = datetime.utcnow()
    # Note: reviewed_by would need admin user ID - for now we'll leave it null
    
    # Award points to user
    user.points += quest.points
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Submission approved'})

@admin_bp.route('/verify/reject/<int:submission_id>', methods=['POST'])
def reject_submission(submission_id):
    submission = UserQuest.query.get_or_404(submission_id)
    
    # Update submission status
    submission.status = 'rejected'
    submission.reviewed_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Submission rejected'})

# ===== REWARD MANAGEMENT ROUTES =====

@admin_bp.route('/rewards')
def manage_rewards():
    """Admin reward management page"""
    rewards = Reward.query.all()
    rewards_data = [r.to_dict() for r in rewards]
    return render_template('admin_rewards.html', rewards=rewards, rewards_data=rewards_data)

@admin_bp.route('/rewards/add', methods=['POST'])
def add_reward():
    """Create a new reward"""
    title = request.form.get('title')
    description = request.form.get('description')
    cost = int(request.form.get('cost'))
    image_url = request.form.get('image_url')
    category = request.form.get('category')
    stock_str = request.form.get('stock')
    
    # Parse stock (empty = unlimited)
    stock = None
    if stock_str and stock_str.strip():
        stock = int(stock_str)
    
    reward = Reward(
        title=title,
        description=description,
        cost=cost,
        image_url=image_url,
        category=category,
        stock=stock,
        is_active=True
    )
    
    db.session.add(reward)
    db.session.commit()
    
    return redirect(url_for('admin.manage_rewards'))

@admin_bp.route('/rewards/edit/<int:reward_id>', methods=['POST'])
def edit_reward(reward_id):
    """Edit an existing reward"""
    reward = Reward.query.get_or_404(reward_id)
    
    reward.title = request.form.get('title')
    reward.description = request.form.get('description')
    reward.cost = int(request.form.get('cost'))
    reward.image_url = request.form.get('image_url')
    reward.category = request.form.get('category')
    
    stock_str = request.form.get('stock')
    reward.stock = int(stock_str) if stock_str and stock_str.strip() else None
    
    db.session.commit()
    
    return redirect(url_for('admin.manage_rewards'))

@admin_bp.route('/rewards/toggle/<int:reward_id>', methods=['POST'])
def toggle_reward(reward_id):
    """Toggle reward active status"""
    reward = Reward.query.get_or_404(reward_id)
    reward.is_active = not reward.is_active
    db.session.commit()
    return jsonify({'success': True})

@admin_bp.route('/rewards/delete/<int:reward_id>', methods=['POST'])
def delete_reward(reward_id):
    """Delete a reward"""
    reward = Reward.query.get_or_404(reward_id)
    db.session.delete(reward)
    db.session.commit()
    return jsonify({'success': True})
