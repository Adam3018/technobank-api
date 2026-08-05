"""
CRUD operations
"""

from .conference import (
    get_conference,
    get_conferences,
    create_conference,
    update_conference,
    delete_conference,
)
from .email_template import (
    get_email_template,
    get_email_templates,
    create_email_template,
    update_email_template,
    send_emails,
    delete_email_template,
)
from .visitor import (
    get_visitor,
    get_visitors,
    create_visitor,
    update_visitor,
    delete_visitor,
)

__all__ = [
    "get_conference",
    "get_conferences",
    "create_conference",
    "update_conference",
    "delete_conference",
    "get_email_template",
    "get_email_templates",
    "create_email_template",
    "update_email_template",
    "delete_email_template",
    "get_visitor",
    "get_visitors",
    "create_visitor",
    "update_visitor",
    "delete_visitor",
]
