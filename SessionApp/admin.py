from django.contrib import admin
from .models import Session
from ConferenceApp.models import submission
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'conference', 'session_day', 'start_time', 'end_time', 'room', 'duration')
    list_filter = ('conference', 'session_day', 'room')
    search_fields = ('title', 'topic', 'conference__name')
    date_hierarchy = 'session_day'
    autocomplete_fields = ['conference']
    
    def duration(self, obj):
        """Calcule la durée de la session"""
        if obj.start_time and obj.end_time:
            # Calcul plus précis de la durée
            from datetime import datetime
            start_dt = datetime.combine(obj.session_day, obj.start_time)
            end_dt = datetime.combine(obj.session_day, obj.end_time)
            delta = end_dt - start_dt
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            if minutes > 0:
                return f"{hours}h{minutes:02d}"
            return f"{hours}h"
        return "N/A"
    duration.short_description = "Durée"

