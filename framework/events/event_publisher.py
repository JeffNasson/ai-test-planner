from framework.events.event_listener import on_validation_completed

def publish_event(event_name: str, data: dict):
    print(f"EVENT: {event_name}")
    print(data)

    if event_name == "ValidationCompleted":
        on_validation_completed(data)