from DigitizerEventListMessage import *
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

TRACE_TOPIC = "trace_in"
BROKER_ADDRESS = "localhost:9092"


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


def display_payload_information(payload: DigitizerEventListMessage):
    """
    Displays the metadata and event list size information of a deserialised message.
    """
    metadata = payload.Metadata()
    print("-------------------------------------------------------------")
    print("[RECEIVED MESSAGE]:")
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
    print("-------------------------------------------------------------\n")


def listen(trace_topic: str, broker_address: str):
    """
    Listens on a particular trace topic and attempts to parse any detected messages.

    Parameters:
    trace_topic (str): The name of the trace topic.
    """
    consumer = KafkaConsumer(trace_topic, bootstrap_servers=broker_address)
    for msg in consumer:
        payload = parse_msg(msg)
        display_payload_information(payload)


listen(TRACE_TOPIC, BROKER_ADDRESS)
