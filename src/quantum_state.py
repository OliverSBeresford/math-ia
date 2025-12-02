import numpy as np

class QuantumState:
    """Class representing a quantum state vector."""
    def __init__(self, theta=None, phi=None):
        # If vector is not provided, initialize from Bloch angles theta and phi
        if theta is not None and phi is not None:
            # Save variables to the object
            self.vector = self.angles_to_vector(theta, phi)
            self.theta = theta
            self.phi = phi
        else:
            raise ValueError("Both theta and phi must be provided.")
    
        # Ensure the state vector is a numpy array and normalized
        self.vector = np.array(self.vector, dtype=complex)
        self.normalize()

    def angles_to_vector(self, theta, phi):
        """Convert Bloch angles theta and phi to a state vector."""
        a = np.cos(theta / 2)
        b = np.sin(theta / 2) * complex(real=np.cos(phi), imag=np.sin(phi))
        return np.array([a, b], dtype=complex)
    
    def vector_to_angles(self):
        """Convert the state vector back to Bloch angles theta and phi."""
        alpha, beta = self.vector
        # theta depends on the magnitude of alpha: |alpha| = cos(theta/2)
        a_abs = np.abs(alpha)
        theta = 2 * np.arccos(a_abs)

        # phi is the relative phase between beta and alpha: phi = arg(beta) - arg(alpha)
        # If sin(theta/2) is (nearly) zero then the global phase is ambiguous; set phi=0
        sin_half = np.sin(theta / 2)
        if abs(sin_half) < 1e-12:
            phi = 0.0
        else:
            phi = np.angle(beta) - np.angle(alpha)
            # normalize to [0, 2*pi)
            phi = (phi + 2 * np.pi) % (2 * np.pi)

        return theta, phi
    
    def normalize(self):
        norm = np.linalg.norm(self.vector)
        if norm == 0:
            raise ValueError("Cannot normalize the zero vector.")
        self.vector /= norm

    def apply_gate(self, gate):
        """Apply a quantum gate (2x2 matrix) to the state."""
        self.vector = gate.dot(self.vector)
        # self.normalize()
        self.theta, self.phi = self.vector_to_angles()

    def bloch_coordinates(self):
        """Return the Bloch sphere coordinates (x, y, z) of the state."""
        alpha, beta = self.vector
        x = np.sin(self.theta) * np.cos(self.phi)
        y = np.sin(self.theta) * np.sin(self.phi)
        z = np.cos(self.theta)
        return np.array([x, y, z])
    
    def rotate_x(self, angle):
        """Rotate the state by 'angle' radians about the x-axis."""
        rx = np.array([[np.cos(angle / 2), -1j * np.sin(angle / 2)],
                       [-1j * np.sin(angle / 2), np.cos(angle / 2)]], dtype=complex)
        self.apply_gate(rx)
        
        return self.bloch_coordinates()
    
    def rotate_y(self, angle):
        """Rotate the state by 'angle' radians about the y-axis."""
        ry = np.array([[np.cos(angle / 2), -np.sin(angle / 2)],
                       [np.sin(angle / 2), np.cos(angle / 2)]], dtype=complex)
        self.apply_gate(ry)
        
        return self.bloch_coordinates()
    
    def rotate_z(self, angle):
        """Rotate the state by 'angle' radians about the z-axis."""
        rz = np.array([[np.exp(-1j * angle / 2), 0],
                       [0, np.exp(1j * angle / 2)]], dtype=complex)
        self.apply_gate(rz)
        
        return self.bloch_coordinates()
    
    def __str__(self):
        return f"QuantumState(vector={self.vector}, theta={self.theta}, phi={self.phi})"