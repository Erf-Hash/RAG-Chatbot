from django.contrib import admin
from . import models


admin.site.site_header = "Chat Bot Website Administration"

class BotAdmin(admin.ModelAdmin):
    list_display = ["name", "title"]
    list_filter = []
    search_fields = ('name',)

    fields = ("name", "title", "document_text")


admin.site.register(models.Bot, BotAdmin)
admin.site.register(models.Conversation)
admin.site.register(models.Message)
