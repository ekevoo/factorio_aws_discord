"""
This module handles all the creation that is necessary.
"""
from random import choices

from factorio_aws_discord.bot.aws import EC2, S3, InstanceState
from factorio_aws_discord.bot.model import WorldsTable, World, Chat
from factorio_aws_discord.bot.settings import settings


class Launcher:
    def __init__(self, worlds_table: WorldsTable, ec2: EC2, s3: S3):
        self._worlds = worlds_table
        self._ec2 = ec2
        self._s3 = s3

    def launch(self, chat: Chat, can_create: bool = False) -> InstanceState:
        world = self._worlds.find_one_by(chat_id=chat.chat_id)
        if not world and can_create:
            world = self.create(chat)
        state = self._ec2.ensure_running(world.ec2_instance_id)
        if state == InstanceState.gone:
            state = self.try_to_unarchive(world)
        return state

    def create(self, chat: Chat) -> World:
        alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
        wid = ''.join(choices(alphabet, k=4))
        world = World(wid, '', settings.bucket + '/' + wid, settings.region, chat)
        self._worlds.upsert(world)
        self._ec2.create(world)
        self._worlds.upsert(world)
        return world

    def try_to_unarchive(self, world: World) -> InstanceState:
        if not self._s3.has_archive(world.bucket_url):
            self._worlds.delete(world.wid)
            return InstanceState.gone

        self._ec2.unarchive_from(world)
        self._worlds.upsert(world)
        return self._ec2.ensure_running(world.ec2_instance_id)
