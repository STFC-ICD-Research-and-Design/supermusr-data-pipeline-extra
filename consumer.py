import flatbuffers
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

import DigitizerEventListMessage

TRACE_TOPIC = "trace_in"


def parse_msg(msg: ConsumerRecord) -> bytearray:
    """
    Parses messages detected on a particular trace_topic and serialises them using the flatbuffers schema.

    Parameters:
    msg (ConsumerRecord): The message to be parsed.

    Returns:
    bytearray: The serialised buffer.
    """
    # Create a `FlatBufferBuilder`
    builder = flatbuffers.Builder(1024)
    DigitizerEventListMessage.Start(builder)
    # DigitizerEventListMessage.AddVoltage(builder, voltage)
    serialised = DigitizerEventListMessage.End(builder)
    builder.Finish(serialised)
    buf = builder.Output()
    return buf


def listen(trace_topic: str):
    """
    Listens on a particular trace topic and attempts to pass any detected messages.

    Parameters:
    trace_topic (str): The name of the trace topic.
    """
    consumer = KafkaConsumer(trace_topic)
    for msg in consumer:
        buf = parse_msg(msg)
        print(buf)


listen(TRACE_TOPIC)
