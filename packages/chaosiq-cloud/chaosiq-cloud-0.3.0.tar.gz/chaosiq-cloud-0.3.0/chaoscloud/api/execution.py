# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any, List, NoReturn, Optional
import uuid

from chaoslib.types import Configuration, Experiment, Extension, Journal, \
    Secrets, Settings
from chaostoolkit import encoder as json_encoder
from cloudevents.sdk import converters
from cloudevents.sdk import marshaller
from cloudevents.sdk.converters import structured
from cloudevents.sdk.event import v02
from logzero import logger
from requests import Response, Session
import simplejson as json
from tzlocal import get_localzone

from . import urls

__all__ = ["publish_event", "initialize_execution", "publish_execution",
           "fetch_execution"]


def initialize_execution(session: Session, experiment: Experiment,
                         journal: Journal) -> Optional[Response]:
    """
    Initialize the execution payload and send it over.
    """
    experiment_id = get_experiment_id(experiment.get('extensions'))
    if not experiment_id:
        logger.debug("Missing experiment identifier")
        return

    journal["experiment"] = experiment
    journal["status"] = "running"
    execution_url = urls.execution(
        urls.experiment(session.base_url, experiment_id=experiment_id))
    try:
        data = json.dumps(
            {
                "journal": journal
            }, ensure_ascii=False, default=json_encoder)
        r = session.post(execution_url, data=data, headers={
            "content-type": "application/json"
        })
    except Exception:
        logger.debug("Failed to create execution", exc_info=True)
        return

    if r.status_code not in [200, 201]:
        is_json = 'application/json' in r.headers.get("content-type", '')
        error = r.json() if is_json else r.text
        logger.warning("Execution failed to be published: {}".format(error))
    else:
        logger.info("Execution available at {}".format(
            urls.clean(r.headers["Content-Location"])))
        payload = r.json()
        set_execution_id(payload["id"], experiment)

    return r


def publish_execution(session: Session,
                      journal: Journal) -> Optional[Response]:
    """
    Publish the execution.
    """
    experiment = journal["experiment"]
    experiment_id = get_experiment_id(experiment.get("extensions"))
    execution_id = get_execution_id(experiment.get("extensions"))
    execution_url = urls.execution(
        urls.experiment(session.base_url, experiment_id=experiment_id),
        execution_id=execution_id)
    try:
        data = json.dumps(
            {
                "journal": journal
            }, ensure_ascii=False, default=json_encoder)
        r = session.put(execution_url, data=data, headers={
            "content-type": "application/json"
        })
    except Exception:
        logger.debug("Failed to upload execution", exc_info=True)
        return

    if r.status_code not in [200, 204]:
        is_json = 'application/json' in r.headers.get("content-type", '')
        error = r.json() if is_json else r.text
        logger.warning(
            "Execution journal failed to be published: {}".format(error))

    return r


def fetch_execution(session: Session, journal: Journal) -> Optional[Response]:
    """
    Request the execution if an identifier is found the extension block.
    """
    experiment = journal["experiment"]
    experiment_id = get_experiment_id(experiment.get("extensions"))
    execution_id = get_execution_id(experiment.get("extensions"))
    if not execution_id:
        return

    execution_url = urls.execution(
        urls.experiment(session.base_url, experiment_id=experiment_id),
        execution_id=execution_id)
    try:
        r = session.get(execution_url)
    except Exception:
        logger.debug("Failed to fetch execution", exc_info=True)
        return

    if r.status_code > 399:
        return

    return r


def publish_event(session: Session, event_type: str, payload: Any,
                  configuration: Configuration, secrets: Secrets,
                  extensions: List[Extension], settings: Settings,
                  state: Any = None) -> NoReturn:
    """
    Publish an execution's event.
    """
    experiment_id = get_experiment_id(extensions)
    execution_id = get_execution_id(extensions)
    if not execution_id:
        logger.debug(
            "Cannot send event to ChaosIQ because execution "
            "identifier was not found in the experiment's extensions block.")
        return

    tz = get_localzone()
    data = {
        "context": payload,
        "state": state
    }
    try:
        data = json.dumps(data, ensure_ascii=False, default=json_encoder)
    except Exception as x:
        logger.debug(
            "Failed to serialize to json during '{}' event".format(event_type),
            exc_info=True
        )
        data = json.dumps({
            "context": payload,
            "state": None,
            "error": {
                "type": "json-serialization",
                "trace": str(x)
            }
        }, ensure_ascii=False, default=json_encoder)

    event = (
        v02.Event().
        SetContentType("application/json").
        SetData(data).
        SetEventID(str(uuid.uuid4())).
        SetSource("chaosiq-cloud").
        SetEventTime(tz.localize(datetime.now()).isoformat()).
        SetEventType(event_type)
    )
    m = marshaller.NewHTTPMarshaller(
        [
            structured.NewJSONHTTPCloudEventConverter()
        ]
    )

    url = urls.event(urls.execution(
        urls.experiment(session.base_url, experiment_id=experiment_id),
        execution_id=execution_id))
    headers, body = m.ToRequest(event, converters.TypeStructured, lambda x: x)
    r = session.post(url, headers=headers, data=body.getvalue())
    if r.status_code != 201:
        logger.debug("Failed to push event to {}: {}".format(url, r.text))


###############################################################################
# Internals
###############################################################################
def get_experiment_id(extensions: List[Extension]) -> Optional[str]:
    if not extensions:
        return
    for extension in extensions:
        if extension["name"] == "chaosiq":
            return extension.get("experiment_id")


def get_execution_id(extensions: List[Extension]) -> Optional[str]:
    if not extensions:
        return
    for extension in extensions:
        if extension["name"] == "chaosiq":
            return extension.get("execution_id")


def set_execution_id(execution_id: str, experiment: Experiment) -> NoReturn:
    extensions = experiment.get("extensions", [])
    for extension in extensions:
        if extension["name"] == "chaosiq":
            extension["execution_id"] = execution_id
            break
