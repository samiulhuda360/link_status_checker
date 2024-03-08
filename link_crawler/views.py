from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
from rest_framework import viewsets
from django.contrib import messages
from .models import Link
from .serializers import LinkSerializer
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from .models import Link
from django.utils.dateparse import parse_date
import openpyxl
from datetime import datetime
from django.contrib.messages import get_messages
from django.conf import settings
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.utils.timezone import now




@login_required
def home(request):
    # Start with the base queryset
    links_queryset = Link.objects.filter(user=request.user).order_by('-link_created')    
    # Retrieve filter/search parameters
    start_date = request.GET.get('startDate', '').strip()
    end_date = request.GET.get('endDate', '').strip()
    link_type = request.GET.get('linkType', '').strip()
    index_status = request.GET.get('index_status', '').strip()
    print("Index status:",index_status)

    search_target_link = request.GET.get('searchTargetLink', '').strip()

    # Apply date range filter if both dates are provided
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            links_queryset = links_queryset.filter(link_created__range=[start_date, end_date])
        except ValueError:
            # Handle invalid date format
            pass

    # Apply link type filter if provided and not the placeholder
    if link_type and link_type != "Choose...":
        links_queryset = links_queryset.filter(status_of_link=link_type)
    
    if index_status and index_status != "Choose...":
        links_queryset = links_queryset.filter(index_status=index_status)

    # Apply target link search if provided
    if search_target_link:
        links_queryset = links_queryset.filter(target_link__icontains=search_target_link)
        
    total_links = links_queryset.count()
    # Get 'per_page' from GET parameters or default to 20, and make sure it's an integer
    per_page = int(request.GET.get('per_page', 20))

    # Instantiate the Paginator
    paginator = Paginator(links_queryset, per_page)

    # Get the page number from the request
    page = request.GET.get('page', 1)
    try:
        links = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        links = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        links = paginator.page(paginator.num_pages)

    return render(request, 'link_crawler/home.html', {
        'links': links,
        'per_page': per_page,
        'current_page': int(page),
        'total_links': total_links, 
    })
    
    
@login_required
def handle_actions(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        print(action)
        selected_ids = request.POST.getlist('selected_links')

        if action == 'download':
            # Assuming download_status_report returns an HttpResponse object
            return download_status_report(request, selected_ids)
        elif action == 'delete':
            # Assuming delete_links performs deletion and then returns an HttpResponse object
            return delete_links(request, selected_ids)
        elif action == 'mark_addressed':
            return mark_links_as_addressed(request, selected_ids)
        else:
            # If the action is not recognized, redirect to a default page or show an error message
            return HttpResponseRedirect(reverse('home'))

    # If the request method is not POST, redirect to a default page or show an error message
    return HttpResponseRedirect(reverse('home'))

def download_status_report(request, selected_links_ids):
    # Create a new Excel workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # Define the title of the worksheet
    ws.title = "Links Status Report"

    # Set the header row
    headers = ['Target Link', 'Referring Domain', 'Anchor', 'Status Of Link', 'Is Index', 'Link Created', 'Last Crawled']
    ws.append(headers)
    # Fetch the selected links from the database
    selected_links = Link.objects.filter(id__in=selected_links_ids)

    # Iterate over the queryset and append rows to the worksheet
    for link in selected_links:
        if link.index_status == Link.index:
            is_index = 'Yes' 
        elif link.index_status == Link.not_index:
            is_index = 'No' 
        else:
            is_index = 'Unknown' 
        # Prepare row with handling of potential blank values
        row = [
            link.target_link or '',  # Empty string if None
            link.link_to or '',  # Empty string if None
            link.anchor_text or '',  # Empty string if None
            link.get_status_of_link_display() or '',  # Empty string if None
            is_index,
            link.link_created.strftime('%Y-%m-%d') if link.link_created else '',
            link.last_crawl_date.strftime('%Y-%m-%d') if link.last_crawl_date else '',
        ]
        ws.append(row)

    # Set the HTTP response with a file attachment
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=links_status_report.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response

def delete_links(request, selected_links_ids):
    links_to_delete = Link.objects.filter(id__in=selected_links_ids)
    count = links_to_delete.count()
    links_to_delete.delete()

    messages.success(request, f'Deleted {count} links successfully.')
    return HttpResponseRedirect(reverse('home'))

def mark_links_as_addressed(request, selected_links_ids):
    updated_count = Link.objects.filter(id__in=selected_links_ids).update(address_status='addressed')

    # Provide feedback to the user
    messages.success(request, f'Marked {updated_count} links as addressed successfully.')

    # Redirect to home or another success page
    return HttpResponseRedirect(reverse('home'))


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


@login_required
def download_report(request):
    # Create a new Excel workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # Set the title for the worksheet
    ws.title = "Links Report"

    # Set the header row
    headers = ['Target Link', 'Link To', 'Anchor Text', 'Status Of Link', 'Index Status', 'Link Created', 'Last Crawl Date']
    ws.append(headers)

    # Retrieve the links based on the user's selection or all links
    # Here, you may add filtering based on request parameters
    links = Link.objects.all()

    for link in links:
        # Prepare the data row for each link
        data_row = [
            link.target_link,
            link.link_to,
            link.anchor_text,
            link.get_status_of_link_display(),  # This will fetch the human-readable value for the 'status_of_link' choice
            link.get_index_status_display(),    # Similarly, this fetches the readable value for 'index_status'
            link.link_created.strftime('%Y-%m-%d') if link.link_created else 'N/A',
            link.last_crawl_date.strftime('%Y-%m-%d') if link.last_crawl_date else 'N/A',
        ]
        ws.append(data_row)

    # Set the name of the Excel file
    filename = f"Links_Report_{now().strftime('%Y-%m-%d')}.xlsx"

    # Create a HTTP response with content type as Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # Set the content disposition to attachment to force download
    response['Content-Disposition'] = f'attachment; filename={filename}'

    # Save the Excel file to the response
    wb.save(response)

    return response

@require_http_methods(["GET", "POST"])
@login_required  # Require the user to be logged in to access this view
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

                # Check if a record with the same target_link, link_to, anchor_text, and user exists
                exists = Link.objects.filter(
                    target_link=row[2],
                    link_to=row[3],
                    anchor_text=row[1],
                    user=request.user  # Filter by the current user
                ).exists()

                if exists:
                    skipped_rows.append({
                        'row': index-1,
                        'anchor': row[1],
                        'target_link': row[2],
                        'link_to': row[3],
                    })
                else:
                    Link.objects.create(
                        user=request.user,  # Set the current user
                        anchor_text=row[1],
                        target_link=row[2],
                        link_to=row[3],
                        link_created=link_created
                    )

            if skipped_rows:
                request.session['skipped_rows'] = skipped_rows
                messages.warning(request, "Some rows were skipped due to duplicates.")
            else:
                messages.success(request, "Excel file processed successfully")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('add_links')

    skipped_rows = request.session.pop('skipped_rows', None)
    return render(request, "link_crawler/add_links.html", {'skipped_rows': skipped_rows})

@login_required
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
