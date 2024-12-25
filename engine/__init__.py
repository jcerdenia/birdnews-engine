from service import ai_service, checklist_service, content_service, email_service

from .engine import Engine


def get_engine():
    return Engine(
        ai_service,
        checklist_service,
        content_service,
        email_service,
    )


def main():
    engine = get_engine()
    engine.run()
