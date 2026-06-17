import cv2
import MotorModule as motor
import WebcamModule as cam
import UltrasonicModule as ultra
import LaneModule as lane
from PersonDetection import detectPerson

print("Autonomous Car Starting...")

try:
    while True:
        # --- Get Frame ---
        img = cam.getImg()
        if img is None:
            continue

        # --- Person Detection ---
        img, person_found = detectPerson(img)
        if person_found:
            print("Person Detected! Stopping.")
            motor.stop()
            cv2.imshow("Autonomous Car", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue  # skip lane/ultrasonic logic while person is present

        # --- Ultrasonic Distance ---
        distance = ultra.getDistance()

        if distance == -1:
            # Sensor timeout — no reading, drive cautiously
            print("Ultrasonic timeout, no reading.")
            motor.move(30, 0)
        elif distance < 20:
            # Obstacle too close
            print(f"Obstacle at {round(distance, 2)} cm — Stopping.")
            motor.stop()
        else:
            # --- Lane Following ---
            curve = lane.getLaneCurve(img)
            turn = curve * 0.15
            motor.move(50, turn)

        # --- Display ---
        cv2.imshow("Autonomous Car", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n Interrupted by user.")

except Exception as e:
    print(f"\n Unexpected error: {e}")

finally:
    print(" Cleaning up...")
    motor.stop()
    motor.cleanup()
    cv2.destroyAllWindows()
    print("Done.")