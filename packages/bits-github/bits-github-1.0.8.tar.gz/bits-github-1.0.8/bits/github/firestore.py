# -*- coding: utf-8 -*-
"""Firestore Class file."""

from google.cloud import firestore


class Firestore(object):
    """Firestore class."""

    def __init__(self, auth, github, project='broad-bitsdb-firestore'):
        """Initialize a class instance."""
        self.github = github
        self.project = project

        self.firestore = firestore
        self.db = firestore.Client(self.project)

        self.bitsdb_project = 'broad-bitsdb-prod'
        self.bitsdb = firestore.Client(self.bitsdb_project)

    def get_people(self):
        """Return a list of people."""
        fields = [
            'email_username',
            'emplid',
            'full_name',
            'github_id',
            'github_login',
            'google_id',
            'terminated',
            'username',
        ]
        query = self.db.collection('people_people').select(fields)
        people = []
        for item in query.stream():
            people.append(item.to_dict())
        return people

    def get_people_dict(self, key='email_username'):
        """Return a dict of people by username."""
        people = {}
        for p in self.get_people():
            if key not in p or not p[key]:
                continue
            k = p[key]
            people[k] = p
        return people

    def get_repos_outside_collaborators(self):
        """Return a list of repo syncs."""
        query = self.db.collection('github_repos_outside_collaborators')
        repos_outside_collaborators = []
        for item in query.stream():
            repos_outside_collaborators.append(item.to_dict())
        return repos_outside_collaborators

    def get_repos_outside_collaborators_dict(self, key='id'):
        """Return a dict of repo syncs by repo id."""
        repos_outside_collaborators = {}
        for t in self.get_repos_outside_collaborators():
            repo_id = t[key]
            repos_outside_collaborators[repo_id] = t
        return repos_outside_collaborators

    def get_team_syncs(self):
        """Return a list of team syncs."""
        query = self.bitsdb.collection('github_team_syncs')
        team_syncs = []
        for item in query.stream():
            team_syncs.append(item.to_dict())
        return team_syncs

    def get_team_syncs_dict(self, key='github_team_slug'):
        """Return a dict of team syncs by team id."""
        team_syncs = {}
        for s in self.get_team_syncs():
            team_id = s[key]
            team_syncs[team_id] = s
        return team_syncs

    def get_teams_members(self):
        """Return a list of team syncs."""
        query = self.db.collection('github_teams_members')
        teams_members = []
        for item in query.stream():
            teams_members.append(item.to_dict())
        return teams_members

    def get_teams_members_dict(self, key='id'):
        """Return a dict of team syncs by team id."""
        teams_members = {}
        for t in self.get_teams_members():
            team_id = t[key]
            teams_members[team_id] = t
        return teams_members

    def get_teams_repos(self):
        """Return a list of team syncs."""
        query = self.db.collection('github_teams_repos')
        teams_repos = []
        for item in query.stream():
            teams_repos.append(item.to_dict())
        return teams_repos

    def get_teams_repos_dict(self, key='id'):
        """Return a dict of team syncs by team id."""
        teams_repos = {}
        for t in self.get_teams_repos():
            team_id = t[key]
            teams_repos[team_id] = t
        return teams_repos
