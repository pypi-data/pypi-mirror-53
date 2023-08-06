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
#     Daniel Izquierdo <dizquierdo@bitergia.com>
#

from . import its
from .metrics import Metrics


class Jira(its.ITS):
    name = "jira_issues"

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


class JiraMetrics(Metrics):
    """ This class will be the root one for all Jira metrics """
    # TODO: All JiraMetrics metrics should inherit from this class
    # but they are doing it from ITSMetrics directly. Change the design.
    ds = Jira


class Opened(JiraMetrics):
    """ Tickets Opened metric class for issue tracking systems """

    id = "opened"
    name = "Opened tickets"
    desc = "Number of opened tickets"
    FIELD_COUNT = "key"
    FIELD_NAME = "url"


class Openers(its.Openers):
    ds = Jira


class Closed(JiraMetrics):
    """ Tickets Closed metric class for issue tracking systems
       "status":"Closed"  "status":"Resolved"  "status":"Done"
    """
    id = "closed"
    name = "Closed tickets"
    desc = "Number of closed tickets"
    FIELD_COUNT = "key"
    FIELD_NAME = "url"
    filters = {"*status": "Open"}


class DaysToCloseMedian(its.DaysToCloseMedian):
    ds = Jira
    filters = {"*status": "Open"}


class DaysToCloseAverage(its.DaysToCloseAverage):
    ds = Jira
    filters = {"*status": "Open"}


class BMI(its.BMI):
    ds = Jira
    # To use JIRA implementation inside BMI general implementation
    closed_class = Closed
    opened_class = Opened


class Projects(its.Projects):
    ds = Jira
