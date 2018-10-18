from mosta.phone.models import Phone, ChargingHistory


def initiate_stop_charging(phone):
    ChargingHistory.objects.create(
        issuer=phone,
        issue_type=ChargingHistory.ISSUE_TYPE_ANNOUNCED_FULL_BATTERY,
        battery_state=phone.battery_level
    )

    loading_phones_count = Phone.objects.filter(
        owner=phone.owner,
        needs_charging=True,
        attached_power_socket=phone.attached_power_socket
    ).count()

    if loading_phones_count == 0 and phone.attached_power_socket:
        phone.attached_power_socket.active = False
        phone.attached_power_socket.save()
        for attached_phone in Phone.objects.filter(attached_power_socket=phone.attached_power_socket):
            ChargingHistory.objects.create(
                issuer=attached_phone,
                issue_type=ChargingHistory.ISSUE_TYPE_STOPPED_CHARGING,
                battery_state=attached_phone.battery_level
            )


def initiate_charging(phone):
    latest_charging_history = ChargingHistory.objects.filter(issuer=phone).order_by('-time')
    if latest_charging_history:
        latest_charging_history = latest_charging_history[0]

    if not latest_charging_history or (
            latest_charging_history.issue_type != ChargingHistory.ISSUE_TYPE_ANNOUNCED_CHARGING and
            latest_charging_history.issue_type != ChargingHistory.ISSUE_TYPE_REQUESTED_CHARGING
    ):
        if phone.attached_power_socket and phone.attached_power_socket.active:
            ChargingHistory.objects.create(
                issuer=phone,
                issue_type=ChargingHistory.ISSUE_TYPE_ANNOUNCED_CHARGING,
                battery_state=phone.battery_level
            )
        else:
            ChargingHistory.objects.create(
                issuer=phone,
                issue_type=ChargingHistory.ISSUE_TYPE_REQUESTED_CHARGING,
                battery_state=phone.battery_level
            )

    if phone.attached_power_socket:
        phone.attached_power_socket.active = True
        phone.attached_power_socket.save()
