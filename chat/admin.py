from django.contrib import admin
from . import models


admin.site.site_header = "Chat Bot Website Administration"


class BotAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "creator", "score"]
    list_filter = []
    search_fields = ("name",)

    fields = ("name", "title", "document_text", "is_active")

    def save_model(self, request, obj, form, change):
        if obj.creator is None:
            obj.creator = request.user
                
        if obj.score is None:
            obj.score = 0

        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(BotAdmin, self).get_queryset(request)
        
        return super(BotAdmin, self).get_queryset(request).filter(creator = request.user).filter(is_active = True)
        


class ConversationAdmin(admin.ModelAdmin):
    list_display = ["title", "bot", "last_message_date"]
    list_filter = ["bot", "last_message_date"]
    search_fields = ("title",)

    fields = ("title", "bot", "last_message_date")


class MessageAdmin(admin.ModelAdmin):
    list_display = ["message", "comment", "conversation"]
    list_filter = ["comment"]
    search_fields = ("message",)

    fields = ()


admin.site.register(models.Bot, BotAdmin)
admin.site.register(models.Conversation, ConversationAdmin)
admin.site.register(models.Message, MessageAdmin)
