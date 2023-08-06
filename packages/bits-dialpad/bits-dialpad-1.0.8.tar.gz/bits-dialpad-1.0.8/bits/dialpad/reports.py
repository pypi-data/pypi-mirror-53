# -*- coding: utf-8 -*-
"""Dialpad Reports class file."""

import datetime


class Reports(object):
    """Reports class."""

    def __init__(self, auth, dialpad):
        """Initialize a class instance."""
        self.auth = auth
        self.dialpad = dialpad
        self.verbose = dialpad.verbose

        self.now = datetime.datetime.now()

    def _get_calls(self, user):
        """Return the number of calls the user has made."""
        target_id = user['target_id']
        if target_id not in self.stats:
            return 0
        stats = self.stats[target_id]
        calls = 0
        for s in sorted(stats, key=lambda x: x['date']):
            calls += int(s['all_calls']) - int(s['abandoned'])
        return calls

    def _get_days_since_creation(self, user):
        """Return the number of days since the account was created."""
        date_added = datetime.datetime.strptime(user['date_added'], '%Y-%m-%d %H:%M:%S')
        delta = self.now - date_added
        return delta.days

    def _get_rooms(self):
        """Return a list of rooms."""
        rooms = {}
        for r in self.dialpad.get_rooms():
            target_id = r['target_id']
            rooms[target_id] = r
        return rooms

    def _get_stats(self):
        """Return stats as a dict by user."""
        data = self.dialpad.get_stats(days_ago_end=360)
        stats = {}
        for d in data:
            user_id = d['user_id']
            if user_id not in stats:
                stats[user_id] = []
            stats[user_id].append(dict(d))
        return stats

    def _get_usage_users(self):
        """Return a list of users and their usage."""
        usage_users = []
        db = self.auth.google().firestore('broad-bitsdb-firestore').db
        query = db.collection('dialpad_usage_users')
        for doc in query.stream():
            usage_users.append(doc.to_dict())
        return usage_users

    def usage_report(self):
        """Display details of a report of usage."""
        print('Getting stats from Dialpad API...')
        self.stats = self._get_stats()

        print('Getting users usage from Dialpad API...')
        usage_users = self._get_usage_users()
        print('Found {} Dialpad users usage.'.format(len(usage_users)))

        # reports
        rooms_no_calls_at_360 = []
        users_no_calls_at_180 = []
        users_no_calls_at_360 = []

        # check users
        for u in usage_users:
            user_type = u['type']
            calls = self._get_calls(u)
            days = self._get_days_since_creation(u)

            u['calls'] = calls
            u['days'] = days

            maxcalls = 0
            sixmonths = 180
            year = 360

            # check for users
            if user_type == 'user':

                # check users created more than 360 days ago with no calls
                if days > year and calls <= maxcalls:
                    users_no_calls_at_360.append(u)
                    continue

                # check users created more than 180 days ago with no calls
                if days > sixmonths and calls <= maxcalls:
                    users_no_calls_at_180.append(u)
                    continue

            # check for rooms
            elif user_type == 'room':

                # check rooms created more than 360 days ago with no calls
                if days > year and calls <= maxcalls:
                    rooms_no_calls_at_360.append(u)
                    continue

        if rooms_no_calls_at_360:
            print('\nRooms created >{} days ago and no calls:'.format(year))
        for u in rooms_no_calls_at_360:
            print('   {} <{}>: {} [{}]'.format(
                u['name'],
                u['primary_email'],
                u['date_added'],
                u['calls'],
            ))
            print(u)

        if users_no_calls_at_180:
            print('\nUsers created >{} days ago and no calls:'.format(sixmonths))
        for u in users_no_calls_at_180:
            print('   {} <{}>: {} [{}]'.format(
                u['name'],
                u['primary_email'],
                u['date_added'],
                u['calls'],
            ))

        if users_no_calls_at_360:
            print('\nUsers created >{} days ago and <={} calls:'.format(year, maxcalls))
        for u in users_no_calls_at_360:
            print('   {} <{}>: {} [{}]'.format(
                u['name'],
                u['primary_email'],
                u['date_added'],
                u['calls'],
            ))
