"""A snapshot of current codenames.

Validated with the PermissionsInspector in tests and system checks.

"""

from edc_permissions.codenames import (
    account_manager,
    administration,
    data_manager,
    everyone,
    export,
    lab_view,
    pharmacy,
)
from edc_permissions.constants import (
    ACCOUNT_MANAGER,
    ADMINISTRATION,
    AUDITOR,
    CLINIC,
    DATA_MANAGER,
    EVERYONE,
    EXPORT,
    LAB,
    LAB_VIEW,
    PHARMACY,
    PII,
    PII_VIEW,
    UNBLINDING_REVIEWERS,
    UNBLINDING_REQUESTORS,
)


from ..group_names import RANDO, AE_REVIEW
from .ae import ae
from .ae_review import ae_review
from .auditor import auditor
from .clinic import clinic
from .lab import lab
from .pii_view import pii_view
from .pii import pii
from .rando import rando
from .screening import screening
from .tmg import tmg
from .unblinding import unblinding_requestors, unblinding_reviewers


CODENAMES = {
    ACCOUNT_MANAGER: account_manager,
    ADMINISTRATION: administration,
    AE_REVIEW: ae_review,
    AUDITOR: auditor,
    CLINIC: clinic,
    DATA_MANAGER: data_manager,
    EVERYONE: everyone,
    EXPORT: export,
    LAB: lab,
    LAB_VIEW: lab_view,
    PHARMACY: pharmacy,
    PII: pii,
    PII_VIEW: pii_view,
    RANDO: rando,
    UNBLINDING_REVIEWERS: unblinding_reviewers,
    UNBLINDING_REQUESTORS: unblinding_requestors,
}
