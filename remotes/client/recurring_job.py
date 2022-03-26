##
#     Project: Django Remotes
# Description: A Django application to execute remote commands
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2022 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import sched
import time
import typing


class RecurringJob(object):
    """
    Enqueue recurring jobs every `interval` seconds
    """
    def __init__(self):
        """
        Setup the scheduler object
        """
        self.scheduler = sched.scheduler(timefunc=time.time,
                                         delayfunc=time.sleep)

    def add_job(self,
                delay: int,
                action: typing.Callable,
                *args: typing.Any,
                **kwargs: typing.Any) -> None:
        """
        Add an `action` execution after a `delay`.
        The `action` will be repeated if it returns a value or it will be
        canceled in the case it returned a False value.

        :param delay: delay in seconds between the execution
        :param action: callable to execute (return True to repeat it again)
        :param args: arguments list to pass to the action
        :param kwargs: keyword arguments list to pass to the action
        :return: None
        """
        def queue_job(*arguments: typing.Any,
                      **kwarguments: typing.Any) -> None:
            """
            Enqueue the job and schedule the restart

            :return: None
            """
            if action(*arguments, **kwarguments):
                self.scheduler.enter(delay=delay,
                                     priority=1,
                                     action=queue_job,
                                     argument=arguments,
                                     kwargs=kwarguments)

        self.scheduler.enter(delay=delay,
                             priority=1,
                             action=queue_job,
                             argument=args,
                             kwargs=kwargs)

    def run(self) -> None:
        """
        Execute the recurring actions

        :return: None
        """
        self.scheduler.run()
