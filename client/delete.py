# -----------------------------------------------------------------------------
# NDN Repo delete client.
#
# @Author Daniel Achee
# @Author Caton Zhong
# @Date   2021-01-25
# -----------------------------------------------------------------------------

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import argparse
import asyncio as aio
from ..protocol.repo_commands import RepoCommand
from .command_checker import CommandChecker
from ..utils import PubSub
import logging
from ndn.app import NDNApp
from ndn.encoding import Name, Component, DecodeError, NonStrictName
from ndn.types import InterestNack, InterestTimeout
from ndn.utils import gen_nonce
from typing import Optional


class DeleteClient(object):
    def __init__(self, app: NDNApp, prefix: NonStrictName, repo_name: NonStrictName):
        """
        This client deletes data packets from the remote repo.
        :param app: NDNApp.
        :param repo_name: NonStrictName. Routable name to remote repo.
        """
        self.app = app
        self.prefix = prefix
        self.repo_name = repo_name
        self.pb = PubSub(self.app, self.prefix)

    async def delete_file(self, file_name: NonStrictName, total_blocks: int, publisher_id, fetch_prefix):
	"""
        Delete file with file name file_name from repo 

        :param file_name: NonStrictName. The name of the file stored in the remote repo.
	:param total_blocks
	:param publisher_id
	:param fetch_prefix
        :return: Boolean of whether delete was acknowledged or not by the repo
        """
        # send command interest
	file = File()
	file.name = file_name
	file.totalBlocks = total_blocks
	file.publisherId = publisher_id 
	fetch_prefix = FetchPrefix()
	fetch_prefix.name = fetch_prefix
        cmd = RepoCommand()
        cmd.file = prefix
        cmd_bytes = cmd.encode()

        # publish msg to repo's delete topic
        await self.pb.wait_for_ready()
        is_success = await self.pb.publish(self.repo_name + ['delete'], cmd_bytes)
        if is_success:
            logging.info('Published an delete msg and was acknowledged by a subscriber')
        else:
            logging.info('Published an delete msg but was not acknowledged by a subscriber')
	return is_success
