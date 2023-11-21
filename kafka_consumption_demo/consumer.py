from DigitizerEventListMessage import *
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

TRACE_TOPIC = "trace_in"
BROKER_ADDRESS = "localhost:9092"
NUM_EVENTS_TO_DISPLAY = 5


def parse_msg(msg: ConsumerRecord) -> DigitizerEventListMessage:
    """
    Deserialises received messages using the flatbuffers schema.

    Parameters:
    msg (ConsumerRecord): The message to be parsed.

    Returns:
    DigitizerEventListMessage: The deserialised payload.
    """
    payload = DigitizerEventListMessage.GetRootAs(msg.value, 0)
    return payload


def hline():
    """
    Print a horizontal seperator to the console.
    """
    print("-------------------------------------------------------------")


def display_metadata(payload: DigitizerEventListMessage):
    """
    Displays the metadata of a deserialised message.
    """
    metadata = payload.Metadata()
    timestamp = metadata.Timestamp()
    print(
        "Timestamp:\t\t\t",
        timestamp.Hour(),
        ":",
        timestamp.Minute(),
        ", ",
        timestamp.Second() * (10**9)
        + timestamp.Millisecond() * (10**6)
        + timestamp.Microsecond() * (10**3)
        + timestamp.Nanosecond(),
        " ns",
    )
    print("Running:\t\t\t", metadata.Running())
    print("Veto Flags:\t\t\t", metadata.VetoFlags())
    print("Frame Number:\t\t\t", metadata.FrameNumber())
    print("Period Number:\t\t\t", metadata.PeriodNumber())
    print("Protons Per Pulse:\t\t", metadata.ProtonsPerPulse())
    hline()


def display_events(payload: DigitizerEventListMessage, num_events_to_display: int):
    """
    Displays the event list size information of a deserialised message.
    """
    num_voltages = payload.VoltageLength()
    num_channels = payload.ChannelLength()
    voltages_to_display = min(num_voltages, num_events_to_display)
    channels_to_display = min(num_channels, num_events_to_display)
    print(f"Received {num_voltages} voltages. First {voltages_to_display} voltages:")
    for i in range(0, voltages_to_display):
        print(payload.Voltage(i))
    hline()
    print(f"Received {num_channels} channels. First {channels_to_display} channels:")
    for i in range(0, channels_to_display):
        print(payload.Channel(i))
    hline()


def display_payload_information(
    payload: DigitizerEventListMessage, num_events_to_display: int
):
    """
    Displays the metadata and event list size information of a deserialised message.
    """
    hline()
    print("[RECEIVED MESSAGE]:")
    hline()
    display_events(payload, num_events_to_display)
    display_metadata(payload)
    print("\n")


def listen(trace_topic: str, broker_address: str):
    """
    Listens on a particular trace topic and attempts to parse any detected messages.

    Parameters:
    trace_topic (str): The name of the trace topic.
    """
    consumer = KafkaConsumer(trace_topic, bootstrap_servers=broker_address)
    for msg in consumer:
        payload = parse_msg(msg)
        display_payload_information(payload, NUM_EVENTS_TO_DISPLAY)


listen(TRACE_TOPIC, BROKER_ADDRESS)
