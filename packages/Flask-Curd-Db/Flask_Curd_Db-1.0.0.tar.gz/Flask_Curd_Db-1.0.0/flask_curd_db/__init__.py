#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 10:55
# @File    : __init__.py.py
# @author  : dfkai
# @Software: PyCharm
import logging


class _FlaskCurdDB(object):
    def __init__(self, app=None, db=None, logger=None):
        self.app = app
        self.db = db
        if not logger and app:
            self._logger = app.logger
        else:
            self.logger = logger

    def get_app(self):
        if self.app is None:
            logging.warning("FlaskCurdDb not init app")
        if self.db is None:
            logging.warning("FlaskCurdDb not init db")
        if not self.logger:
            if self.app:
                self.logger = self.app.logger
            else:
                self.logger = logging
        return self.app, self.db, self.logger


_flask_curd_db = _FlaskCurdDB()


def FlaskCurdDb(app, db, logger=None):
    _flask_curd_db.__init__(app, db, logger)


