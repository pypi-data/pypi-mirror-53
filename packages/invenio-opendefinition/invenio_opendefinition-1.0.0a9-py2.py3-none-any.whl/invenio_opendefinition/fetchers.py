# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""PID fetchers for Invenio-OpenDefinition."""

from __future__ import absolute_import, print_function

from invenio_pidstore.fetchers import FetchedPID


def license_fetcher(record_uuid, data):
    """Fetch PID from license record."""
    return FetchedPID(
        provider=None,
        pid_type='od_lic',
        pid_value=str(data['id'])
    )
