import os
import openai
import config

openai.api_key = config.API_KEY


class MemorySystem:
    def __init__(self):
        self.memory_path = "memory_files"
        self.reference_path = "memory_reference"
        self.subconscious_path = "subconscious"
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def store_memory(self, content, memory_type):
        # Create memory directory if it doesn't exist
        if not os.path.exists(self.memory_path):
            os.makedirs(self.memory_path)

        # Save the full content to subconscious
        with open(os.path.join(self.subconscious_path, f"{memory_type}.txt"), "a") as f:
            f.write(content + "\n")

        # Summarize the content
        summarized_content = self.summarize_memory(content)

        # Save the summarized content to memory
        with open(os.path.join(self.memory_path, f"{memory_type}.txt"), "a") as f:
            f.write(summarized_content + "\n")

    def summarize_memory(self, content):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following content: {content}"
                }
            ],
            temperature=0.02,
            max_tokens=417,
            top_p=1,
            frequency_penalty=0.51,
            presence_penalty=0.12
        )
        return response.choices[0].message['content']

    def retrieve_memory(self, memory_type):
        with open(os.path.join(self.memory_path, f"{memory_type}.txt"), "r") as f:
            memories = f.readlines()
        return memories

    def evolve_memory(self, memory_type, content):
        # Store the evolved memory in the reference folder
        if not os.path.exists(self.reference_path):
            os.makedirs(self.reference_path)

        with open(os.path.join(self.reference_path, f"{memory_type}.txt"), "a") as f:
            f.write(content + "\n")

    def learn_passively(self, content):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Tell me more about {content}"
                }
            ],
            temperature=0.02,
            max_tokens=417,
            top_p=1,
            frequency_penalty=0.51,
            presence_penalty=0.12
        )
        return response.choices[0].message['content']

# Example usage:
# memory_system = MemorySystem()
# memory_system.store_memory("The Eiffel Tower is located in Paris.", "landmarks")
# print(memory_system.retrieve_memory("landmarks"))
# print(memory_system.learn_passively("Eiffel Tower"))

