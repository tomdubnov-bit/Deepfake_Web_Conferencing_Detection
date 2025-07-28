README:


Multi-View Deepfake Integrity Check

Motivation: The $25 Million LessonIn early 2024, the multinational firm Arup suffered a staggering loss of approximately $25 million due to a sophisticated deepfake attack. An employee, initially suspicious of an email request, was convinced to authorize the transfers after attending a fake video conference. During the call, all participants—including the Chief Financial Officer and senior colleagues—were AI-generated deepfakes with perfectly cloned visuals and voices. This case proves that relying on visual recognition in a multi-person virtual environment is no longer safe.

Solution: Silo-Sight 
Silo-Sight tackles this threat by leveraging a core weakness of current deepfake technology: its struggle with geometric and 3D consistency across multiple simultaneous viewing angles.💡 Project Goal (3-Day POC): Apex-SightWe will build a Proof-of-Concept (POC) that acts as a "zero-trust" check for a person entering a secure virtual call. The system will use two webcams to continuously verify the physical location of a single, rigid facial feature.The principle is simple: A real nose tip, viewed from two fixed cameras, must always triangulate to a single, consistent 3D point in space. A deepfake, generated in 2D, will show measurable geometric inconsistencies when attempting to reconcile the two views.

Key Functionality
Dual-Camera Acquisition: Capture synchronized video streams from two cameras (e.g., placed at a $\approx 90^{\circ}$ angle).Stereo Calibration: Mathematically establish the fixed relationship between the two cameras (Intrinsic and Extrinsic parameters).Nose Tip Tracking: Use facial landmark detection to reliably find the 2D pixel coordinates of the Nose Tip in both video feeds.
Consistency Check: Implement the core logic to calculate the reprojection error between the actual tracked nose tip position and its mathematically predicted position in the second camera, based on the fixed calibration data.

Technical Stack

ComponentTechnology/LibraryPurposeLanguagePythonRapid prototyping and access to robust computer vision libraries.
Video ProcessingOpenCV (cv2)Camera stream acquisition, synchronization, and the full suite of Stereo Calibration functions (cv.calibrateCamera, cv.stereoCalibrate, etc.).Feature TrackingDlib / MediapipeFast and accurate facial landmark detection (specifically targeting the index for the Nose Tip).Data/MathNumPyHigh-performance numerical operations for matrix manipulation and error calculation.

Output & Measure of Success
Output
The system will continuously output a Confidence Score based on the computed geometric error.
Zero-Trust Score ($S_{C}$): A value from 0 to 100, representing the probability that the face is not a deepfake (i.e., its geometry is physically consistent).
Metric: The core metric is the Mean Reprojection Error in pixels.$$\text{Reprojection Error} (E_{pix}) = \text{Distance}(P_{actual}, P_{predicted})$$Error ConditionSC​ (Confidence Score)InterpretationReal Person$S_C \geq 90$Low error, consistent geometry. 
Verification PASSED.Deepfake/Inconsistency$S_C < 70$High, erratic error indicating geometric instability. 
Verification FAILED.Testing / Measuring SuccessBaseline Test (Success Criteria 1): Accurately calculate the average error $E_{real}$ (in pixels) for a live person across 30 seconds of video. $E_{real}$ should be low (e.g., $< 2.0$ pixels).Deepfake Test (Success Criteria 2): Run the system against a pre-recorded video of a known deepfake (or a synthetic video with known inconsistencies). The calculated error $E_{fake}$ must be measurably and consistently higher than the $E_{real}$ baseline (e.g., $E_{fake} > 2 \times E_{real}$).

Long-Term Vision (Beyond the Hackathon)
This POC is the foundation for a more powerful, general-purpose integrity engine.The ultimate long-term goal is to move from a simple geometric consistency check to full 3D head model reconstruction in real-time. By accurately triangulating the nose tip and a few other rigid landmarks (like the ear points or chin), we can create a truth anchor. The system could then:
Generate a low-fidelity 3D model of the user's head in real-time.Continuously project that 3D model back onto the two camera feeds.
Assert truth by checking if the live video and audio align perfectly with the derived 3D geometry—a task exponentially harder for deepfake generative models..