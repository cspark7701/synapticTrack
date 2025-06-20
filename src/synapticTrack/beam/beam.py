import pandas as pd
from periodictable import elements

def get_ion_species_name(mass_number, charge_state):
    """
        Determines the ion species name.

        Args:
            mass_number (int): Mass number.
            charge_state (int): Charge state.

        Returns:
            str: ion species name for given mass and charge.
        """
    # Approximate atomic number from mass (for common isotopes)
    # You may also provide atomic number directly if known
    # We simply find the nearest Z element with mass closest to A
    best_match = None
    best_diff = float('inf')
    
    for elem in elements:
        if elem.number and elem.mass:
            diff = abs(elem.mass - mass_number)
            if diff < best_diff:
                best_diff = diff
                best_match = elem
    
    if not best_match:
        raise ValueError(f"Could not find element for mass {mass_number}")

    symbol = best_match.symbol
    return f"{symbol}{charge_state}+"

class Beam:
    def __init__(self, state: pd.DataFrame, mass_number: int, charge_state: int, beam_current: float):
        """
        Initializes a Beam object.

        Args:
            state (pd.DataFrame): DataFrame representing the beam state.
            mass_number (int): Mass number of the ion species.
            charge_state (int): Charge state of the ion.
            beam_current (float): Beam current.
        """
        if not isinstance(state, pd.DataFrame):
            raise TypeError("state must be a pandas DataFrame")
        if state.empty:
            raise ValueError("state DataFrame cannot be empty")

        self._state = state
        self._mass_number = mass_number
        self._charge_state = charge_state
        self._beam_current = beam_current
        self._species = get_ion_species_name(mass_number, charge_state)

    @property
    def state(self):
        """Gets the beam state DataFrame."""
        return self._state

    @property
    def x(self):
        """Gets the x-coordinates from the beam state."""
        return self._state['x']

    @property
    def xp(self):
        """Gets the x' (x prime) coordinates."""
        return self._state['xp']

    @property
    def y(self):
        """Gets the y-coordinates."""
        return self._state['y']

    @property
    def yp(self):
        """Gets the y' (y prime) coordinates."""
        return self._state['yp']

    @property
    def dt(self):
        """Gets the time deviation."""
        return self._state['dt']

    @property
    def dW(self):
        """Gets the energy deviation."""
        return self._state['dW']

    @property
    def macroparticles(self):
        """Gets the number of macroparticles."""
        return self._state.shape[0]

    @property
    def species(self):
        """Gets the ion species."""
        return self._species

    @property
    def mass_number(self):
        """Gets the mass number."""
        return self._mass_number

    @property
    def charge_state(self):
        """Gets the charge state."""
        return self._charge_state

    @property
    def beam_current(self):
        """Gets the beam current."""
        return self._beam_current

    @property
    def centroid(self):
        """
        Computes the beam centroid (mean of x, xp, y, yp, dt, dW).

        Returns:
            pd.Series: Centroid values with keys ['x', 'xp', 'y', 'yp', 'dt', 'dW']
        """
        expected_columns = ['x', 'xp', 'y', 'yp', 'dt', 'dW']
        missing = [col for col in expected_columns if col not in self._state.columns]
        if missing:
            raise ValueError(f"Missing expected columns in beam state: {missing}")
        return self._state[expected_columns].mean()

    @property
    def rms_size(self):
        """
        Computes the RMS (standard deviation) of the beam distribution.

        Returns:
            pd.Series: RMS size for ['x', 'xp', 'y', 'yp', 'dt', 'dW']
        """
        expected_columns = ['x', 'xp', 'y', 'yp', 'dt', 'dW']
        missing = [col for col in expected_columns if col not in self._state.columns]
        if missing:
            raise ValueError(f"Missing expected columns in beam state: {missing}")
        return self._state[expected_columns].std()

