# -*- coding: utf-8 -*-
"""Quay class file."""

import requests


class Quay(object):
    """Quay class."""

    def __init__(self, token, orgname="broadinstitute", clientid=None, secret=None, verbose=False):
        """Initialize a Quay class instance."""
        # access token
        self.token = token

        # organization name
        self.orgname = orgname

        # oauth2 clientid and secret
        self.clientid = clientid
        self.secret = secret

        # set verbosity
        self.verbose = verbose

        # API base url
        self.base_url = 'https://quay.io/api/v1'

        # request headers
        self.headers = {
            'Authorization': 'Bearer %s' % (self.token)
        }

    def get(self, path, params=None):
        """Get a url path."""
        url = '%s/%s' % (self.base_url, path)
        return requests.get(url, headers=self.headers, params=params)

    #
    # Quay endpoints
    #
    def get_api_discovery(self):
        """Return a list of org invoices."""
        # GET /api/v1/discovery
        url = "discovery"
        return self.get(url).json()

    def get_org(self):
        """Return organization and teams."""
        # GET /api/v1/organization/{orgname}
        url = "organization/{}".format(self.orgname)
        return self.get(url).json()

    def get_org_applications(self):
        """Return a list of organization members."""
        # GET /api/v1/organization/{orgname}/applications
        url = 'organization/{}/applications'.format(self.orgname)
        return self.get(url).json().get('applications', [])

    def get_org_collaborators(self):
        """Return a list of organization collaborators."""
        # GET /api/v1/organization/{orgname}/collaborators
        url = 'organization/{}/collaborators'.format(self.orgname)
        return self.get(url).json().get('collaborators', [])

    def get_org_invoices(self):
        """Return a list of org invoices."""
        # GET /api/v1/organization/{orgname}/invoices
        url = "organization/{}/invoices".format(self.orgname)
        return self.get(url).json().get('invoices', [])

    def get_org_member(self, membername):
        """Return an organization member."""
        # GET /api/v1/organization/{orgname}/members/{membername}
        url = 'organization/{}/members/{}'.format(self.orgname, membername)
        return self.get(url).json()

    def get_org_members(self):
        """Return a list of organization members."""
        # GET /api/v1/organization/{orgname}/members
        url = 'organization/{}/members'.format(self.orgname)
        return self.get(url).json().get('members', [])

    def get_org_repos(self, public=False, starred=False):
        """Return a list of repos."""
        return self.get_repos(namespace=self.orgname, public=public, starred=starred)

    def get_org_teams(self):
        """Return a list of organization members."""
        return list(self.get_org()['teams'].values())

    def get_org_team_members(self, teamname):
        """Return a list of organization members."""
        # GET /api/v1/organization/{orgname}/team/{teamname}/members
        url = 'organization/{}/team/{}/members'.format(self.orgname, teamname)
        params = {
            'includePending': True,
        }
        return self.get(url, params=params).json().get('members', [])

    def get_org_team_permissions(self, teamname):
        """Return a list of organization permissions."""
        # GET /api/v1/organization/{orgname}/team/{teamname}/permissions
        url = 'organization/{}/team/{}/permissions'.format(self.orgname, teamname)
        return self.get(url).json().get('permissions', [])

    def get_repos(
        self,
        last_modified=None,
        namespace=None,
        popularity=None,
        public=False,
        repo_kind=None,
        starred=False
    ):
        """Return a list of repos."""
        # GET /api/v1/repository
        url = 'repository'
        params = {
            'last_modified': last_modified,
            'namespace': namespace,
            'popularity': popularity,
            'public': public,
            'repo_kind': repo_kind,
            'starred': starred,
        }
        return self.get(url, params=params).json().get('repositories', [])

    def get_user(self, username=None):
        """Return the current user."""
        # GET /api/v1/user - get current user
        # GET /api/v1/users/username - get named user
        url = 'user'
        if username:
            url = 'users/{}'.format(username)
        return self.get(url).json()
