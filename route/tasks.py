from root.celery import app
from route.services.suggest_like import SuggestLike


@app.task
def update_suggest_count():
    SuggestLike.fetch_like()
