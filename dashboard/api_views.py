from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vulnerability


@api_view(['POST'])
def upload_report_api(request):

    print("=" * 50)
    print("API HIT FROM GITHUB ACTIONS")
    print("=" * 50)

    data = request.data

    imported_count = 0
    skipped_count = 0
    total_vulnerabilities = 0

    results = data.get("Results", [])

    print(f"Results found: {len(results)}")

    for result in results:

        target = result.get("Target", "Unknown")

        vulnerabilities = result.get(
            "Vulnerabilities",
            []
        )

        print("Vulnerabilities found:", len(vulnerabilities))
        print(vulnerabilities[:1])

        vuln_count = len(vulnerabilities)

        total_vulnerabilities += vuln_count

        print(
            f"Target: {target} | "
            f"Vulnerabilities: {vuln_count}"
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

    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Results Found: {len(results)}")
    print(f"Vulnerabilities Found: {total_vulnerabilities}")
    print(f"Imported: {imported_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Database Count: {Vulnerability.objects.count()}")

    return Response({
        "status": "SUCCESS_TEST",
        "message": "NEW CODE DEPLOYED",
        "results_found": len(results),
        "vulnerabilities_found": total_vulnerabilities,
        "imported": imported_count,
        "skipped": skipped_count,
        "database_count": Vulnerability.objects.count()
    })