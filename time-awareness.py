"""
title: Time Awareness
author: Roni Laukkarinen
description: Time Awareness for AI.
repository_url: https://www.openwebui.com/f/abhiraaid/time_awareness
version: 0.2.0
required_open_webui_version: >= 0.5.0
"""

import time
import sys
import datetime
import logging
import functools
import inspect
import zoneinfo
import uuid
import bs4
from bs4 import BeautifulSoup
import re


def set_logs(logger: logging.Logger, level: int, force: bool = False):
    logger.setLevel(level)
    for handler in logger.handlers:
        if not force and isinstance(handler, logging.StreamHandler):
            handler.setLevel(level)
            return
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(levelname)s[%(name)s]%(lineno)s:%(asctime)s: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


LOGGER: logging.Logger = logging.getLogger("FUNC:TIME_AWARENESS")
set_logs(LOGGER, logging.INFO)


def log_exceptions(func):
    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def _wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as exc:
                LOGGER.error("Error in %s: %s", func, exc, exc_info=True)
                raise exc

    else:

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                LOGGER.error("Error in %s: %s", func, exc, exc_info=True)
                raise exc

    return _wrapper


class ROLE:
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Filter:
    class Valves:
        def __init__(self, timezone=None, priority=-10):
            self.timezone = timezone or time.tzname[0]
            self.priority = priority

    class UserValves:
        def __init__(self, timezone=None, enabled=True):
            self.timezone = timezone or time.tzname[0]
            self.enabled = enabled

    CONTEXT_ID = "time_awareness"

    def __init__(self):
        self.valves = self.Valves()
        self.uservalves = self.UserValves()
        self._queries = {}

    async def get_time_context(
        self,
        timestamp: int = None,
        variables: dict = None,
        __event_emitter__=None,
        user: dict = None,
    ):
        tz = self.valves.timezone
        comment = "System timezone"
        if variables is not None and variables.get("{{CURRENT_TIMEZONE}}"):
            tz = variables["{{CURRENT_TIMEZONE}}"]
        if user is not None:
            usertz = user.get("valves", {}).get("timezone", "").strip()
            if usertz:
                tz = usertz
                comment = (
                    "Timezone provided by user. User location most likely different"
                )
        if tz not in zoneinfo.available_timezones():
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"Unknown timezone: {tz}.",
                            "done": True,
                        },
                    }
                )
        format = "%a %d %b %Y, %H:%M:%S"
        timezone = zoneinfo.ZoneInfo(tz)
        if timestamp is None:
            date = datetime.datetime.now(tz=timezone)
        else:
            date = datetime.datetime.fromtimestamp(timestamp, tz=timezone)
        date_str = date.strftime(format)
        context = f'<time timezone="{tz}" format="{format}"><!-- {comment} -->{date_str}</time>'
        return context

    @log_exceptions
    async def inlet(
        self,
        body: dict,
        __event_emitter__,
        user: dict = None,
    ) -> dict:
        if user is not None:
            if not user.get("valves", {}).get("enabled", True):
                return body
        messages = body.get("messages")
        if not messages:
            return body
        context = await self.get_time_context(
            __event_emitter__=__event_emitter__,
            user=user,
            variables=body.get("metadata", {}).get("variables", {}),
        )
        user_message, user_message_ind = get_last_message(messages, ROLE.USER)
        if user_message_ind is None or user_message is None:
            return body
        if "message_id" in body.get("metadata", {}):
            query_id = body["metadata"]["message_id"]
            self._queries[query_id] = {"context": context, "timestamp": time.time()}
        user_message["content"] = add_or_update_filter_context(
            user_message["content"], context, id=self.CONTEXT_ID
        )
        if user is None:
            return body
        if "id" not in user:
            return body
        return body

    @log_exceptions
    async def outlet(
        self,
        body: dict,
        __event_emitter__,
        user: dict = None,
    ) -> dict:
        answer_id = body.get("id")
        session_id = body.get("session_id")
        chat_id = body.get("chat_id")
        messages = body.get("messages")
        user_id = user.get("id") if user else None
        if None in (answer_id, session_id, chat_id, messages, user_id):
            return body
        user_msg, user_msg_ind = get_last_message(messages, ROLE.USER)
        query = self._queries.get(answer_id)
        if not query:
            return body
        user_msg["content"] = add_or_update_filter_context(
            user_msg["content"], query["context"], self.CONTEXT_ID
        )
        return body


def get_last_message(messages, role):
    for i, m in enumerate(reversed(messages)):
        if m.get("role") == role:
            return (m, len(messages) - i - 1)
    return (None, None)


def add_or_update_filter_context(
    message,
    context: str,
    id: str,
    selector: str = "details[type=filters_context]",
    container: str = (
        '<details type="filters_context">'
        "\n<summary>Filters context</summary>\n"
        "<!--This context was added by the system to this message, not by the user. "
        "**Important:** Never say timezone out loud, it is unncessary information for the user. Never say seconds, unless needed. You do not need to tell the time unless asked. If the time is asked, tell only time. If the date is asked or related to the question, consider the whole date and time. Times always in 24h format. Message sent on: -->"
        '\n{content}\n<!-- User message will follow "details" closing tag. --></details>\n'
    ),
) -> str:
    # Handle multimodal content (list of content objects)
    if isinstance(message, list):
        # Extract only text content for processing
        text_content = ""
        for content in message:
            if isinstance(content, dict) and content.get("type") == "text":
                text_content += content.get("text", "")
        message = text_content

    # Ensure message is a string
    if not isinstance(message, str):
        message = str(message)

    soup = BeautifulSoup(message, "xml")
    details_match = soup.select(selector)
    context_end = "context_end"
    context_str = f'<context id="{id}">{context}</context>'
    if not len(details_match):
        out_soup = BeautifulSoup(container.format(content=context_str), "xml").contents[
            0
        ]
        out_soup.append(
            BeautifulSoup(
                f'<{context_end} uuid="{str(uuid.uuid4())}"/>', "xml"
            ).contents[0]
        )
        return "\n".join((str(out_soup), message))
    elif len(details_match) > 1:
        raise ValueError("Ill-formed message: more than one container found.")
    else:
        details = details_match[0]
        user_msg = _remove_context(
            message, details, container=container, context_end=context_end
        )
        context_soup = BeautifulSoup(context_str, "xml").contents[0]
        same_ids = details.select(f"context[id={id}]")
        if len(same_ids) > 1:
            raise ValueError(f"More than one context found with the id {id}. Abort.")
        elif len(same_ids) == 1:
            elt = same_ids[0]
            elt.replace_with(context_soup)
        else:
            details.insert(-1, context_soup)
        return "\n".join((str(soup.contents[0]), user_msg))


def _remove_context(message: str, details: bs4.Tag, container: str, context_end: str):
    end_uuid: str = None
    for child in details:
        if getattr(child, "name", None) == context_end:
            end_uuid = child.get("uuid")
    if end_uuid is None:
        raise ValueError("Ill-formed prior context: no context_end uuid found. Abort.")
    uuid_ind = message.index(end_uuid)
    match = re.search(r"(</.*>)\s*$", container)
    if match is None:
        raise ValueError(
            "Ill-formed container: no closing tag found prior to EOF. Abort."
        )
    closing_tag = match.groups()[0]
    closing_tag_ind = message.index(closing_tag, uuid_ind)
    user_msg = message[closing_tag_ind + len(closing_tag) :]
    return user_msg
