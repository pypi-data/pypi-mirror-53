#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from placementclient import base


class Allocation(base.Resource):
    pass


class AllocationManager(base.BasicManager):

    base_url = 'allocations'
    resource_class = Allocation

    def list(self, consumer_id):
        return self._list('/%s/%s' % (self.base_url, consumer_id),
                          response_key=self.base_url)

    def delete(self, consumer_id):
        return self._delete('/%s/%s' % (self.base_url, consumer_id))
