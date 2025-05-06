from sqlalchemy import Column, DateTime, TIMESTAMP

from app.models.common import utcnow


class TimeStampMixin(object):
    created_at = Column(TIMESTAMP(timezone=True), default=utcnow(), nullable=True)
    updated_at = Column(
        TIMESTAMP(timezone=True), default=utcnow(), onupdate=utcnow(), nullable=True
    )
