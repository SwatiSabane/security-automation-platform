from django.shortcuts import render
from .models import Vulnerability
from .forms import ReportUploadForm
import json

def dashboard_home(request):

    total = Vulnerability.objects.count()

    critical = Vulnerability.objects.filter(
        severity='Critical'
    ).count()

    high = Vulnerability.objects.filter(
        severity='High'
    ).count()

    medium = Vulnerability.objects.filter(
        severity='Medium'
    ).count()

    low = Vulnerability.objects.filter(
        severity='Low'
    ).count()

    open_count = Vulnerability.objects.filter(
    status='Open').count()

    in_progress_count = Vulnerability.objects.filter(
        status='In Progress').count()

    resolved_count = Vulnerability.objects.filter(
        status='Resolved').count()

    vulnerabilities = Vulnerability.objects.all()
    recent_vulnerabilities = Vulnerability.objects.order_by(
    '-created_at'
)[:5]
    context = {
        'total': total,
        'critical': critical,
        'high': high,
        'medium': medium,
        'low': low,
        'vulnerabilities': vulnerabilities,
        'recent_vulnerabilities': recent_vulnerabilities,

        'open_count': open_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,


        'critical_count': critical,
        'high_count': high,
        'medium_count': medium,
        'low_count': low,

    }

    return render(
        request,
        'dashboard/home.html',
        context
    )

from .forms import ReportUploadForm
import os

from django.shortcuts import render
from .forms import ReportUploadForm
import os
import json

from django.shortcuts import render
from .forms import ReportUploadForm
from .models import Vulnerability

import os
import json

from django.shortcuts import render
from .forms import ReportUploadForm
from .models import Vulnerability
import json


def upload_report(request):

    message = None

    if request.method == 'POST':

        form = ReportUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            try:

                uploaded_file = request.FILES['report_file']

                # Read JSON directly from uploaded file
                data = json.load(uploaded_file)

                imported_count = 0
                skipped_count = 0

                results = data.get(
                    "Results",
                    []
                )

                for result in results:

                    vulnerabilities = result.get(
                        "Vulnerabilities",
                        []
                    )

                    for vuln in vulnerabilities:

                        cve = vuln.get(
                            "VulnerabilityID",
                            "UNKNOWN"
                        )

                        package = vuln.get(
                            "PkgName",
                            "Unknown Package"
                        )

                        severity = vuln.get(
                            "Severity",
                            "Unknown"
                        )

                        description = vuln.get(
                            "Title",
                            "No Description"
                        )

                        obj, created = Vulnerability.objects.get_or_create(
                            cve_id=cve,
                            defaults={
                                'package_name': package,
                                'severity': str(severity).title(),
                                'description': description,
                                'status': 'Open'
                            }
                        )

                        if created:
                            imported_count += 1
                        else:
                            skipped_count += 1

                message = (
                    f"Import Complete | "
                    f"Imported: {imported_count} | "
                    f"Skipped: {skipped_count}"
                )

            except Exception as e:

                message = f"Error: {str(e)}"

    else:

        form = ReportUploadForm()

    return render(
        request,
        'dashboard/upload.html',
        {
            'form': form,
            'message': message
        }
    )