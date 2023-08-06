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


class GitHubIssues(its.ITS):
    name = "github_issues"

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


class GitHubIssuesMetrics(its.ITS):
    """ This class will be the root one for all GitHubIssues metrics """
    # TODO: All GitHubIssuesMetrics metrics should inherit from this class
    # but they are doing it from ITSMetrics directly. Change the design.
    ds = GitHubIssues


class Opened(its.Opened):
    ds = GitHubIssues
    filters = {"pull_request": "false"}


class Openers(its.Openers):
    ds = GitHubIssues
    filters = {"pull_request": "false"}


class Closed(its.Closed):
    ds = GitHubIssues
    filters = {"state": "closed", "pull_request": "false"}


class DaysToCloseMedian(its.DaysToCloseMedian):
    ds = GitHubIssues
    filters = {"state": "closed", "pull_request": "false"}


class DaysToCloseAverage(its.DaysToCloseAverage):
    ds = GitHubIssues
    filters = {"state": "closed", "pull_request": "false"}


class BMI(its.BMI):
    ds = GitHubIssues
    filters = {"pull_request": "false"}


class Projects(its.Projects):
    ds = GitHubIssues
    filters = {"pull_request": "false"}
