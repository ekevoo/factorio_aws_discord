""" Access to AWS resources """
from enum import Enum

from factorio_aws_discord.bot.model import World


class InstanceState(Enum):
    running = 'running'
    gone = 'gone'


class EC2:
    def ensure_running(self, ec2_instance_id: str) -> InstanceState:
        raise NotImplemented

    def create(self, world: World):
        raise NotImplemented

    def unarchive_from(self, world: World):
        raise NotImplemented


class S3:
    def has_archive(self, bucket_url: str) -> bool:
        raise NotImplemented
