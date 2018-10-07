from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOfSim(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sim.owner == request.user


class IsOwnerOfIssuer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.phone.issuer == request.user
