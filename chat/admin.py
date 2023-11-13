from django.contrib import admin
import models


admin.site.register(models.User)
admin.site.register(models.Bot)
admin.site.register(models.Conversation)
admin.site.register(models.Message)
