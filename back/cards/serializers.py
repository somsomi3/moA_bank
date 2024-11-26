from rest_framework import serializers
from .models import UserMakingCard, CardDesign

class CardDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDesign
        fields = ['id', 'image', 'name']


class CardSerializer(serializers.ModelSerializer):
    card_design = CardDesignSerializer()

    class Meta:
        model = UserMakingCard
        fields = [
            'id', 
            'card_name', 
            'card_image', 
            'notification', 
            'annual_fee', 
            'base_performance', 
            'base_performance_last', 
            'merit_summary', 
            'card_design',
        ]
