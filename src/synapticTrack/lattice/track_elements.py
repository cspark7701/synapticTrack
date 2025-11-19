# track_elements.py
import json

class Element:
    """Base class for all TRACK elements."""
    def __init__(self, name, elem_type, length):
        self.name = name
        self.elem_type = elem_type
        self.length = length

    def print_element(self):
        print(f"{self.elem_type.upper()} {self.name}")

    def to_line(self):
        raise NotImplementedError("Each element must implement its own TRACK line output.")

    def get_name(self):
        return self.name

    def get_type(self):
        return self.elem_type

    def get_length(self):
        return self.length

    # ------- NEW: JSON serialization helpers -------

    def to_dict(self):
        """Serialize common fields for JSON."""
        return {
            "elem_type": self.elem_type,
            "name": self.name,
            "length": self.length,
        }

    @staticmethod
    def from_dict(data: dict) -> "Element":
        """Factory: build the right Element subclass from a JSON dict."""
        etype = data["elem_type"].lower()
        name = data["name"]

        if etype == "drift":
            return Drift(
                name=name,
                length=data["length"],
                rx=data.get("rx", 0.0),
                ry=data.get("ry", 0.0),
                nstep=data.get("nstep"),
            )

        if etype == "bmag":
            return BMag(
                name=name,
                length=data["length"],
                rbend=data["rbend"],
                theta_deg=data["theta_deg"],
                airgap=data["airgap"],
                width=data["width"],
                beta1_deg=data["beta1_deg"],
                beta2_deg=data["beta2_deg"],
                r1_inv=data.get("r1_inv", 0.0),
                r2_inv=data.get("r2_inv", 0.0),
                nstep=data.get("nstep"),
            )

        if etype == "quad":
            return Quad(
                name=name,
                Bq_G=data["Bq_G"],
                length=data["length"],
                Heff=data["Heff"],
                Ra=data["Ra"],
                nstep=data.get("nstep", 10),
            )

        if etype == "equad":
            return EQuad(
                name=name,
                Vf=data["Vf"],
                length=data["length"],
                Heff=data["Heff"],
                Ra=data["Ra"],
                nstep=data.get("nstep", 10),
            )

        if etype == "stm":
            return Corr(
                name=name,
                length=data["length"],
                FH=data["FH"],
                FV=data["FV"],
                Ra=data.get("Ra", 0.0),
                nstep=data.get("nstep", 0),
                FHkick=data.get("FHkick", 0.0),
                FVkick=data.get("FVkick", 0.0),
            )

        if etype == "marker":
            return Marker(name=name)

        if etype == "scanner":
            return Scanner(name=name, scanner_type=data["scanner_type"])

        raise ValueError(f"Unsupported element type in JSON: {etype}")


class Drift(Element):
    def __init__(self, name, length, rx=0.0, ry=0.0, nstep=None):
        super().__init__(name, "drift", length)
        self.rx = rx
        self.ry = ry
        self.nstep = nstep

    def print_element(self):
        print(f"Drift {self.name}: L={self.length} cm, Rx={self.rx} cm, Ry={self.ry} cm, Steps={self.nstep}")

    def to_line(self):
        line = f"0    drift    {self.length:.6f}    {self.rx:.2f}    {self.ry:.2f}"
        if self.nstep:
            line += f"    {self.nstep}"
        return line

    def to_dict(self):
        d = super().to_dict()
        d.update({"rx": self.rx, "ry": self.ry, "nstep": self.nstep})
        return d


class BMag(Element):
    def __init__(self, name, length, rbend, theta_deg, airgap, width,
                 beta1_deg, beta2_deg, r1_inv=0.0, r2_inv=0.0, nstep=None):
        super().__init__(name, "bmag", length)
        self.rbend = rbend
        self.theta_deg = theta_deg
        self.airgap = airgap
        self.width = width
        self.beta1_deg = beta1_deg
        self.beta2_deg = beta2_deg
        self.r1_inv = r1_inv
        self.r2_inv = r2_inv
        self.nstep = nstep

    def print_element(self):
        print(
            f"BMag {self.name}: L={self.length} cm, R={self.rbend} cm, θ={self.theta_deg}°, "
            f"g={self.airgap} cm, w={self.width} cm, β1={self.beta1_deg}°, β2={self.beta2_deg}°, "
            f"R1⁻¹={self.r1_inv}, R2⁻¹={self.r2_inv}, Steps={self.nstep}"
        )


    def to_line(self):
        line = (
            f"0    bmag    {self.length:.6f}    {self.rbend:.6f}    {self.theta_deg:.2f}    "
            f"{self.airgap:.2f}    {self.width:.2f}    {self.beta1_deg:.4f}    {self.beta2_deg:.4f}"
        )
        if self.r1_inv or self.r2_inv or self.nstep:
            line += f"    {self.r1_inv:.4f}    {self.r2_inv:.4f}"
            if self.nstep:
                line += f"    {self.nstep}"
        return line

    def to_dict(self):
        d = super().to_dict()
        d.update(
            {
                "rbend": self.rbend,
                "theta_deg": self.theta_deg,
                "airgap": self.airgap,
                "width": self.width,
                "beta1_deg": self.beta1_deg,
                "beta2_deg": self.beta2_deg,
                "r1_inv": self.r1_inv,
                "r2_inv": self.r2_inv,
                "nstep": self.nstep,
            }
        )
        return d


