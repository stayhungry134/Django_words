# 设置虚拟环境路径
VIRTUALENV_PATH="/root/program/python/env/django_words"

# 检查虚拟环境是否存在
if [ ! -d "$VIRTUALENV_PATH" ]; then
    echo "虚拟环境路径不存在：$VIRTUALENV_PATH"
    exit 1
fi

# 激活虚拟环境
source "$VIRTUALENV_PATH/bin/activate"

# shellcheck disable=SC2164
cd "/var/www/backend/django_words/uwsgi"
uwsgi --ini django_words.ini
# shellcheck disable=SC2164
cd "/var/www/backend/django_words"
nohup celery -A django_words worker -l info >> log/celery.log 2>&1 &
nohup celery -A django_words beat -l info >> log/beat.log 2>&1 &
