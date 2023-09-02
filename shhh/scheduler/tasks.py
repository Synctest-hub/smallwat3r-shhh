import logging
from datetime import datetime

from shhh.constants import ClientType
from shhh.domain import model
from shhh.extensions import db, scheduler
from shhh.liveness import db_liveness_ping

logger = logging.getLogger("tasks")


@db_liveness_ping(ClientType.TASK)
def delete_expired_links() -> None:
    """Delete expired secrets from the database."""
    app = scheduler.app
    with app.app_context():
        expired_secrets = db.session.query(model.Secret).filter(
            model.Secret.date_expires <= datetime.now()).all()  # type: ignore
        _delete_records(expired_secrets)
        logger.info("%s expired records have been deleted.",
                    len(expired_secrets))


def _delete_records(records: list[model.Secret]) -> None:
    for record in records:
        db.session.delete(record)
        db.session.commit()
