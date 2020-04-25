from datetime import datetime
from celery.schedules import crontab

from .. import celery


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Register task to run periodically."""
    # Trigger Celery beat to delete records every minutes.
    sender.add_periodic_task(crontab(minute="*/1"), delete_expired_links.s())


@celery.task
def delete_expired_links():
    """Delete expired links from the database."""
    db.session.query(Slugs).filter(date_expires > datetime.now()).delete()
    db.session.commit()
