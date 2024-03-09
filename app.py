from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv
import re
from openai.types.beta import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.run import Run
from openai.types.beta.threads.thread_message import ThreadMessage
import time


load_dotenv(".env")  # Replace ".env" with your actual .env file path

client = OpenAI()
client2 = OpenAI()
topic = input("Enter your topic here: ")

# Create assistant1
assistant1 = client.beta.assistants.create(
    name="cool debater",
    instructions='your task is to debate on the topic given to you.and then argue on the topic.you are a very cool presenter. knowledgeable, who argue based on real points.',
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-1106"
)

# Create assistant2
assistant2 = client2.beta.assistants.create(
    name="aggressive debater",
    instructions='your task is to debate on the topic given to you.and then argue on the topic. you are very well-knowing debater. who believe in the past history. you believe history repeat itself. and always prove yourself',
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-1106"
)

# Create threads for each assistant
thread1 = client.beta.threads.create()
thread2 = client2.beta.threads.create()

while True:
    # Assistant1
    message1 = client.beta.threads.messages.create(
        thread_id=thread1.id,
        role="user",
        content=topic
    )

    run1 = client.beta.threads.runs.create(
        thread_id=thread1.id,
        assistant_id=assistant1.id,
        instructions="aggressively prove your points.try to prove wrong the other perspictive presentaed to you. empower your words. try to make your converation small in less then 50 words"
    )

    while run1.status != "completed":
        run1 = client.beta.threads.runs.retrieve(
            thread_id=thread1.id,
            run_id=run1.id
        )
        time.sleep(1)

    messages1 = client.beta.threads.messages.list(
        thread_id=thread1.id
    )

    for m in messages1.data:
        
        if m.role == "assistant":
            print(m.role + "1: " + m.content[0].text.value)
            topic = m.content[0].text.value
            break
            

    print("    ")
    message2 = client2.beta.threads.messages.create(
        thread_id=thread2.id,
        role="user",
        content=topic
    )

    # Assistant2
    run2 = client2.beta.threads.runs.create(
        thread_id=thread2.id,
        assistant_id=assistant2.id,
        instructions="aggressively prove your points.try to prove wrong the other perspictive presentaed to you. empower your words. try to make your converation small in less then 50 words"
    )

    while run2.status != "completed":
        run2 = client2.beta.threads.runs.retrieve(
            thread_id=thread2.id,
            run_id=run2.id
        )
        time.sleep(1)

    messages2 = client2.beta.threads.messages.list(
        thread_id=thread2.id
    )
    for m in messages2.data:
        
        if m.role == "assistant":
            print(m.role + "2: " + m.content[0].text.value)
            topic = m.content[0].text.value
            break
    print("   ")
