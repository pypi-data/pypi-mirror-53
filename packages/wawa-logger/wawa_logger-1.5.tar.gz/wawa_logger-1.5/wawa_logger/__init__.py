from requests import post



def publish(**kwargs):
    """
    sends data based on input to centralized source

    params
    :url - where do we send the logs
    :tool_name
    :event_type
    :source_host
    :source_addr
    :dest_host
    :username
    returns
    :bool True|False
    """
    noval = "no_data"
    payload = {
        "tool_name": kwargs.get("tool_name", ""),
        "event_type": kwargs.get("event_type", ""),
        "source_host": kwargs.get("source_host", ""),
        "dest_host": kwargs.get("dest_host", ""),
        "source_addr": kwargs.get("source_addr", ""),
        "username": kwargs.get("username", "")
    }
    try:
        r = post(kwargs.get("url"), json=payload)
    except Exception as e:
        print(f"Exception: {e}")