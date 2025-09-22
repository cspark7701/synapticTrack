# track_elements.py

class Element:
    """Base class for all TRACK elements."""
    def __init__(self, name, elem_type):
        self.name = name
        self.elem_type = elem_type

    def print_element(self):
        print(f"{self.elem_type.upper()} {self.name}")

    def to_line(self):
        raise NotImplementedError("Each element must implement its own TRACK line output.")


class Drift(Element):
    def __init__(self, name, length_cm, rx_cm=0.0, ry_cm=0.0, nstep=None):
        super().__init__(name, "drift")
        self.length_cm = length_cm
        self.rx_cm = rx_cm
        self.ry_cm = ry_cm
        self.nstep = nstep

    def print_element(self):
        print(f"Drift {self.name}: L={self.length_cm} cm, Rx={self.rx_cm} cm, Ry={self.ry_cm} cm, Steps={self.nstep}")

    def to_line(self):
        line = f"0    drift    {self.length_cm:.6f}    {self.rx_cm:.2f}    {self.ry_cm:.2f}"
        if self.nstep:
            line += f"    {self.nstep}"
        return line


class BMag(Element):
    def __init__(self, name, length_cm, rbend_cm, theta_deg, airgap_cm, width_cm,
                 beta1_deg, beta2_deg, r1_inv=0.0, r2_inv=0.0, nstep=None):
        super().__init__(name, "bmag")
        self.length_cm = length_cm
        self.rbend_cm = rbend_cm
        self.theta_deg = theta_deg
        self.airgap_cm = airgap_cm
        self.width_cm = width_cm
        self.beta1_deg = beta1_deg
        self.beta2_deg = beta2_deg
        self.r1_inv = r1_inv
        self.r2_inv = r2_inv
        self.nstep = nstep

    def print_element(self):
        print(f"BMag {self.name}: L={self.length_cm} cm, R={self.rbend_cm} cm, θ={self.theta_deg}°, g={self.airgap_cm} cm, w={self.width_cm} cm, β1={self.beta1_deg}°, β2={self.beta2_deg}°, R1⁻¹={self.r1_inv}, R2⁻¹={self.r2_inv}, Steps={self.nstep}")


    def to_line(self):
        line = f"0    bmag    {self.length_cm:.6f}    {self.rbend_cm:.6f}    {self.theta_deg:.2f}    {self.airgap_cm:.2f}    {self.width_cm:.2f}    {self.beta1_deg:.4f}    {self.beta2_deg:.4f}"
        if self.r1_inv or self.r2_inv or self.nstep:
            line += f"    {self.r1_inv:.4f}    {self.r2_inv:.4f}"
            if self.nstep:
                line += f"    {self.nstep}"
        return line


class Quad(Element):
    def __init__(self, name, Bq_G, length_cm, Heff_cm, Ra_cm, nstep=10):
        super().__init__(name, "quad")
        self.Bq_G = Bq_G
        self.length_cm = length_cm
        self.Heff_cm = Heff_cm
        self.Ra_cm = Ra_cm
        self.nstep = nstep

    def print_element(self):
        print(f"Quad {self.name}: Bq={self.Bq_G} G, L={self.length_cm} cm, Heff={self.Heff_cm} cm, Ra={self.Ra_cm} cm, Steps={self.nstep}")

    def to_line(self):
        return f"0    quad    {self.Bq_G:.2f}    {self.length_cm:.6f}    {self.Heff_cm:.6f}    {self.Ra_cm:.2f}    {self.nstep}"


class EQuad(Element):
    def __init__(self, name, Vf, length_cm, Heff_cm, Ra_cm, nstep=10):
        super().__init__(name, "equad")
        self.Vf = Vf
        self.length_cm = length_cm
        self.Heff_cm = Heff_cm
        self.Ra_cm = Ra_cm
        self.nstep = nstep

    def print_element(self):
        print(f"EQuad {self.name}: Vf={self.Vf} V, L={self.length_cm} cm, Heff={self.Heff_cm} cm, Ra={self.Ra_cm} cm, Steps={self.nstep}")

    def to_line(self):
        return f"0    equad    {self.Vf:.6f}    {self.length_cm:.6f}    {self.Heff_cm:.6f}    {self.Ra_cm:.2f}    {self.nstep}"

class SteeringManget(Element):
    def __init__(self, name, hkick, vkick):
        super().__init__(name, "stM")
        self.hkick = hkick
        slef.vkick = vkick

    def print_element(self):
        print(f"Steering {self.name}: HKick={self.hkick}, VKick={self.vkick}")

    def to_line(self):
        return f"0    stM    {self.hkick:.6f}    {self.vkick:.6f}"

class Marker(Element):
    def __init__(self, name):
        super().__init__(name, "marker")

    def print_element(self):
        print(f"Marker {self.name}")

    def to_line(self):
        return f"0    marker"

class Scanner(Element):
    def __init__(self, name, scanner_type):
        super().__init__(name, "scanner")
        self.scanner_type = scanner_type

    def print_element(self):
        print(f"Scanner {self.name}: Type={self.scanner_type}")


    def to_line(self):
        return f"0    diagn    {self.scanner_type}    3"

