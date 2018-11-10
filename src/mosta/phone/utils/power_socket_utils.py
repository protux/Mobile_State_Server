from mosta.phone.models import PowerSocket, Phone


def needs_power_socket_activation(power_socket_id):
    try:
        power_socket = PowerSocket.objects.get(pk=power_socket_id)
    except PowerSocket.DoesNotExist:
        return False

    phones_to_charge = Phone.objects.filter(attached_power_socket=power_socket, needs_charging=True)
    return len(phones_to_charge) > 0
