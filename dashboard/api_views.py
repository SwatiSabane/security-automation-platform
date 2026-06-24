from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Vulnerability


@api_view(['POST'])
def upload_report_api(request):

    data = request.data

    imported_count = 0
    skipped_count = 0

    results = data.get("Results", [])

    for result in results:

        vulnerabilities = result.get(
            "Vulnerabilities",
            []
        )

        for vuln in vulnerabilities:

            cve = vuln.get("VulnerabilityID")

            package = vuln.get("PkgName")

            severity = vuln.get("Severity")

            description = vuln.get(
                "Title",
                "No Description"
            )

            obj, created = Vulnerability.objects.get_or_create(
                cve_id=cve,
                defaults={
                    "package_name": package,
                    "severity": severity.title(),
                    "description": description,
                    "status": "Open"
                }
            )

            if created:
                imported_count += 1
            else:
                skipped_count += 1

    return Response({
        "status": "success",
        "imported": imported_count,
        "skipped": skipped_count
    })