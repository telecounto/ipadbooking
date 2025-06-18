# data.py
from models import iPad, Period

# Define available iPads
AVAILABLE_IPADS = [
    iPad(id="1", description="iPad 1"),
    iPad(id="2", description="iPad 2"),
    iPad(id="3", description="iPad 3"),
    iPad(id="5", description="iPad 5"),
    iPad(id="6", description="iPad 6"),
    iPad(id="19", description="iPad 19 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="20", description="iPad 20 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="21", description="iPad 21 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="22", description="iPad 22 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="23", description="iPad 23 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="24", description="iPad 24 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="25", description="iPad 25 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="26", description="iPad 26 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="27", description="iPad 27 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="28", description="iPad 28 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="29", description="iPad 29 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="30", description="iPad 30 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="31", description="iPad 31 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="32", description="iPad 32 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)"),
    iPad(id="33", description="iPad 33"),
    iPad(id="34", description="iPad 34"),
    iPad(id="35", description="iPad 35"),
    iPad(id="36", description="iPad 36"),
    iPad(id="37", description="iPad 37"),
    iPad(id="38", description="iPad 38"),
    iPad(id="39", description="iPad 39"),
    iPad(id="40", description="iPad 40"),
    iPad(id="41", description="iPad 41"),
    iPad(id="42", description="iPad 42"),
    iPad(id="43", description="iPad 43"),
    iPad(id="44", description="iPad 44"),
    iPad(id="45", description="iPad 45 E-Sports Club (Wed)"),
    iPad(id="46", description="iPad 46 E-Sports Club (Wed)"),
    iPad(id="47", description="iPad 47 E-Sports Club (Wed)"),
    iPad(id="48", description="iPad 48 E-Sports Club (Wed)"),
    iPad(id="49", description="iPad 49 E-Sports Club (Wed)"),
    iPad(id="50", description="iPad 50 E-Sports Club (Wed)"),
    iPad(id="51", description="iPad 51 E-Sports Club (Wed)"),
    iPad(id="52", description="iPad 52 E-Sports Club (Wed)"),
    iPad(id="53", description="iPad 53 E-Sports Club (Wed)"),
    iPad(id="54", description="iPad 54 E-Sports Club (Wed)"),
    iPad(id="55", description="iPad 55 E-Sports Club (Wed)"),
    iPad(id="56", description="iPad 56"),
    iPad(id="57", description="iPad 57 Robotics (After school Tue/Fri)"),
    iPad(id="58", description="iPad 58 Robotics (After school Tue/Fri)"),
    iPad(id="59", description="iPad 59 Robotics (After school Tue/Fri)"),
    iPad(id="60", description="iPad 60 Robotics (After school Tue/Fri)"),
    iPad(id="61", description="iPad 61 Robotics (After school Tue/Fri)"),
]

# Define available time periods
AVAILABLE_PERIODS = [
    Period(id="P1", start_time="08:10", end_time="09:00"),
    Period(id="P2", start_time="09:00", end_time="09:50"),
    Period(id="P3", start_time="10:00", end_time="10:50"),
    Period(id="P4", start_time="10:50", end_time="11:40"),
    Period(id="P5", start_time="11:40", end_time="12:30"),
    Period(id="P6", start_time="12:30", end_time="13:20"),
    Period(id="P7", start_time="13:30", end_time="14:20"),
    Period(id="P8", start_time="14:20", end_time="15:10"),
    Period(id="P9", start_time="15:30", end_time="16:20"),
]

# Example usage (optional, for testing data.py directly)
if __name__ == '__main__':
    print("Available iPads:")
    for ipad in AVAILABLE_IPADS:
        print(ipad)

    print("\nAvailable Periods:")
    for period in AVAILABLE_PERIODS:
        print(period)
