from rest_framework import serializers

"""
member_id param is required. strategy param is optional, defaults to 'average'; this is 
where more strategies could be defined and validated.
"""


class GetDataSerializer(serializers.Serializer):
    VALID_STRATEGIES = ['average', 'sum', 'min', 'max']

    member_id = serializers.IntegerField(required=True)
    strategy = serializers.CharField(required=False, default='average')

    def validate_strategy(self, value):
        if value not in self.VALID_STRATEGIES:
            raise serializers.ValidationError(
                f"Invalid strategy. Please choose from: { ', '.join(self.VALID_STRATEGIES)}. Default strategy for missing argument is 'average'"
            )
        return value
