from datetime import datetime, timedelta


def get_available_slots(busy_slots, date_str, service_duration):
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    work_start = datetime.combine(date, datetime.strptime('09:00', '%H:%M').time())
    work_end = datetime.combine(date, datetime.strptime('20:00', '%H:%M').time())
    slot_duration = timedelta(minutes=30)

    all_slots = []
    current = work_start
    while current < work_end:
        all_slots.append(current)
        current += slot_duration

    available_slots = []
    for slot in all_slots:
        is_available = True
        for busy_start, duration in busy_slots:
            if busy_start and duration:
                busy_end = busy_start + timedelta(minutes=duration)
                if busy_start <= slot < busy_end:
                    is_available = False
                    break
        if is_available:
            available_slots.append(slot.strftime('%Y-%m-%dT%H:%M'))

    return available_slots
