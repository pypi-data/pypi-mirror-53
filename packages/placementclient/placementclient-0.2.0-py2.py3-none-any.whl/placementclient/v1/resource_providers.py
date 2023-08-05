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


class ResourceProvider(base.Resource):

    def __init__(self, manager, info, loaded=False, resp=None):
        super(ResourceProvider, self).__init__(manager, info, loaded, resp)
        self.id = self.uuid

    def usages(self):
        links = {x['rel']: x['href'].replace('/placement', '')
                 for x in self.links}
        return self.manager._get(links['usages'],
                                 response_key='usages',
                                 obj_class=Usage)

    def inventories(self):
        links = {x['rel']: x['href'].replace('/placement', '')
                 for x in self.links}
        return self.manager._get(links['inventories'],
                                 response_key='inventories',
                                 obj_class=Inventory)

    def allocations(self):
        return self.manager.allocations(self.id)


class Usage(base.Resource):
    pass


class Inventory(base.Resource):
    pass


class ResourceProviderManager(base.BasicManager):

    base_url = 'resource_providers'
    resource_class = ResourceProvider

    def list(self, **kwargs):
        return self._list('/%s' % self.base_url, params=kwargs,
                          response_key=self.base_url)

    def get(self, resource_id):
        return self._get('/%s/%s' % (self.base_url, resource_id))

    def delete(self, resource_id):
        return self._delete('/%s/%s' % (self.base_url, resource_id))

    def allocations(self, resource_id):
        return self._list('/%s/%s/allocations' % (self.base_url, resource_id),
                          response_key='allocations')
