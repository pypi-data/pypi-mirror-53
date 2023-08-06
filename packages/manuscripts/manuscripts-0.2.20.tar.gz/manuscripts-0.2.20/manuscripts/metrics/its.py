# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2019 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     Alvaro del Castillo <acs@bitergia.com>
#

""" Metrics for the issue tracking system """

from .metrics import Metrics


class ITS():
    name = "its"

    @classmethod
    def get_section_metrics(cls):
        """
        Get the mapping between metrics and sections in Manuscripts report
        :return: a dict with the mapping between metrics and sections in Manuscripts report
        """

        return {
            "overview": {
                "activity_metrics": [Closed, Opened],
                "author_metrics": [],
                "bmi_metrics": [BMI],
                "time_to_close_metrics": [DaysToCloseMedian],
                "projects_metrics": [Projects]
            },
            "com_channels": {
                "activity_metrics": [],
                "author_metrics": []
            },
            "project_activity": {
                "metrics": [Opened, Closed]
            },
            "project_community": {
                "author_metrics": [],
                "people_top_metrics": [],
                "orgs_top_metrics": [],
            },
            "project_process": {
                "bmi_metrics": [BMI],
                "time_to_close_metrics": [DaysToCloseAverage, DaysToCloseMedian],
                "time_to_close_title": "Days to close (median and average)",
                "time_to_close_review_metrics": [],
                "time_to_close_review_title": "",
                "patchsets_metrics": []
            }
        }


class ITSMetrics(Metrics):
    """ This class is the root one for all ITS metrics """

    ds = ITS


class Opened(ITSMetrics):
    """ Tickets Opened metric class for issue tracking systems """

    id = "opened"
    name = "Opened tickets"
    desc = "Number of opened tickets"
    FIELD_COUNT = "id"
    FIELD_NAME = "url"


class Openers(ITSMetrics):
    """ Tickets Openers metric class for issue tracking systems """

    id = "openers"
    name = "Ticket submitters"
    desc = "Number of persons submitting new tickets"
    FIELD_COUNT = 'author_uuid'  # field used to count Authors
    FIELD_NAME = 'author_name'  # field used to list Authors


class Closed(ITSMetrics):
    """ Tickets Closed metric class for issue tracking systems
       "state": "closed" is the filter to be used in GitHub
    """
    id = "closed"
    name = "Closed tickets"
    desc = "Number of closed tickets"
    filters = {"state": "closed"}
    FIELD_COUNT = "id"
    FIELD_NAME = "url"
    FIELD_DATE = "closed_at"


class DaysToCloseMedian(ITSMetrics):
    id = "days_to_close_ticket_median"
    name = "Days to close tickets (median)"
    desc = "Number of days needed to close a ticket (median)"
    FIELD_COUNT = 'time_to_close_days'
    AGG_TYPE = 'median'
    filters = {"state": "closed"}

    def get_agg(self):
        agg = super(DaysToCloseMedian, self).get_agg()
        if agg is None:
            agg = 0  # None is because NaN in ES. Let's convert to 0
        return agg


class DaysToCloseAverage(ITSMetrics):
    id = "days_to_close_ticket_avg"
    name = "Days to close tickets (average)"
    desc = "Number of days needed to close a ticket (average)"
    FIELD_COUNT = 'time_to_close_days'
    AGG_TYPE = 'average'
    filters = {"state": "closed"}


# NOT IMPLEMENTED YET
# class Closers(ITSMetrics):
#     """ Tickets Closers metric class for issue tracking systems """
#     id = "closers"
#     name = "Tickets closers"
#     desc = "Number of persons closing tickets"


class BMI(ITSMetrics):
    """ The Backlog Management Index measures efficiency dealing with tickets

        This is based on the book "Metrics and Models in Software Quality
        Engineering. Chapter 4.3.1. By Stephen H. Kan.

        BMI is calculated as the number of closed tickets out of the opened
        tickets in a given interval. This metric aims at having an overview of
        how the community deals with tickets. Continuous values under 1
        (or 100 if this is calculated as a percentage) shows low peformance
        given that the community leaves a lot of opened tickets. Continuous
        values close to 1 or over 1 shows a better performance. This would
        indicate that most of the tickets are being closed.
    """

    id = "bmi_tickets"
    name = "Backlog Management Index"
    desc = "Number of tickets closed out of the opened ones in a given interval"
    closed_class = Closed
    opened_class = Opened

    def __get_metrics(self):
        """ Each metric must have its own filters copy to modify it freely"""
        esfilters_closed = None
        esfilters_opened = None
        if self.esfilters:
            esfilters_closed = self.esfilters.copy()
            esfilters_opened = self.esfilters.copy()

        closed = self.closed_class(self.es_url, self.es_index,
                                   start=self.start, end=self.end,
                                   esfilters=esfilters_closed, interval=self.interval)
        opened = self.opened_class(self.es_url, self.es_index,
                                   start=self.start, end=self.end,
                                   esfilters=esfilters_opened, interval=self.interval)
        return (closed, opened)

    def get_agg(self):
        (closed, opened) = self.__get_metrics()
        closed_agg = closed.get_agg()
        opened_agg = opened.get_agg()

        if opened_agg == 0:
            bmi = 1  # if no submitted issues/prs, bmi is at 100%
        else:
            bmi = closed_agg / opened_agg

        return bmi

    def get_ts(self):
        bmi = {}
        (closed, opened) = self.__get_metrics()
        closed_ts = closed.get_ts()
        opened_ts = opened.get_ts()

        bmi['date'] = closed_ts['date']
        bmi['unixtime'] = closed_ts['unixtime']
        bmi['value'] = []
        for i in range(0, len(opened_ts['value'])):
            if opened_ts['value'][i] == 0:
                bmi['value'].append(0)
            else:
                bmi['value'].append(closed_ts['value'][i] / opened_ts['value'][i])

        return bmi


class Projects(ITSMetrics):
    """ Projects metric class for issue tracking systems """
    id = "projects"
    name = "Projects"
    desc = "Number of distinct projects active in the ticketing system"
    FIELD_NAME = 'project'  # field used to list projects
