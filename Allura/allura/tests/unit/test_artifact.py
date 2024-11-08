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


from allura import model as M


class TestArtifact:

    def test_translate_query(self):
        fields = {'name_t': '', 'shortname_s': ''}
        query = 'name:1 AND shortname:2 AND shortname_name_field:3'
        q = M.Artifact.translate_query(query, fields)
        assert q == 'name_t:1 AND shortname_s:2 AND shortname_name_field:3'
