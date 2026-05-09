from rest_framework import serializers
from .models import LeaveRequest

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(read_only=True)
    approved_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee', 'leave_type', 'start_date', 'end_date', 'reason', 'status', 'days_requested', 'approved_by', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['status', 'days_requested', 'approved_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        # employee will be set in the view
        return super().create(validated_data)

class LeaveDecisionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    comments = serializers.CharField(allow_blank=True, required=False)
