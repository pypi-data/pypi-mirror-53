import math
from . import halo, disk


halo_virial_mass = 1e12  # [5e10, 1e13] Msol
disk_mass = 1e11  # [1.25e8, 5.3e11] Msol
max_radio_kpc = 16


def total_mass(radio_kpc):
    return halo_virial_mass + disk_mass * radio_kpc


def disk_mass_at_present_time(radio_kpc):
    return radio_kpc * disk_mass


def delta_total_mass(radio_kpc):
    return total_mass(radio_kpc) - total_mass(radio_kpc-1)


def delta_disk_mass(radio_kpc):
    return disk_mass_at_present_time(radio_kpc) - disk_mass_at_present_time(radio_kpc-1)


def collapse_time(radio_kpc):
    """ infall rate in Gyr """
    tau = -13.2 / math.log(1 - (delta_disk_mass(radio_kpc) / delta_total_mass(radio_kpc)))
    return tau
