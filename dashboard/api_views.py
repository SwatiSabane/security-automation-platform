from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Vulnerability


@api_view(['POST'])
def upload_report_api(request):

    print("=" * 50)
    print("API HIT FROM GITHUB ACTIONS")
    print("=" * 50)

    data = request.data

    print("Top-level keys:")
    print(data.keys())

    imported_count = 0
    skipped_count = 0

    results = data.get("Results", [])

    print(f"Results found: {len(results)}")

    for result in results:

        target = result.get("Target", "Unknown")

        vulnerabilities = result.get(
            "Vulnerabilities",
            []
        )

        print(
            f"Target: {target} | "
            f"Vulnerabilities: {len(vulnerabilities)}"
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
                    "package_name": package,
                    "severity": str(severity).title(),
                    "description": description,
                    "status": "Open"
                }
            )

            if created:
                imported_count += 1
                print(f"Imported: {cve}")

            else:
                skipped_count += 1
                print(f"Skipped: {cve}")

    print(
        f"Final Result -> Imported: {imported_count}, "
        f"Skipped: {skipped_count}"
    )
    print("Total records:", Vulnerability.objects.count())
    return Response({
    "status": "SUCCESS_TEST",
    "message": "NEW CODE DEPLOYED",
    "imported": imported_count,
    "skipped": skipped_count,
    "database_count": Vulnerability.objects.count()
})