from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.contrib import messages
from .models import Link
from .serializers import LinkSerializer
import datetime
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Link
from django.utils.dateparse import parse_date
import openpyxl
from datetime import datetime
from django.contrib.messages import get_messages
from django.conf import settings
import os






@login_required
def home(request):
    links = Link.objects.all().order_by('-link_created')
    
    # Retrieve filter/search parameters
    start_date = request.GET.get('startDate', '').strip()
    end_date = request.GET.get('endDate', '').strip()
    link_type = request.GET.get('linkType', '').strip()
    search_target_link = request.GET.get('searchTargetLink', '').strip()

    # Apply date range filter if both dates are provided
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            links = links.filter(link_created__range=[start_date, end_date])
        except ValueError:
            # Handle invalid date format
            pass

    # Apply link type filter if provided and not the placeholder
    if link_type and link_type != "Choose...":
        links = links.filter(status_of_link=link_type)

    # Apply target link search if provided
    if search_target_link:
        links = links.filter(target_link__icontains=search_target_link)

    return render(request, 'link_crawler/home.html', {'links': links})


@require_http_methods(["GET", "POST"])
def add_links(request):
    if request.method == 'POST':
        if 'fileUpload' not in request.FILES:
            messages.error(request, "No file uploaded.")
            return redirect('add_links')
        
        excel_file = request.FILES.get('fileUpload')
        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, "File is not in the format of a .xlsx")
            return redirect('add_links')

        skipped_rows = []

        try:
            wb = openpyxl.load_workbook(excel_file, data_only=True)
            sheet = wb.active

            for index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                link_created = datetime(*row[4].timetuple()[:3]) if isinstance(row[4], datetime) else None

                # Check if a record with the same target_link, link_to, and anchor_text exists
                exists = Link.objects.filter(
                    target_link=row[2],
                    link_to=row[3],
                    anchor_text=row[1]
                ).exists()

                if exists:
                    # If a matching record exists, append a description to skipped_rows
                    skipped_rows.append({
                        'row': index-1,
                        'anchor': row[1],
                        'target_link': row[2],
                        'link_to': row[3],
                    })
                else:
                    # If no matching record exists, proceed to create a new record
                    Link.objects.create(
                        anchor_text=row[1],
                        target_link=row[2],
                        link_to=row[3],
                        link_created=link_created
                    )

            if skipped_rows:
                request.session['skipped_rows'] = skipped_rows  # Store skipped_rows in session
                messages.warning(request, "Some rows were skipped due to duplicates.")
            else:
                messages.success(request, "Excel file processed successfully")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('add_links')

    # Handle GET request: Retrieve skipped_rows from session and clear it
    skipped_rows = request.session.pop('skipped_rows', None)
    return render(request, "link_crawler/add_links.html", {'skipped_rows': skipped_rows})


def download_excel_template(request):
    # Define the path to the Excel file
    file_path = os.path.join(settings.BASE_DIR, 'links_upload_format.xlsx')
    
    # Check if file exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="links_upload_format.xlsx"'
            return response
    else:
        # You can return an HTTP 404 response if the file is not found
        # Or handle it some other way if you prefer
        return HttpResponse("The requested Excel template was not found.", status=404)

class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer



