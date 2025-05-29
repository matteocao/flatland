from ..internal_representation.object_representation import \
    ObjectRepresentation


class SightSensorMixin:
    def sense_sight(self, perceivable_objects, snapshot):
        for obj in perceivable_objects:
            if obj is self:
                continue
            rep = self.internal_state.get_representation(obj, snapshot)
            rep.visible_size = getattr(obj, "size", None)
            rep.attractiveness = getattr(obj, "attractiveness", None)


class HearingSensorMixin:
    def sense_hearing(self, perceivable_objects, snapshot):
        for obj in perceivable_objects:
            if obj is self:
                continue
            rep = self.internal_state.get_representation(obj, snapshot)
            rep.noise_intensity = getattr(obj, "noise_intensity", None)
