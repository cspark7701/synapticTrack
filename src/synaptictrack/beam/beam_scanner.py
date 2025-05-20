import pandas as pd

class BeamWS:
    def __init__(self, data, scan_id=None):
        """
        Initializes a BeamWS object for wire scanner data.

        Args:
            data (pd.DataFrame): DataFrame with wire scanner data.
                                 Required columns: ['x_pos', 'x_current', 'y_pos', 'y_current', 'd_pos', 'd_current']
            scan_id (str, optional): Identifier for this scan (e.g. filename, run ID, wire scanner label).
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")
        if data.empty:
            raise ValueError("data DataFrame cannot be empty")
        required_columns = ['x_pos', 'x_current', 'y_pos', 'y_current']
        if not set(required_columns).issubset(data.columns):
            raise ValueError(f"data must contain columns: {required_columns}")

        self._data = data
        self._scan_id = scan_id

    @property
    def data(self):
        """Returns full wire scanner data DataFrame."""
        return self._data

    @property
    def x_position(self):
        return self._data['x_pos']

    @property
    def x_current(self):
        return self._data['x_current']

    @property
    def y_position(self):
        return self._data['y_pos']

    @property
    def y_current(self):
        return self._data['y_current']

    @property
    def scan_id(self):
        return self._scan_id

    def num_points(self):
        """Returns number of measurement points."""
        return len(self._data)

    def describe(self):
        """Returns dictionary summary of scan."""
        return {
            "scan_id": self._scan_id,
            "points": self.num_points(),
            "x_range_mm": (self.x_position.min(), self.x_position.max()),
            "y_range_mm": (self.y_position.min(), self.y_position.max())
        }

class BeamAS:
    def __init__(self, data, scan_id=None):
        """
        Initializes a BeamAS object for 2D Alison scanner data.

        Args:
            data (pd.DataFrame): DataFrame with Alison scanner data.
                                 Required columns: ['x', 'xp', 'current']
            scan_id (str, optional): Identifier for this scan (e.g. filename, run ID).
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")
        if data.empty:
            raise ValueError("data DataFrame cannot be empty")
        required_columns = ['x', 'xp', 'x_current', 'hv', 'y_current']
        if not set(required_columns).issubset(data.columns):
            raise ValueError(f"data must contain columns: {required_columns}")

        self._data = data
        self._scan_id = scan_id

    @property
    def data(self):
        """Returns full Alison scanner DataFrame."""
        return self._data

    @property
    def x(self):
        return self._data['x']

    @property
    def xp(self):
        return self._data['xp']

    @property
    def x_current(self):
        return self._data['x_current']

    @property
    def hv(self):
        """Optional: high voltage applied [100 V units]."""
        return self._data['hv'] if 'hv' in self._data.columns else None

    @property
    def y_current(self):
        """Optional: Y plane current, if measured."""
        return self._data['y_current'] if 'y_current' in self._data.columns else None



    @property
    def scan_id(self):
        return self._scan_id

    def num_points(self):
        """Returns number of measurement points."""
        return len(self._data)

    def describe(self):
        """Returns dictionary summary of scan."""
        return {
            "scan_id": self._scan_id,
            "points": self.num_points(),
            "x_range_mm": (self.x.min(), self.x.max()),
            "xp_range_mrad": (self.xp.min(), self.xp.max()),
            "current_range_A": (self.x_current.min(), self.x_current.max())
        }

