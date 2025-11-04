import os
import subprocess
from typing import List
from .track_elements import *


class Lattice(list):
    """A lattice consisting of a list of TRACK elements."""

    def __init__(self, elements=None):
        elements = elements or []
        if not all(isinstance(elem, Element) for elem in elements):
            raise TypeError("All elements must be instances of Element or its subclasses.")
        super().__init__(elements)

    def print_lattice(self):
        for i, elem in enumerate(self, start=1):
            print(f"{i:03d}. ", end="")
            elem.print_element()

    def write(self, filename="sclinac.dat", load_beam=None):
        with open(filename, "w") as f:
            if isinstance(load_beam, int):
                f.write(f"{load_beam}    scrch\n")

            for elem in self:
                f.write(elem.to_line() + "\n")

            if isinstance(load_beam, int):
                f.write(f"{-load_beam - 1}    scrch\n")
            f.write("0    stop")


    def parse(self, filename="sclinac.dat"):
        self.elements = []
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
 
                if not line or line.startswith("!"):
                    continue

                tokens = line.split()
                keyword = tokens[1].lower()

                if keyword == "drift":
                    elem = Drift(name="drift", length_cm=float(tokens[2]),
                                          rx_cm=float(tokens[3]), ry_cm=float(tokens[4]),
                                          nstep=int(tokens[5]) if len(tokens) > 5 else None)
                elif keyword == "bmag":
                    elem = BMag(name="bmag", length_cm=float(tokens[2]),
                                         rbend_cm=float(tokens[3]), theta_deg=float(tokens[4]),
                                         airgap_cm=float(tokens[5]), width_cm=float(tokens[6]),
                                         beta1_deg=float(tokens[7]), beta2_deg=float(tokens[8]),
                                         r1_inv=float(tokens[9]) if len(tokens) > 9 else 0.0,
                                         r2_inv=float(tokens[10]) if len(tokens) > 10 else 0.0,
                                         nstep=int(tokens[11]) if len(tokens) > 11 else None)
                elif keyword == "quad":
                    elem = Quad(name="quad", Bq_G=float(tokens[2]), length_cm=float(tokens[3]),
                                         Heff_cm=float(tokens[4]), Ra_cm=float(tokens[5]),
                                         nstep=int(tokens[6]))
                elif keyword == "equad":
                    elem = EQuad(name="equad", Vf=float(tokens[2]), length_cm=float(tokens[3]),
                                          Heff_cm=float(tokens[4]), Ra_cm=float(tokens[5]),
                                          nstep=int(tokens[6]))
                elif keyword == "marker":
                    elem = Marker(name="marker")
                elif keyword == "stM":
                    elem = SteeringMagnet(name="stM")
                elif keyword == "diagn":
                    elem = Scanner(name="diagn", scanner_type=str(tokens[2]))
                elif keyword == "scrch":
                    continue
                elif keyword == "stop":
                    continue
                else:
                    raise VlaueError(f"Unsupported element tyep: {keyword}")

                self.add_element(elem)
