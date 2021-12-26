"""Methods to check whether an installed engine version is compatible with recipes."""
import os
import subprocess

from honeybee_radiance.config import folders as rad_folders
from honeybee_energy.config import folders as energy_folders

# These constants set the engine version compatibility across the entire
# LBT Grasshopper plugin
RADIANCE_DATE = (2021, 3, 28)
EP_VERSION = (9, 6, 0)
OS_VERSION = (3, 3, 0)
COMPATIBILITY_URL = 'https://github.com/ladybug-tools/lbt-grasshopper/wiki/' \
    '1.4-Compatibility-Matrix'


def check_radiance_date():
    """Check if the installed version of Radiance is at or above the acceptable date."""
    rad_msg = 'Download and install the version of Radiance listed in the Ladybug ' \
        'Tools compatibility matrix\n{}'.format(COMPATIBILITY_URL)
    assert rad_folders.radiance_path is not None, \
        'No Radiance installation was found on this machine.\n{}'.format(rad_msg)
    rad_version = rad_folders.radiance_version_date
    if rad_version is None:
        rad_exe = os.path.join(rad_folders.radbin_path, 'rtrace.exe') if os.name == 'nt' \
            else os.path.join(self.radbin_path, 'rtrace')
        cmds = [rad_exe, '-version']
        use_shell = True if os.name == 'nt' else False
        process = subprocess.Popen(cmds, stderr=subprocess.PIPE, shell=use_shell)
        _, stderr = process.communicate()
        if stderr not in ('', b''):
            msg = 'A Radiance installation was found at {}\n' \
            'but the Radiance executables are not accessible.\n{}'.format(
                rad_folders.radbin_path, stderr)
            raise ValueError(msg)
        return None  # in case the issue was specifically with mkmap
    assert rad_version >= RADIANCE_DATE, \
        'The installed Radiance is from {}.\n Must be from from {} or later.\n{}'.format(
            '/'.join(str(v) for v in rad_version),
            '/'.join(str(v) for v in RADIANCE_DATE), rad_msg)


def check_openstudio_version():
    """Check if the installed version of OpenStudio is at or above the acceptable one."""
    in_msg = 'Download and install the version of OpenStudio listed in the Ladybug ' \
        'Tools compatibility matrix\n{}.'.format(COMPATIBILITY_URL)
    assert energy_folders.openstudio_path is not None, \
        'No OpenStudio installation was found on this machine.\n{}'.format(in_msg)
    os_version = energy_folders.openstudio_version
    if os_version is None:
        cmds = [energy_folders.openstudio_exe, 'openstudio_version']
        use_shell = True if os.name == 'nt' else False
        process = subprocess.Popen(cmds, stderr=subprocess.PIPE, shell=use_shell)
        _, stderr = process.communicate()
        msg = 'An OpenStudio installation was found at {}\n' \
            'but the OpenStudio executable is not accessible.\n{}'.format(
                energy_folders.openstudio_exe, stderr)
        raise ValueError(msg)
    assert os_version >= OS_VERSION, \
        'The installed OpenStudio is {}.\nMust be version {} or greater.\n{}'.format(
            '.'.join(str(v) for v in os_version),
            '.'.join(str(v) for v in OS_VERSION), in_msg)


def check_energyplus_version():
    """Check if the installed version of EnergyPlus is at or above the acceptable one."""
    in_msg = 'Get a compatible version of EnergyPlus by downloading and installing\n' \
        'the version of OpenStudio listed in the Ladybug Tools compatibility ' \
        'matrix\n{}.'.format(COMPATIBILITY_URL)
    assert energy_folders.energyplus_path is not None, \
        'No EnergyPlus installation was found on this machine.\n{}'.format(in_msg)
    ep_version = energy_folders.energyplus_version
    if ep_version is None:
        cmds = [energy_folders.energyplus_exe, '--version']
        use_shell = True if os.name == 'nt' else False
        process = subprocess.Popen(cmds, stderr=subprocess.PIPE, shell=use_shell)
        _, stderr = process.communicate()
        msg = 'An EnergyPlus installation was found at {}\n' \
            'but the EnergyPlus executable is not accessible.\n{}'.format(
                energy_folders.energyplus_exe, stderr)
        raise ValueError(msg)
    assert ep_version is not None and ep_version >= EP_VERSION, \
        'The installed EnergyPlus is {}.\nMust be version {} or greater.\n{}'.format(
            '.'.join(str(v) for v in ep_version),
            '.'.join(str(v) for v in EP_VERSION), in_msg)
