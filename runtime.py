import time
import sys

# Define pulse timings (seconds)
SHORT_PULSE_DURATION = 0.1
LONG_PULSE_DURATION = 0.3
PAUSE_DURATION = 0.2
EMPHASIS_MULTIPLIER = 1.5

def play_pulse(symbol):
    """Simulate playing pulse based on symbol."""
    if symbol == '^':
        print("Beep (short)")
        time.sleep(SHORT_PULSE_DURATION)
    elif symbol == '~':
        print("Beep (long)")
        time.sleep(LONG_PULSE_DURATION)
    elif symbol == '*':
        print("Emphasis pulse")
        time.sleep(SHORT_PULSE_DURATION * EMPHASIS_MULTIPLIER)
    elif symbol == '_':
        print("Pause")
        time.sleep(PAUSE_DURATION)
    else:
        print("Unknown symbol:", symbol)
        time.sleep(PAUSE_DURATION)

def run_pulse_string(pulse_string):
    """Run the pulse string by simulating pulses."""
    # Remove brackets if any
    pulse_string = pulse_string.strip('[]')

    for symbol in pulse_string:
        play_pulse(symbol)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runtime.py '<pulse_string>'")
        print("Example: python runtime.py '[^^^_^~^]'")
        sys.exit(1)

    pulse_str = sys.argv[1]
    print(f"Running PulseLang: {pulse_str}")
    run_pulse_string(pulse_str)
    print("Done.")
