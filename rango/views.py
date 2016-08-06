from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
from django.shortcuts import redirect
from django.contrib.auth.models import User

def index(request):
    context = RequestContext(request)

    category_list = Category.objects.all()
    context_dict = {'categories': category_list}

    for category in category_list:


        page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    #### NEW CODE ####
    if request.session.get('last_visit'):
        # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).seconds > 0:
            request.session['visits'] = visits + 1
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
    #### END NEW CODE ####

    # Render and return the rendered response back to the user.
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    # Request the contex.
    context = RequestContext(request)

    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.
    if request.session['visits']:
        count = request.session['visits']
    else:
        count = 0
    return render_to_response('rango/about.html', {'visit_count': count}, context)
    # Return and render the response, ensuring the count is passed to the template engine.

def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    if request.method == 'POST':
                query = request.POST['query'].strip()
                if query:
                    result_list = run_query(query)
                    context_dict['result_list'] = result_list

    return render(request, 'rango/category.html', context_dict)



@login_required
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return HttpResponse('The specified page does not exist!')


    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    # made the change here
    context_dict = {'form':form, 'category': cat, 'category_name_slug': category_name_slug}

    return render(request, 'rango/add_page.html', context_dict)



@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

@login_required
def change_password(request):
    return render(request, 'rango/restricted.html', {})


def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})

def track_url(request):
    context = RequestContext(request)
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)

@login_required
def profile(request):
    context = RequestContext(request)
    cat_list = Category.objects.all()
    context_dict = {'cat_list': cat_list}
    u = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('rango/profile.html', context_dict, context)