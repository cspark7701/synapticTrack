import os
import json
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

    def write(self, filename: str = "sclinac.dat", load_beam=None):
        """
        Write lattice in TRACK format to the given filename.
        load_beam : int
            Initial beam distribution number
            Will be used for output beam distribution number (load_beam + 1)
        """
        with open(filename, "w") as f:
            if isinstance(load_beam, int):
                f.write(f"{load_beam}    scrch\n")

            for elem in self:
                f.write(elem.to_line() + "\n")

            if isinstance(load_beam, int):
                f.write(f"{-load_beam - 1}    scrch\n")

            f.write("0    stop")

    def write_stl(self, filename: str, load_beam=None):
        """
        Write lattice to a file with .stl extension, using TRACK text format.

        Parameters
        ----------
        filename : str
            Base filename or path. If it does not end with '.stl', the extension
            will be appended automatically.
        load_beam : int or None
            Optional TRACK 'scrch' control flag, passed through to write().
        """
        base, ext = os.path.splitext(filename)
        if ext.lower() != ".stl":
            filename = base + ".stl"
        self.write(filename=filename, load_beam=load_beam)

    def to_json(self, filename: str):
        """
        Save lattice to a JSON file.

        The file will contain a list of element dictionaries.
        """
        data = [elem.to_dict() for elem in self]
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def from_json(cls, filename: str) -> "Lattice":
        """
        Load a lattice from a JSON file created by to_json().
        """
        with open(filename, "r") as f:
            data = json.load(f)

        lattice = cls()
        for elem_dict in data:
            elem = Element.from_dict(elem_dict)
            lattice.append(elem)
        return lattice

    @classmethod
    def parse(cls, filename: str = "sclinac.dat"):
        """
        Parse a TRACK lattice file and return a Lattice instance.

        Raises ValueError (or IndexError) on malformed lines.
        """
        lattice = cls()

        with open(filename, "r") as f:
            for lineno, line in enumerate(f, start=1):
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("!"):
                    continue

                tokens = line.split()

                # Need at least an index + keyword
                if len(tokens) < 2:
                    raise ValueError(f"Malformed lattice line {lineno}: {line}")

                keyword = tokens[1].lower()

                try:
                    if keyword == "drift":
                        # index  keyword  L(cm)  Rx(cm)  Ry(cm)  nstep(optional)
                        if len(tokens) < 5:
                            raise ValueError
                        elem = Drift(
                            name="drift",
                            length=float(tokens[2]),
                            rx=float(tokens[3]),
                            ry=float(tokens[4]),
                            nstep=int(tokens[5]) if len(tokens) > 5 else None,
                        )

                    elif keyword == "bmag":
                        # index  keyword  L  Rbend  theta  gap  width  beta1  beta2 [r1_inv] [r2_inv] [nstep]
                        if len(tokens) < 9:
                            raise ValueError
                        elem = BMag(
                            name="bmag",
                            length=float(tokens[2]),
                            rbend=float(tokens[3]),
                            theta_deg=float(tokens[4]),
                            airgap=float(tokens[5]),
                            width=float(tokens[6]),
                            beta1_deg=float(tokens[7]),
                            beta2_deg=float(tokens[8]),
                            r1_inv=float(tokens[9]) if len(tokens) > 9 else 0.0,
                            r2_inv=float(tokens[10]) if len(tokens) > 10 else 0.0,
                            nstep=int(tokens[11]) if len(tokens) > 11 else None,
                        )

                    elif keyword == "quad":
                        # index  keyword  Bq  L  Heff  Ra  nstep
                        if len(tokens) < 7:
                            raise ValueError
                        elem = Quad(
                            name="quad",
                            Bq_G=float(tokens[2]),
                            length=float(tokens[3]),
                            Heff=float(tokens[4]),
                            Ra=float(tokens[5]),
                            nstep=int(tokens[6]),
                        )

                    elif keyword == "equad":
                        # index  keyword  Vf  L  Heff  Ra  nstep
                        if len(tokens) < 7:
                            raise ValueError
                        elem = EQuad(
                            name="equad",
                            Vf=float(tokens[2]),
                            length=float(tokens[3]),
                            Heff=float(tokens[4]),
                            Ra=float(tokens[5]),
                            nstep=int(tokens[6]),
                        )

                    elif keyword == "marker":
                        elem = Marker(name="marker")

                    elif keyword == "stm":  # 'stM' -> lowered to 'stm'
                        elem = SteeringMagnet(name="stm")

                    elif keyword == "diagn":
                        # index  keyword  type
                        if len(tokens) < 3:
                            raise ValueError
                        elem = Scanner(name="diagn", scanner_type=str(tokens[2]))

                    elif keyword in {"scrch", "stop"}:
                        # TRACK control lines; skip
                        continue

                    else:
                        raise ValueError(f"Unsupported element type: {keyword}")

                except (IndexError, ValueError) as exc:
                    # Wrap any parsing issues as ValueError with line info
                    raise ValueError(
                        f"Malformed lattice line {lineno}: {line}"
                    ) from exc

                lattice.append(elem)

        return lattice
