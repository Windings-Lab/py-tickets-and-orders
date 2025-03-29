from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


def create_order(
        tickets: list[dict[str, int]],
        username: str,
        date: str | None = None,
) -> None:
    with transaction.atomic():
        order = Order(
            user=User.objects.get(username=username),
        )
        order.save()
        if date:
            date = date.replace(" ", "T")
            order.created_at = datetime.fromisoformat(date)
            order.save()

        for ticket_dict in tickets:
            ticket_dict["movie_session_id"] = ticket_dict["movie_session"]
            ticket_dict.pop("movie_session")
            ticket = Ticket(**ticket_dict)
            ticket.order = order
            ticket.save()


def get_orders(username: str | None = None) -> QuerySet:
    query = Order.objects.all()
    if username:
        query = query.filter(user__username=username)

    return query
