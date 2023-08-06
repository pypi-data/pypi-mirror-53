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

    def get_dict(self, items, key='id'):
        """Return a dict from a list."""
        data = {}
        for i in items:
            if key not in i or not i[key]:
                continue
            k = i[key]
            data[k] = i
        return data

    def get_members(self):
        """Return a list of members."""
        query = self.db.collection('github_members')
        members = []
        for item in query.stream():
            members.append(item.to_dict())
        return members

    def get_members_dict(self, key='id'):
        """Return a dict of members by member id."""
        return self.get_dict(self.get_members(), key)

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
        return self.get_dict(self.get_people(), key)

    def get_repos(self):
        """Return a list of repos."""
        query = self.db.collection('github_repos')
        repos = []
        for item in query.stream():
            repos.append(item.to_dict())
        return repos

    def get_repos_dict(self, key='id'):
        """Return a dict of repos by repo id."""
        return self.get_dict(self.get_repos(), key)

    def get_repos_outside_collaborators(self):
        """Return a list of repos outside collaborators."""
        query = self.db.collection('github_repos_outside_collaborators')
        repos_outside_collaborators = []
        for item in query.stream():
            repos_outside_collaborators.append(item.to_dict())
        return repos_outside_collaborators

    def get_repos_outside_collaborators_dict(self, key='id'):
        """Return a dict of repos outside collaborators."""
        return self.get_dict(self.get_repos_outside_collaborators(), key)

    def get_teams(self):
        """Return a list of teams."""
        query = self.db.collection('github_teams')
        teams = []
        for item in query.stream():
            teams.append(item.to_dict())
        return teams

    def get_teams_dict(self, key='id'):
        """Return a dict of teams by team id."""
        return self.get_dict(self.get_teams(), key)

    def get_team_syncs(self):
        """Return a list of team syncs."""
        query = self.bitsdb.collection('github_team_syncs')
        team_syncs = []
        for item in query.stream():
            team_syncs.append(item.to_dict())
        return team_syncs

    def get_team_syncs_dict(self, key='github_team_slug'):
        """Return a dict of team syncs by team id."""
        return self.get_dict(self.get_team_syncs(), key)

    def get_teams_members(self):
        """Return a list of team syncs."""
        query = self.db.collection('github_teams_members')
        teams_members = []
        for item in query.stream():
            teams_members.append(item.to_dict())
        return teams_members

    def get_teams_members_dict(self, key='id'):
        """Return a dict of team syncs by team id."""
        return self.get_dict(self.get_teams_members_dict(), key)

    def get_teams_repos(self):
        """Return a list of team syncs."""
        query = self.db.collection('github_teams_repos')
        teams_repos = []
        for item in query.stream():
            teams_repos.append(item.to_dict())
        return teams_repos

    def get_teams_repos_dict(self, key='id'):
        """Return a dict of team syncs by team id."""
        return self.get_dict(self.get_teams_repos_dict(), key)
