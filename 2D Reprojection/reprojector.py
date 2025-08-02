"""
2D Reprojection Module
Projects 3D points back to 2D image coordinates for verification.
"""

import cv2
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
import config


class StereoReprojector:
    """
    Reprojects 3D points to 2D image coordinates using stereo calibration.
    """

    def __init__(self, calibration_path=None):
        """
        Initialize reprojector with calibration data.

        Args:
            calibration_path (str): Path to calibration file (None = use config default)

        Raises:
            FileNotFoundError: If calibration file doesn't exist
        """
        calibration_path = calibration_path or config.CALIBRATION_DATA_PATH

        # Load calibration data
        self.calibration = self._load_calibration(calibration_path)

        # Extract projection matrices
        self.P1 = self.calibration['P1']
        self.P2 = self.calibration['P2']

        print(f"✓ Loaded calibration for reprojection from {calibration_path}")

    def _load_calibration(self, calibration_path):
        """
        Load calibration data from file.

        Args:
            calibration_path (str): Path to .npz calibration file

        Returns:
            dict: Calibration parameters

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        import os
        if not os.path.exists(calibration_path):
            raise FileNotFoundError(
                f"Calibration file not found: {calibration_path}\n"
                f"Run stereo_calibrate.py first to generate calibration data."
            )

        data = np.load(calibration_path)

        return {
            'P1': data['P1'],
            'P2': data['P2'],
        }

    def project_3d_to_2d(self, points_3d, camera='cam1'):
        """
        Project 3D points back to 2D image coordinates (reprojection).

        Args:
            points_3d (np.ndarray): Nx3 array of 3D points
            camera (str): 'cam1' or 'cam2' to select projection matrix

        Returns:
            np.ndarray: Nx2 array of reprojected 2D points

        Raises:
            ValueError: If camera not recognized
        """
        if camera == 'cam1':
            P = self.P1
        elif camera == 'cam2':
            P = self.P2
        else:
            raise ValueError(f"camera must be 'cam1' or 'cam2', got '{camera}'")

        # Convert to homogeneous coordinates (Nx4: [X, Y, Z, 1])
        n_points = len(points_3d)
        points_3d_homogeneous = np.hstack([points_3d, np.ones((n_points, 1))])

        # Project: P @ [X, Y, Z, 1]^T
        # P is 3x4, points is Nx4, so we transpose points for matrix multiplication
        projected_homogeneous = (P @ points_3d_homogeneous.T).T  # Nx3

        # Convert from homogeneous to 2D: [x/w, y/w]
        points_2d = projected_homogeneous[:, :2] / projected_homogeneous[:, 2:3]

        return points_2d.astype(np.float32)

    def reproject_to_both_cameras(self, points_3d):
        """
        Reproject 3D points to both camera views.

        Args:
            points_3d (np.ndarray): Nx3 array of 3D points

        Returns:
            tuple: (reprojected_cam1, reprojected_cam2) as Nx2 arrays
        """
        reprojected_cam1 = self.project_3d_to_2d(points_3d, camera='cam1')
        reprojected_cam2 = self.project_3d_to_2d(points_3d, camera='cam2')

        print(f"✓ Reprojected {len(points_3d)} points to both cameras")

        return reprojected_cam1, reprojected_cam2


def test_reprojection(calibration_path):
    """
    Test reprojection with synthetic 3D data.

    Args:
        calibration_path (str): Path to calibration file
    """
    print("="*60)
    print("Testing 2D Reprojection")
    print("="*60)

    # Initialize reprojector
    reprojector = StereoReprojector(calibration_path)

    # Create synthetic 3D point (nose tip at 60cm from cameras)
    points_3d = np.array([[0.0, 0.0, 0.6]], dtype=np.float32)  # X, Y, Z in meters

    print(f"\nTest 3D point: ({points_3d[0][0]:.2f}, {points_3d[0][1]:.2f}, {points_3d[0][2]:.2f}) m")

    # Reproject to both cameras
    repr_cam1, repr_cam2 = reprojector.reproject_to_both_cameras(points_3d)

    print(f"\nReprojected 2D coordinates:")
    print(f"  Camera 1: ({repr_cam1[0][0]:.1f}, {repr_cam1[0][1]:.1f}) pixels")
    print(f"  Camera 2: ({repr_cam2[0][0]:.1f}, {repr_cam2[0][1]:.1f}) pixels")

    print("\n✓ Reprojection test complete")
    print("="*60)


if __name__ == "__main__":
    """
    Test reprojection module.
    Usage: python reprojector.py [calibration_path]
    """
    import sys

    calibration_path = sys.argv[1] if len(sys.argv) > 1 else config.CALIBRATION_DATA_PATH

    try:
        test_reprojection(calibration_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nRun stereo calibration first:")
        print("  cd Calibration")
        print("  python stereo_calibrate.py --cam1 video1.mp4 --cam2 video2.mp4")
        sys.exit(1)
