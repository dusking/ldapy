from ldapobject import LdapObject
import user


class Group(LdapObject):

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        self._create_attribute_aliases()
        self._print_attributes = self._attributes_aliases.keys()
        self._print_attributes.extend(['mail', 'member'])

    def members(self):
        if 'member' not in self:
            return []
        result = []
        for member in self.member:
            result.append(user.User({'uid': self._extract_keys_from_dn(keys=['uid', 'cn'],
                                                                       distinguish_name=member),
                                     'distinguishedName': member}))
        return result

    def _create_attribute_aliases(self):
        self.set_attribute_aliases({
            'name': 'cn',
            'organization_unit': 'ou',
        })
        self.set_attribute_aliases({'unique_name': 'sAMAccountName'}) if 'sAMAccountName' in self \
            else self.set_attribute_aliases({'unique_name': 'uid'})
        self.set_attribute_aliases(self._aliases_to_cammelcase(['distinguishedName',
                                                                'objectCategory',
                                                                'objectClass']))