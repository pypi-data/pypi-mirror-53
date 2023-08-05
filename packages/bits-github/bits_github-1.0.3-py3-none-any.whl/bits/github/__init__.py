# -*- coding: utf-8 -*-
"""GitHub class file."""

import requests


class GitHub(object):
    """GitHub class."""

    def __init__(
            self,
            token,
            org=None,
            owner_team=None,
            role_team=None,
            verbose=False,
    ):
        """Initialize an GitHub class instance."""
        # set github token
        self.token = token

        # set github organization name
        self.org = org

        # set a team to include all owners
        self.owner_team = owner_team

        # set a team to include all role accounts
        self.role_team = role_team

        # enable verbosity
        self.verbose = verbose

        # set the base urls
        self.base_url = 'https://api.github.com'
        self.org_base_url = '{}/orgs/{}'.format(self.base_url, self.org)

        # set the headers for authorized requests
        self.headers = {'Authorization': 'token {}'.format(self.token)}

    #
    # Sub Classes
    #
    def datastore(self, auth):
        """Return a Datastore instance."""
        from bits.github.datastore import Datastore
        return Datastore(auth, self)

    def firestore(self, auth):
        """Return a Firestore instance."""
        from bits.github.firestore import Firestore
        return Firestore(auth, self)

    def sync(self, auth):
        """Return an Update instance."""
        from bits.github.sync import Sync
        return Sync(auth, self)

    def update(self, auth):
        """Return an Update instance."""
        from bits.github.update import Update
        return Update(auth, self)

    #
    # Helpers
    #
    def get(self, url, headers={}, params={}):
        """Return a response from a GET call."""
        # add any additional headers
        headers = {**self.headers, **headers}

        # ret response to request
        response = requests.get(url, headers=headers, params=params)

        # raise for status
        response.raise_for_status()

        # return json
        return response

    def get_list(self, base_url, url, headers={}, params={}):
        """Return a paginated list from a GET call."""
        items_list = []

        # add any additional headers
        headers = {**self.headers, **headers}

        next_url = '{}/{}'.format(base_url, url)

        while next_url:
            # get response to request
            response = requests.get(next_url, headers=headers, params=params)

            # raise for status
            response.raise_for_status()

            # get next url from response links
            next_url = response.links.get('next', {}).get('url')

            # add items to list
            items_list.extend(response.json())

        return items_list

    #
    # Organizations
    #
    def get_org(self, org=None):
        """Return an organization."""
        # GET /orgs/:org
        if not org:
            org = self.org
        url = '{}/orgs/{}'.format(self.base_url, org)
        return self.get(url).json()

    #
    # Org Hooks
    #
    def get_org_hooks(self):
        """Return a list of organization hooks."""
        # GET /orgs/:org/hooks
        return self.get_list(self.org_base_url, 'hooks')

    #
    # Org Invitations
    #
    def get_org_invitations(self):
        """Return a list of organization invitations."""
        # GET /orgs/:org/invitations
        headers = {'Accept': 'application/vnd.github.dazzler-preview'}
        return self.get_list(self.org_base_url, 'invitations', headers=headers)

    def get_org_invitation_teams(self, invitation_id):
        """Return a list of organization invitation teams."""
        # GET /orgs/:org/invitations/:invitation_id/teams
        headers = {'Accept': 'application/vnd.github.dazzler-preview'}
        url = 'invitations/{}/teams'.format(invitation_id)
        return self.get_list(self.org_base_url, url, headers)

    #
    # Org Members
    #
    def get_org_members(self, filterString=None, role=None, insecure=False):
        """Return a list of organization members."""
        # GET /orgs/:org/members
        params = {
            'filter': filterString,
            'role': role,
        }
        if insecure:
            params['filter'] = '2fa_disabled'
        return self.get_list(self.org_base_url, 'members', params=params)

    #
    # Org Memberships
    #
    def get_org_membership(self, member):
        """Return a user's organization membership."""
        # GET /orgs/:org/memberships/:username
        url = '{}/orgs/{}/memberships/{}'.format(self.base_url, self.org, member)
        return self.get(url).json()

    def invite_org_member(self, member):
        """Invite a member to the organization."""
        # PUT /orgs/:org/memberships/:username
        url = '{}/memberships/{}'.format(self.org_base_url, member)
        return requests.put(url, headers=self.headers).json()

    def remove_org_member(self, member):
        """Delete an invitation to the organization."""
        # DELETE /orgs/:org/memberships/:username
        url = '{}/memberships/{}'.format(self.org_base_url, member)
        return requests.put(url, headers=self.headers).json()

    #
    # Org Outside Collaborators
    #
    def get_org_outside_collaborators(self, filterString=None, insecure=False):
        """Return a list of organization outside_collaborators."""
        # GET /orgs/:org/outside_collaborators
        headers = {
            # 'Accept': 'application/vnd.github.korra-preview'
        }
        params = {
            'filter': filterString,
        }
        if insecure:
            params['filter'] = '2fa_disabled'
        return self.get_list(self.org_base_url, 'outside_collaborators', headers=headers, params=params)

    #
    # Org Public Members
    #
    def get_org_public_member(self, member):
        """Check if a user is a public member of the org."""
        # GET /orgs/:org/public_members/:username
        url = '{}/orgs/{}/public_members/{}'.format(self.base_url, self.org, member)
        return self.get(url)

    def get_org_public_members(self):
        """Return a list of organization public members."""
        # GET /orgs/:org/public_members
        return self.get_list(self.org_base_url, 'public_members')

    #
    # Org Repos
    #
    def get_org_repos(self):
        """Return a list of organization repos."""
        # GET /orgs/:org/repos
        headers = {'Accept': 'application/vnd.github.baptiste-preview+json'}
        return self.get_list(self.org_base_url, 'repos', headers=headers)

    #
    # Org Teams
    #
    def get_org_teams(self):
        """Return a list of organization teams."""
        # GET /orgs/:org/teams
        # add header for Nested Teams API preview
        headers = {'Accept': 'application/vnd.github.hellcat-preview+json'}
        return self.get_list(self.org_base_url, 'teams', headers)

    def get_org_team_hierarchy(self):
        """Return a dict of organization teams and their children."""
        organization = {}
        teams = self.get_org_teams()
        for team in sorted(teams, key=lambda x: x.get('parent')):
            tid = team['id']
            parent = team['parent']
            if not parent:
                team['children'] = []
                organization[tid] = team
            else:
                pid = parent['id']
                if pid not in organization:
                    print('ERROR: Parent ID not found: {}'.format(pid))
                else:
                    organization[pid]['children'].append(team)
        return organization

    #
    # Repos
    #
    def get_repo(self, repo, etag=None):
        """Return a repo of the organization."""
        # GET /repos/:owner/:repo
        url = '{}/repos/{}/{}'.format(self.base_url, self.org, repo)
        headers = self.headers.copy()
        if etag:
            headers['If-None-Match'] = etag
            return self.get(url, headers=headers)
        return self.get(url, headers=headers).json()

    def get_repo_collaborators(self, repo, affiliation=None):
        """Return a list of repo hook."""
        # GET /repos/:owner/:repo/collaborators
        url = 'repos/{}/{}/collaborators'.format(self.org, repo)
        params = {'affiliation': affiliation}
        return self.get_list(self.base_url, url, params=params)

    def get_repo_hooks(self, repo):
        """Return a list of repo hook."""
        # GET /repos/:owner/:repo/hooks
        url = 'repos/{}/{}/hooks'.format(self.org, repo)
        return self.get_list(self.base_url, url)

    def update_repo_hook(self, repo, hook_id, body):
        """Update a repo hook."""
        # PATCH /repos/:owner/:repo/hooks/:hook_id
        url = '{}/repos/{}/{}/hooks/{}'.format(self.base_url, self.org, repo, hook_id)
        return requests.patch(url, headers=self.headers, json=body)

    #
    # Teams
    #
    def get_team(self, team_id, etag=None):
        """Return a team of the organization."""
        # GET /teams/:team_id
        url = '{}/teams/{}'.format(self.base_url, team_id)
        headers = self.headers.copy()
        if etag:
            headers['If-None-Match'] = etag
            return self.get(url, headers=headers)
        return self.get(url, headers=headers).json()

    def get_team_invitations(self, team_id):
        """Return a list of team invitations."""
        # GET /teams/:team_id/invitations
        headers = {'Accept': 'application/vnd.github.dazzler-preview+json'}
        url = 'teams/{}/invitations'.format(team_id)
        return self.get_list(self.base_url, url, headers=headers)

    def get_team_members(self, team_id, role='all'):
        """Return a list of team members."""
        # GET /teams/:team_id/members
        # headers = {'Accept': 'application/vnd.github.hellcat-preview+json'}
        params = {'role': role}
        url = 'teams/{}/members'.format(team_id)
        return self.get_list(self.base_url, url, params=params)

    def get_team_members_with_children(self, team_id, role='all'):
        """Return a list of team members."""
        # GET /teams/:team_id/members
        headers = {'Accept': 'application/vnd.github.hellcat-preview+json'}
        params = {'role': role}
        url = 'teams/{}/members'.format(team_id)
        return self.get_list(self.base_url, url, headers=headers, params=params)

    def invite_team_member(self, team, member):
        """Invite a member to the organization."""
        # PUT /teams/:id/memberships/:username
        params = {'role': 'member'}
        url = '{}/teams/{}/memberships/{}'.format(self.base_url, team, member)
        return requests.put(url, headers=self.headers, params=params)

    def remove_team_member(self, team, member):
        """Invite a member to the organization."""
        # DELETE /teams/:id/memberships/:username
        url = '{}/teams/{}/memberships/{}'.format(self.base_url, team, member)
        return requests.delete(url, headers=self.headers)

    def get_team_repos(self, team_id):
        """Return a list of team members."""
        # GET /teams/:team_id/repos
        # Add header to get the Nested Teams API
        # headers = {'Accept': 'application/vnd.github.hellcat-preview+json'}
        url = 'teams/{}/repos'.format(team_id)
        return self.get_list(self.base_url, url)

    #
    # User (self - logged in user)
    #
    def get_self(self, etag=None, last_modified=None):
        """Return the logged in user."""
        # GET /user
        url = '{}/user'.format(self.base_url)
        headers = self.headers.copy()
        if etag:
            headers['If-None-Match'] = etag
        elif last_modified:
            headers['If-Modified-Since'] = last_modified

        # get response
        response = self.get(url, headers=headers)
        user = response.json()

        # get etag
        headers = response.headers
        user['etag'] = headers['etag']

        if etag:
            # return response object instead of json
            return response

        return user

    def get_self_repos(self):
        """Return a list of user repos."""
        # GET /user/repos
        url = 'user/repos'
        return self.get_list(self.base_url, url)

    def get_self_teams(self):
        """Return a list of teams for the logged-in user."""
        # GET /user/teams - requires "user" or "repo" scope
        headers = {'Accept': 'application/vnd.github.hellcat-preview+json'}
        url = 'user/teams'
        return self.get_list(self.base_url, url, headers=headers)

    #
    # Users
    #
    def get_user(self, login, etag=None):
        """Return a single user."""
        # GET /users/:username
        url = '{}/users/{}'.format(self.base_url, login)
        headers = self.headers.copy()
        if etag:
            headers['If-None-Match'] = etag
            return self.get(url, headers=headers)
        return self.get(url, headers=headers).json()

    def get_user_repos(self, login):
        """Return a list of public repositories for the specified user."""
        # GET /users/:username/repos
        url = 'users/{}/repos'.format(login)
        return self.get_list(self.base_url, url)
