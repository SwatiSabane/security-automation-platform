from django.contrib import admin
from .models import Vulnerability


@admin.register(Vulnerability)
class VulnerabilityAdmin(admin.ModelAdmin):

    list_display = (
        'cve_id',
        'severity',
        'package_name',
        'status',
        'created_at'
    )

    search_fields = (
        'cve_id',
        'package_name'
    )

    list_filter = (
        'severity',
        'status'
    )

    ordering = (
        '-created_at',
    )