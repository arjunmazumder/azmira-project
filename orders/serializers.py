from rest_framework import serializers
from orders.models import Booking, Installment


#-----------------InstallmentSerializer-----------------------------

class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = ['id', 'due_date', 'amount', 'is_paid', 'payment_date', 'transaction_id']

#-------------------Booking Serializer------------------------------

class BookingSerializer(serializers.ModelSerializer):
    # Display related data
    installments = InstallmentSerializer(many=True, read_only=True)
    user_email = serializers.ReadOnlyField(source='user.email')
    property_title = serializers.ReadOnlyField(source='property.title')

    class Meta:
        model = Booking
        fields = [
            'id', 'user_email', 'property', 'property_title', 
            'total_amount', 'token_money', 'down_payment', 
            'installment_duration_months', 'monthly_installment_amount', 
            'status', 'booking_date', 'token_expiration_date', 'installments'
        ]
        # Ensure installment amount is calculated by the model, not the user
        read_only_fields = ['monthly_installment_amount', 'status', 'booking_date']

    def validate(self, data):
        """
        Check that the token money meets the initial advance requirement.
        """
        if data['token_money'] < 25000:  # Based on contract advance requirement 
            raise serializers.ValidationError(
                {"token_money": "Initial advance must be at least BDT 25,000."}
            )
        return data