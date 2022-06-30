from discord import VoiceClient
from youtube import Music, Youtube


class Queue():
    def __init__(self):
        self.queue = {}


    def add(self, guild_id: str, music: Music):
        temp = self.queue.get(guild_id, [])
        self.queue[guild_id] = [music] + temp


    def poll(self, guild_id: str):
        temp = self.queue[guild_id]
        self.queue[guild_id] = temp[:-1]

        if len(temp) == 0:
            return None

        return temp[-1]


    def reset(self, guild_id: str):
        self.queue[guild_id] = []

    def get_queue(self, guild_id: str):
        return self.queue.get(guild_id, [])

