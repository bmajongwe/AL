from ..models import Process

def save_process_step1(request, data):
    request.session['process_name'] = data.get('name')
    request.session['process_description'] = data.get('description')

def save_process_step2(request, filter_ids):
    request.session['selected_filters'] = filter_ids

def finalize_process_creation(request):
    # Retrieve the process details from the session
    process_name = request.session.get('process_name')
    process_description = request.session.get('process_description')
    selected_filters = request.session.get('selected_filters', [])

    # Create the Process instance
    process = Process.objects.create(
        name=process_name,
        description=process_description,
        created_by='System',  # Update to actual user if needed
        modified_by='System'
    )

    # Link the selected filters
    process.filters.set(selected_filters)

    # Clear session data for the process creation
    request.session.pop('process_name', None)
    request.session.pop('process_description', None)
    request.session.pop('selected_filters', None)

    return process
