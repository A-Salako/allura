#       Licensed to the Apache Software Foundation (ASF) under one
#       or more contributor license agreements.  See the NOTICE file
#       distributed with this work for additional information
#       regarding copyright ownership.  The ASF licenses this file
#       to you under the Apache License, Version 2.0 (the
#       "License"); you may not use this file except in compliance
#       with the License.  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#       Unless required by applicable law or agreed to in writing,
#       software distributed under the License is distributed on an
#       "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#       KIND, either express or implied.  See the License for the
#       specific language governing permissions and limitations
#       under the License.

import logging
import re
import sys
from pylons import tmpl_context as c
from bson import ObjectId
from ming.orm import ThreadLocalORMSession

from allura import model as M
from forgetracker import model as TM

log = logging.getLogger(__name__)


def main():
    task = sys.argv[-1]
    c.project = None

    # Fix ticket artifcat titles
    title = re.compile('(Ticket [0-9]+.*)')
    subs_tickets = M.Mailbox.query.find(dict(artifact_title=title)).all()
    print 'Found total %d old artifact titles (tickets).' % len(subs_tickets)
    for sub in subs_tickets:
        ticket = TM.Ticket.query.get(_id = ObjectId(sub.artifact_index_id.split('#')[1]))
        new_title = 'Ticket #%d: %s' % (ticket.ticket_num, ticket.summary)
        print '"%s" --> "%s"' % (sub.artifact_title , new_title)
        if(task != 'diff'):
            sub.artifact_title = new_title

    # Fix merge request artifact titles
    title = re.compile('(Merge request: .*)')
    subs_mrs = M.Mailbox.query.find(dict(artifact_title=title)).all()
    print 'Found total %d old artifact titles (merge_requests).' % len(subs_tickets)
    for sub in subs_mrs:
        merge_request = M.MergeRequest.query.get(_id = ObjectId(sub.artifact_index_id.split('#')[1]))
        new_title = 'Merge Request #%d: %s' % (merge_request.request_number, merge_request.summary)
        print '"%s" --> "%s"' % (sub.artifact_title , new_title)
        if(task != 'diff'):
            sub.artifact_title = new_title

    ThreadLocalORMSession.flush_all()

if __name__ == '__main__':
    main()
