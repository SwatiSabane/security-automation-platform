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


def upload_report(request):

    message = None

    if request.method == 'POST':

        form = ReportUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            uploaded_file = request.FILES['report_file']

            save_path = os.path.join(
                'uploads',
                uploaded_file.name
            )

            # Save uploaded file
            with open(
                save_path,
                'wb+'
            ) as destination:

                for chunk in uploaded_file.chunks():

                    destination.write(chunk)

            # Read JSON file
            with open(
                save_path,
                'r',
                encoding='utf-8'
            ) as file:

                data = json.load(file)

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
                        "VulnerabilityID"
                    )

                    package = vuln.get(
                        "PkgName"
                    )

                    severity = vuln.get(
                        "Severity"
                    )

                    description = vuln.get(
                        "Title",
                        "No Description"
                    )

                    obj, created = Vulnerability.objects.get_or_create(
                        cve_id=cve,
                        defaults={
                            'package_name': package,
                            'severity': severity.title(),
                            'description': description,
                            'status': 'Open'
                        }
                    )

                    if created:
                        imported_count += 1
                        print(f"Saved: {cve}")

                    else:
                        skipped_count += 1
                        print(f"Skipped: {cve}")

            message = (
                f"Import Complete | "
                f"Imported: {imported_count} | "
                f"Skipped: {skipped_count}"
            )

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