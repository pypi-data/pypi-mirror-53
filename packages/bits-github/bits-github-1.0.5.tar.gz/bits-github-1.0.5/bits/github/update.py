# -*- coding: utf-8 -*-
"""Update Class file."""


class Update(object):
    """Update class."""

    def __init__(self, auth, github):
        """Initialize a class instance."""
        self.auth = auth
        self.github = github
        self.verbose = auth.verbose

        # data
        self.github_ids = {}
        self.google_ids = {}
        self.people = {}
        self.role_accounts = {}
        self.users = {}

    def _get_github_role_accounts(self):
        """Return a dict of github role accounts by github ID."""
        role_accounts = {}
        for m in self.github.get_team_members(self.github.role_team):
            github_id = str(m['id'])
            role_accounts[github_id] = m
        return role_accounts

    def _get_github_team_invitations(self, team_id):
        """Return a dict fo github team invitations by login."""
        invitations = {}
        for i in self.github.get_team_invitations(team_id):
            login = i['login'].lower()
            invitations[login] = i
        return invitations

    def _get_github_team_members(self, team_id):
        """Return a dict of github team members by github ID."""
        members = {}
        for m in self.github.get_team_members(team_id):
            github_id = str(m['id'])
            members[github_id] = m
        return members

    def _get_google_group_members(self, email):
        """Return a list of members from a google group."""
        g = self.auth.google()
        g.auth_service_account(g.scopes, g.subject)
        return g.directory().get_derived_members(email)

    def _get_invitations(self):
        """Return a dict of invitations by GitHub ID."""
        invitations = {}
        for i in self.github.get_org_invitations():
            login = i['login'].lower()
            invitations[login] = i
        return invitations

    def _get_members(self):
        """Return a dict of members by GitHub ID."""
        members = {}
        for m in self.github.get_org_members():
            gid = u'{}'.format(m['id'])
            members[gid] = m
        return members

    def _get_new_logins(self, new):
        """Return a list of logins in the new users data."""
        logins = []
        for gid in new:
            n = new[gid]
            login = n['login'].lower()
            logins.append(login)
        return logins

    def _get_people(self):
        """Return a dict of people."""
        firestore = self.github.firestore(self.auth)
        self.people = firestore.get_people_dict(key='google_id')
        return self.people

    def _get_team_members_to_add(self, current, new, invitations):
        """Return a list of members to add to a team."""
        add = {}
        for github_id in new:
            n = new[github_id]
            login = n['login'].lower()
            if github_id not in current and login not in invitations:
                add[github_id] = new[github_id]
        return add

    def _get_team_members_to_remove(self, current, new, invitations):
        """Return a list of members to remove from a team."""
        remove = {}
        for github_id in current:
            c = current[github_id]
            login = c['login'].lower()
            if github_id not in new and login not in invitations and github_id not in self.role_accounts:
                remove[github_id] = current[github_id]
        return remove

    def _get_users(self):
        """Return a dict of users."""
        datastore = self.github.datastore(self.auth)
        self.users = datastore.get_users_dict()

        # get users by github_id and google_id
        self.github_ids = {}
        self.google_ids = {}
        for email in self.users:
            e = self.users[email]
            github_id = e['github_id']
            google_id = e['google_id']
            self.github_ids[github_id] = e
            self.google_ids[google_id] = e

        return self.users

    def _get_users_to_invite(self, current, new, invitations):
        """Return a list of logins to invite to the organization."""
        invite = []
        for gid in new:
            n = new[gid]
            login = n['login']
            if gid not in current:
                # make sure user doens't already have an invitation
                if login not in invitations:
                    invite.append(login)
        return invite

    def _get_users_to_remove(self, current, new):
        """Return a list of users to remove from the organization."""
        remove = []
        for gid in current:
            if gid not in new:
                login = current[gid]['login']
                remove.append(login)
        return remove

    def _get_users_to_uninvite(self, invitations, logins):
        """Return a list of users to uninvite from the organization."""
        uninvite = []
        for login in invitations:
            if login.lower() not in logins:
                uninvite.append(login)
        return uninvite

    def _prepare_members(self):
        """Prepare a list of org members for GitHub."""
        # get users that have linked their github account
        if not self.users:
            self.users = self._get_users()
        print('Found {} Tokens in GitHub App.'.format(len(self.users)))

        # get people
        if not self.people:
            self.people = self._get_people()
        print('Found {} People in BITSdb.'.format(len(self.people)))

        # get role_accounts
        if not self.role_accounts:
            role_accounts = self._get_github_role_accounts()
        print('Found {} GitHub Role Accounts.'.format(len(role_accounts)))

        members = {}

        # add github users who have linked their account and have a valid token
        for email in self.users:
            user = self.users[email]
            github_id = str(user['github_id'])
            google_id = user['google_id']
            if google_id not in self.people:
                # print('ERROR: Person not found: {}'.format(email))
                continue
            elif self.people[google_id]['terminated']:
                # print('WARNING: Person is terminated: {}'.format(email))
                continue
            members[github_id] = user

        # add in role accounts
        for github_id in role_accounts:
            user = role_accounts[github_id]
            members[github_id] = user

        return members

    def _prepare_team_members(self, group_members):
        """Covert Google Group Members to GitHub ID/logins."""
        team_members = {}
        for m in group_members:
            google_id = m['id']

            # check if google id has linked their account
            if google_id not in self.google_ids:
                # print('Google User not found: {} [{}]'.format(m['email'], google_id))
                continue

            # check if google id is in people
            if google_id not in self.people:
                print('Person not found: {} [{}]'.format(m['email'], google_id))
                continue

            # check if google id is terminated
            else:
                if self.people[google_id]['terminated']:
                    continue

            user = self.google_ids[google_id]
            github_id = user['github_id']
            team_members[github_id] = user

        return team_members

    def update_members(self):
        """Update members in GitHub."""
        current = self._get_members()
        print('Found {} current GitHub Members.'.format(len(current)))

        new = self._prepare_members()
        print('Found {} suitable GitHub Members.'.format(len(new)))

        invitations = self._get_invitations()
        print('Found {} open GitHub Invitations.'.format(len(invitations)))

        # get users to invite and remove from the org
        invite = self._get_users_to_invite(current, new, invitations)
        remove = self._get_users_to_remove(current, new)

        # check for invitations to cancel
        logins = self._get_new_logins(new)
        uninvite = self._get_users_to_uninvite(invitations, logins)

        if invite:
            print('\nMembers to invite: {}'.format(len(invite)))
            for login in sorted(invite):
                print('   + {}'.format(login))
                # self.github.invite_org_member(login)

        if remove:
            print('\nMembers to remove: {}'.format(len(remove)))
            for login in sorted(remove):
                print('   - {}'.format(login))
                # self.github.remove_org_member(login)

        if uninvite:
            print('\nInvitations to cancel: {}'.format(len(uninvite)))
            for login in sorted(uninvite):
                print('   - {}'.format(login))
                # self.github.remove_org_member(login)

        if self.verbose:
            print('Done updating GitHub members.')

    def update_team(self, slug, team_id, email):
        """Update a single team."""
        # get current team members
        current = self._get_github_team_members(team_id)

        # get open team invitations
        invitations = self._get_github_team_invitations(team_id)

        # get google group members
        group_members = self._get_google_group_members(email)

        # prepare google group members into github team members
        new = self._prepare_team_members(group_members)

        # get team members to add
        add = self._get_team_members_to_add(current, new, invitations)

        # get team members to remove
        remove = self._get_team_members_to_remove(current, new, invitations)

        if self.verbose or add or remove:
            print('\n{} [{}] <-- {}:'.format(
                slug,
                team_id,
                email,
            ))

        # display stats
        if self.verbose:
            print('   current: {}, group: {}, new: {}, invitations: {}'.format(
                len(current),
                len(group_members),
                len(new),
                len(invitations),
            ))

        # display any users to add
        if add:
            print('   members to add: {}'.format(len(add)))
            for github_id in sorted(add, key=lambda x: add[x]['login'].lower()):
                user = add[github_id]
                login = user['login'].lower()
                print('     + {} [{}]'.format(login, github_id))
                # add the github user to the team
                self.github.invite_team_member(team_id, login)

        # display any users to remove
        if remove:
            print('   members to remove: {}'.format(len(remove)))
            for github_id in sorted(remove, key=lambda x: remove[x]['login'].lower()):
                user = remove[github_id]
                login = user['login'].lower()
                print('     - {} [{}]'.format(login, github_id))
                # remove the github user from the team
                self.github.remove_team_member(team_id, login)

    def update_teams(self):
        """Update team membership in GitHub from Google Groups."""
        # get Broadies that have linked their GitHub accounts.
        if not self.users:
            self.users = self._get_users()
        print('Found {} Tokens in GitHub App.'.format(len(self.users)))

        # get role accounts
        if not self.role_accounts:
            self.role_accounts = self._get_github_role_accounts()
        print('Found {} Role Accounts in GitHub.'.format(len(self.role_accounts)))

        # firestore - get people
        if not self.people:
            self.people = self._get_people()
        print('Found {} People in BITSdb.'.format(len(self.people)))

        # firestore - get team syncs
        firestore = self.github.firestore(self.auth)
        team_syncs = firestore.get_team_syncs_dict()
        print('Found {} GitHub Team Syncs in BITSdb.'.format(len(team_syncs)))

        for slug in sorted(team_syncs):
            s = team_syncs[slug]
            team_id = s['github_team']
            email = s['google_group']
            self.update_team(slug, team_id, email)

        if self.verbose:
            print('Done updating GitHub teams.')
