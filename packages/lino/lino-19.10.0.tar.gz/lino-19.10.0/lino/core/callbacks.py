# -*- coding: UTF-8 -*-
# Copyright 2009-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals, print_function
import six
from builtins import object

import logging ; logger = logging.getLogger(__name__)

import os
from os.path import join, dirname, exists

import sys
import time
# import copy
import codecs
import atexit
import threading
from importlib import import_module


startup_rlock = threading.RLock()  # Lock() or RLock()?


CLONEABLE_ATTRS = frozenset("""ah request user subst_user
bound_action create_kw known_values param_values
action_param_values""".split())


class CallbackChoice(object):
    #~ def __init__(self,name,label,func):

    def __init__(self, name, func, label):
        self.name = name
        self.func = func
        self.label = str(label)


class Callback(object):
    """A callback is a question that rose during an AJAX action.
    The original action is pending until we get a request
    that answers the question.

    TODO: move all callback-related code out of
    :mod:`lino.core.kernel` into to a separate module and install it
    as a "kernel plugin" in a similar way as :mod:`lino.core.web` and
    :mod:`lino.utils.config`.

    """
    title = _('Confirmation')

    def __init__(self, ar, message):
        self.message = message
        self.choices = []
        self.choices_dict = {}
        self.ar = ar

    def __repr__(self):
        return "Callback(%r)" % self.message

    def set_title(self, title):
        self.title = title

    def add_choice(self, name, func, label):
        """
        Add a possible answer to this callback.
        - name: "yes", "no", "ok" or "cancel"
        - func: a callable to be executed when user selects this choice
        - the label of the button
        """
        assert not name in self.choices_dict
        allowed_names = ("yes", "no", "ok", "cancel")
        if not name in allowed_names:
            raise Exception("Sorry, name must be one of %s" % allowed_names)
        cbc = CallbackChoice(name, func, label)
        self.choices.append(cbc)
        self.choices_dict[name] = cbc
        return cbc

class CallbackManager(object):

    def __init__(self):

        self.pending_threads = {}

    def run_callback(self, request, thread_id, button_id):
        """Continue the action which was started in a previous request and
        which asked for user interaction via a :class:`Callback`.

        This is called from :class:`lino.modlib.extjs.views.Callbacks` and
        similar places in other front ends.

        """
        # logger.info("20131212 get_callback %s %s", thread_id, button_id)

        # 20140304 Also set a renderer so that callbacks can use it
        # (feature needed by beid.FindByBeIdAction).

        thread_id = thread_id
        cb = self.pending_threads.pop(thread_id, None)
        if cb is None:
            ar = ActorRequest(request, renderer=self.default_renderer)
            logger.debug("No callback %r in %r" % (
                thread_id, list(self.pending_threads.keys())))
            ar.error("Unknown callback %r" % thread_id)
            return ar.renderer.render_action_response(ar)

        # e.g. SubmitInsertClient must set `data_record` in the
        # callback request ("ar2"), not the original request ("ar"),
        # i.e. the methods to create an instance and to fill
        # `data_record` must run on the callback request.  So the
        # callback request must be a clone of the original request.
        # New since 20140421
        ar = cb.ar.actor.request_from(cb.ar)
        for k in CLONEABLE_ATTRS:
            setattr(ar, k, getattr(cb.ar, k))

        for c in cb.choices:
            if c.name == button_id:
                a = ar.bound_action.action
                if self.site.log_each_action_request and not a.readonly:
                    logger.info("run_callback {0} {1} {2}".format(
                        thread_id, cb.message, c.name))
                    # ar.info(cb.message)
                func = c.func
                try:
                    func(ar)
                except Warning as e:
                    ar.error(e, alert=True)
                return ar.renderer.render_action_response(ar)

        ar.error("Invalid button %r for callback %r" % (button_id, thread_id))
        return ar.renderer.render_action_response(ar)

    def add_callback(self, ar, *msgs):
        """
        Returns an *action callback* which will initiate a dialog thread by
        asking a question to the user and suspending execution until
        the user's answer arrives in a next HTTP request.

        Calling this from an Action's :meth:`run_from_ui
        <lino.core.actions.Action.run_from_ui>` method will interrupt
        the execution, send the specified message back to the user,
        adding the executables `yes` and optionally `no` to a queue of
        pending "dialog threads".

        The client will display the prompt and will continue this
        thread by requesting
        :class:`lino.modlib.extjs.views.Callbacks`.
        """
        if len(msgs) > 1:
            msg = '\n'.join([force_text(s) for s in msgs])
        else:
            msg = msgs[0]
        # logger.info("20160526 add_callback(%s)", msg)
        return Callback(ar, msg)

    def set_callback(self, ar, cb):
        """
        """
        k = "{0:x}".format(hash(cb))
        self.pending_threads[k] = cb
        # logger.info("20160526 Stored %r in %r" % (
        #     h, self.pending_threads))

        buttons = dict()
        for c in cb.choices:
            buttons[c.name] = c.label

        ar.success(
            cb.message, xcallback=dict(
                id=k,
                title=cb.title,
                buttons=buttons))
