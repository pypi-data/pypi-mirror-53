from django.contrib import admin

from kitchensink.models import ArchieDoc, Sheet, Project

from django.contrib import admin


class ArchieDocAdmin(admin.ModelAdmin):
    fields = ("project", "title", "google_id", "version", "validation_schema")


class SheetsAdmin(admin.ModelAdmin):
    fields = ("project", "title", "google_id", "version", "validation_schema")


admin.site.register(Sheet, SheetsAdmin)
admin.site.register(ArchieDoc, ArchieDocAdmin)
admin.site.register(Project)
