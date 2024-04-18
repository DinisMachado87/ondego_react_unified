from rest_framework import serializers
from events.models import Event
from joinings.models import Joining


class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    joining_id = serializers.SerializerMethodField()
    joining_status = serializers.SerializerMethodField()
    joining_count = serializers.ReadOnlyField()
    let_me_see_count = serializers.ReadOnlyField()
    not_joining_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()


    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError(
                'Image file too large')
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width too large'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height too large'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.owner == request.user
    
    def get_joining_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            joining = Joining.objects.filter(
                event=obj, owner=user
            ).first()
            return joining.id if joining else None
        return None
    
    def get_joining_status(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            joining = Joining.objects.filter(
                event=obj, owner=user
            ).first()
            return joining.joining_status if joining else None
        return None

    class Meta:
        model = Event
        fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'what_title',
            'what_content',
            'where_place',
            'where_address',
            'when_start',
            'when_end',
            'intention',
            'event_image',
            'is_owner',
            'profile_id',
            'profile_image',
            'joining_id',
            'comments_count',
            # Joining counts and choices counts
            'joining_status',
            'joining_count',
            'let_me_see_count',
            'not_joining_count',
        ]
