l
import os
import bpy
import ssl
import sys
import json
import pathlib
import asyncio
import logging
import datetime
import requests
import traceback
import webbrowser

from .. import updater
from .utils import ui_refresh_all, cancel_gen

from threading import Thread, Timer
from contextlib import suppress
from typing import AsyncGenerator
from urllib.parse import urlparse

# Import extra libraries
loaded_all_libs = False
try:
    import boto3
    from gql import Client, gql
    from cryptography.fernet import Fernet
    from gql.transport.appsync_websockets import AppSyncWebsocketsTransport
    from gql.transport.appsync_auth import AppSyncApiKeyAuthentication
    from gql.transport.websockets import log as websockets_logger

    # Set logging levels
    websockets_logger.setLevel(logging.CRITICAL)
    logging.getLogger('boto').setLevel(logging.CRITICAL)
    loaded_all_libs = True
except ImportError as e:
    print(e)


# Disable SSL
ssl._create_default_https_context = ssl._create_unverified_context

class User:
    classes_logged_in = []
    classes_logged_out = []

    def __init__(self):
        self.logging_in = False

        self.logged_in = True
        self.email = "wowowowo@example.com"
        self.username = "lelelele"  # This is a unique id

        self.display_email = False
        self.display_error = None

        self.login_time = None
        self.version_str = "1.0.0"
        self.classes_logged_in = []
        self.classes_logged_out = []

    def set_info(self, classes_logged_in, classes_logged_out, bl_info):
        self.classes_logged_in = classes_logged_in
        self.classes_logged_out = classes_logged_out
        self.version_str = ".".join(map(str, bl_info.get("version")))

    def auto_login(self):
        # Check the login cache

        self.login(data, register_classes=True)

        return self.logged_in

    def login(self, data, register_classes=True):

        self.logged_in = True
        self.display_error = None
        self.login_time = datetime.datetime.utcnow().timestamp()

        self.email = "wowowowo@example.com"
        self.username = "lelelele"  # This is a unique id

        if register_classes:
            self.register_classes()

    def logout(self):
        if not self.logged_in:
            return

        self.logged_in = False
        self.unregister_classes()

    def quit(self):
        pass

    def error(self, *msg):
        # Update the UI if the user is still logging in or of the error message changes
        update_ui = self.logging_in or msg != self.display_error

        self.logging_in = False
        self.display_error = msg

        if update_ui and not self.logged_in:
            ui_refresh_all()

    def register_classes(self):
        # Unregister logged out classes
        for cls in reversed(self.classes_logged_out):
            bpy.utils.unregister_class(cls)

        # Register logged in classes
        for cls in self.classes_logged_in:
            bpy.utils.register_class(cls)

    def unregister_classes(self):
        # Unregister classes_logged_in
        for cls in reversed(self.classes_logged_in):
            bpy.utils.unregister_class(cls)

        # Register classes_logged_out
        for cls in self.classes_logged_out:
            bpy.utils.register_class(cls)

user: User = User()




