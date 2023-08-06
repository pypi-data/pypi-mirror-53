from sitri import Sitri
from sitri.contrib.system import SystemConfigProvider, SystemCredentialProvider

conf = Sitri(
    config_provider=SystemConfigProvider(project_prefix="scylla"),
    credential_provider=SystemCredentialProvider(project_prefix="scylla"),
)
