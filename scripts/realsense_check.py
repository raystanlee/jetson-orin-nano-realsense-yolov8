import pyrealsense2 as rs

pipeline = rs.pipeline()

try:
    pipeline.start()
    print("RealSense pipeline started successfully.")
except Exception as e:
    print("Error starting RealSense:", e)
finally:
    pipeline.stop()