class Quad(Element):
    def __init__(self, name, Bq_G, length, Heff, Ra, nstep=10):
        super().__init__(name, "quad", length)
        self.Bq_G = Bq_G
        self.Heff = Heff
        self.Ra = Ra
        self.nstep = nstep

    def print_element(self):
        print(f"Quad {self.name}: Bq={self.Bq_G} G, L={self.length} cm, Heff={self.Heff} cm, Ra={self.Ra} cm, Steps={self.nstep}")

    def to_line(self):
        return f"0    quad    {self.Bq_G:.2f}    {self.length:.6f}    {self.Heff:.6f}    {self.Ra:.2f}    {self.nstep}"

    def to_dict(self):
        d = super().to_dict()
        d.update(
            {
                "Bq_G": self.Bq_G,
                "Heff": self.Heff,
                "Ra": self.Ra,
                "nstep": self.nstep,
            }
        )
        return d


class EQuad(Element):
    def __init__(self, name, Vf, length, Heff, Ra, nstep=10):
        super().__init__(name, "equad", length)
        self.Vf = Vf
        self.Heff = Heff
        self.Ra = Ra
        self.nstep = nstep

    def print_element(self):
        print(f"EQuad {self.name}: Vf={self.Vf} V, L={self.length} cm, Heff={self.Heff} cm, Ra={self.Ra} cm, Steps={self.nstep}")

    def to_line(self):
        return f"0    equad    {self.Vf:.6f}    {self.length:.6f}    {self.Heff:.6f}    {self.Ra:.2f}    {self.nstep}"

    def to_dict(self):
        d = super().to_dict()
        d.update(
            {
                "Vf": self.Vf,
                "Heff": self.Heff,
                "Ra": self.Ra,
                "nstep": self.nstep,
            }
        )
        return d


class Corr(Element):
    def __init__(self, name, length, FH, FV, Ra=0, nstep=0, FHkick=0, FVkick=0):
        """
        n  CORR  L  FH FB rapC nstep FHkick FVkick
        FH[mrad]: maximum horizontal corrector strengths for transverse correction procedure if FHkick>0.
                  actual corrector strength if FHkick=0. 
        FV[mrad]: maximum vertical corretor strenghts for transverse correction procedure if FVkick>0.
                  actual corrector strength if FVkick=0.
        FHkick[mrad] : horizontal corrector strength for transfer function calculation.
        FVkick[mrad] : vertical corrector strength for transfer function calculation.
        """
        super().__init__(name, "stM", length=length)
        self.FH = FH
        self.FV = FV
        self.Ra = Ra
        self.nstep = nstep
        self.FHkick = FHkick
        self.FVkick = FVkick

    def print_element(self):
        print(
            f"Steering {self.name}: L={self.length} cm, FH={self.FH} mrad, FV={self.FV} mrad, "
            f"Ra={self.Ra} cm, Steps={self.nstep}, FHkick={self.FHkick} mrad, FVkick={self.FVkick} mrad"
        )

    def to_line(self):
        return (
            f"1    corr    {self.length:.6f}    {self.FH:.6f}    {self.FV:.6f}    {self.Ra:.2f}    "
            f"{self.nstep}    {self.FHkick}    {self.FVkick}"
        )

    def to_dict(self):
        d = super().to_dict()
        d.update(
            {
                "FH": self.FH,
                "FV": self.FV,
                "Ra": self.Ra,
                "nstep": self.nstep,
                "FHkick": self.FHkick,
                "FVkick": self.FVkick,
            }
        )
        return d


class Marker(Element):
    def __init__(self, name):
        super().__init__(name, "marker", length=0.0)

    def print_element(self):
        print(f"Marker {self.name}")

    def to_line(self):
        return f"0    marker"

    def to_dict(self):
        return super().to_dict()


class Scanner(Element):
    def __init__(self, name, scanner_type):
        super().__init__(name, "scanner", length=0.0)
        self.scanner_type = scanner_type

    def print_element(self):
        print(f"Scanner {self.name}: Type={self.scanner_type}")

    def to_line(self):
        return f"0    diagn    {self.scanner_type}    3"

    def to_dict(self):
        d = super().to_dict()
        d.update({"scanner_type": self.scanner_type})
        return d
