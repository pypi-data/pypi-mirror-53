from django.contrib.auth.models import Group
from edc_permissions.utils import add_permissions_to_group_by_codenames

from ..codenames import tmg
from ..group_names import TMG


def update_tmg_group_permissions():
    group_name = TMG
    group = Group.objects.get(name=group_name)
    group.permissions.clear()
    add_permissions_to_group_by_codenames(group, tmg)
    return group_name
