from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from orders.models import Booking, Installment
from projects.models import Project, Property

from orders.serializers import(
    BookingSerializer, 
)



class CreateBookingView(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            # Check if property is already booked
            property_obj = serializer.validated_data['property']
            if property_obj.status != 'available':
                return Response({"error": "Property is not available"}, status=status.HTTP_400_BAD_REQUEST)
            
            booking = serializer.save(user=request.user)
            
            # Update Property Status [cite: 43]
            property_obj.status = 'booked'
            property_obj.save()
            
            return Response({"message": "Booking initiated [cite: 53]"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        একজন ইউজার যদি এডমিন বা এমপ্লয়ি না হয়, 
        তবে সে শুধুমাত্র তার নিজের বুকিং করা লিস্ট দেখতে পাবে।
        """
        user = self.request.user
        if user.role in ['employee', 'marketing'] or user.is_staff:
            return Booking.objects.all().order_by('-booking_date')
        return Booking.objects.filter(user=user).order_by('-booking_date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "message": "Bookings retrieved successfully",
            "data": {
                "total_bookings": queryset.count(),
                "requests": serializer.data
            }
        }, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """
        বুকিং সেভ করার সময় অটোমেটিক প্রপার্টির স্ট্যাটাস 'booked' করে দিবে।
        """
        booking = serializer.save(user=self.request.user)
        
        # প্রপার্টি স্ট্যাটাস আপডেট
        property_obj = booking.property
        property_obj.status = 'booked'
        property_obj.save()

        # কন্ট্রাক্ট অনুযায়ী ইনস্টলমেন্ট শিডিউল তৈরি করা (ঐচ্ছিক লজিক)
        self.generate_installments(booking)

    def generate_installments(self, booking):
        """
        বুকিং কনফার্ম হওয়ার পর অটোমেটিক পরবর্তী ১০ মাসের কিস্তি তৈরি করার লজিক।
        """
        from datetime import date
        from dateutil.relativedelta import relativedelta

        for i in range(1, booking.installment_duration_months + 1):
            Installment.objects.create(
                booking=booking,
                amount=booking.monthly_installment_amount,
                due_date=date.today() + relativedelta(months=i)
            )