from django.contrib import admin
from .models import PredictionHistory


@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'input_preview', 'prediction_label', 'confidence', 'created_at')
    search_fields = ('user__username', 'input_text', 'prediction_label')
    list_filter = ('prediction_label', 'created_at')

    @staticmethod
    def input_preview(obj):
        return f"{obj.input_text[:60]}..." if len(obj.input_text) > 60 else obj.input_text
