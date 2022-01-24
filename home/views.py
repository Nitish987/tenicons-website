from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .gcloud_upload import GoogleCloudMediaStorage
from .profile_manager import ProfileManager, profile_exists, create_default_profile, get_photo_path_username
from .item_manager import create_item, item_category, item_subcategory, ItemManager, item_category_sno, item_subcategory_sno, create_item_download_name
from .image_manager import ImageManager, resizeImage
from .search_query import makeQuery
from .models import Uploads
from math import ceil
from io import BytesIO
from tempfile import TemporaryFile

def index(request):
    auth_check = request.user.is_authenticated
    if auth_check == True:
        user = request.user
        username = user.username

        # checking whether the profile of the user exist or not and if exist than creating default user profile
        if not profile_exists(user, username):
            create_default_profile(
                user,
                username,
                user.email,
                True
            ).save()

        context = {
            'form_action_url': '/account/logoutacc',
            'button_title': 'Logout',
            'auth_status': True,
            'profile_pic_url': f'{ProfileManager(request.user, request.user.username).getProfilePicPath()}'
        }
        return render(request, 'home/index.html', context)
    else:
        context = {
            'form_action_url': '/account/',
            'button_title': 'Login',
            'auth_status': False,
        }
        return render(request, 'home/index.html', context)

def profile(request):
    auth_check = request.user.is_authenticated
    if auth_check:
        if request.method == 'POST':
            form_type = request.POST.get('form-type')
            print(form_type)
            if form_type == 'profile-pic-form': # if block for profile pic change
                # getting user profile
                user = request.user
                username = user.username
                user_profile = ProfileManager(user, username).getProfile()
                # checking whether the user have right to change profile pic
                if user_profile.right_to_change_profile_pic:
                    try:
                        # getting profile pic file in chunks( by default by django)
                        profile_pic = request.FILES['profile-img-file']

                        # writing chunks in file to desired google cloud location
                        profile_pic_name = user_profile.unique_id + '.png'
                        path = f'profile/pic/{profile_pic_name}'
                        storage = GoogleCloudMediaStorage()
                        new_path = storage.save(path, profile_pic)

                        # adding path to profile_pic_path field
                        user_profile.profile_pic_path = storage.url(new_path)
                        user_profile.save()

                        messages.add_message(request, messages.SUCCESS, 'Profile Pic Changed!')
                        context = {
                            'form_action_url': '/account/logoutacc',
                            'button_title': 'Logout',
                            'auth_status': True,
                            'profile_pic_url': f'{ProfileManager(user, username).getProfilePicPath()}'
                        }
                        return render(request, 'home/profile.html', context)
                    except:
                        messages.add_message(request, messages.WARNING, 'Please select the Pic!')
                        context = {
                            'form_action_url': '/account/logoutacc',
                            'button_title': 'Logout',
                            'auth_status': True,
                            'profile_pic_url': f'{ProfileManager(user, username).getProfilePicPath()}'
                        }
                        return render(request, 'home/profile.html', context)
                else:
                    messages.add_message(request, messages.ERROR, 'You are not allowed to change profile pic! For details Contact us')
                    context = {
                        'form_action_url': '/account/logoutacc',
                        'button_title': 'Logout',
                        'auth_status': True,
                        'profile_pic_url': f'{ProfileManager(user, username).getProfilePicPath()}'
                    }
                    return render(request, 'home/profile.html', context)

            elif form_type == 'password-change-form': # if block for password change
                old_password = request.POST.get('current_password')
                new_password = request.POST.get('new_password')
                re_password = request.POST.get('re_password')

                user = request.user
                if user.check_password(raw_password=old_password):
                    if new_password == re_password:
                        auth_user = User.objects.get(username=user.username, email=user.email)
                        auth_user.set_password(re_password)
                        auth_user.save()

                        messages.add_message(request, messages.SUCCESS,'Password Changed!')
                    else:
                        messages.add_message(request, messages.ERROR, 'New Password Incorrect!')
                else:
                    messages.add_message(request, messages.ERROR, 'Old Password Incorrect!')
                context = {
                    'form_action_url': '/account/logoutacc',
                    'button_title': 'Logout',
                    'auth_status': True,
                    'profile_pic_url': f'{ProfileManager(request.user, request.user.username).getProfilePicPath()}'
                }
                return render(request, 'home/profile.html', context)
            else:
                context = {
                    'form_action_url': '/account/logoutacc',
                    'button_title': 'Logout',
                    'auth_status': True,
                    'profile_pic_url': f'{ProfileManager(request.user, request.user.username).getProfilePicPath()}'
                }
                return render(request, 'home/profile.html', context)
        else:
            user = request.user
            username = user.username

            context = {
                'form_action_url': '/account/logoutacc',
                'button_title': 'Logout',
                'auth_status': True,
                'profile_pic_url': f'{ProfileManager(user, username).getProfilePicPath()}'
            }
            return render(request, 'home/profile.html', context)
    else:
        return redirect('loginacc')

def uploads(request):
    auth_check = request.user.is_authenticated
    if auth_check:
        if request.method == 'POST':
            user = request.user
            username = user.username

            # checking whether the use is eligible to upload posts
            if ProfileManager(user, username).haveRightToPost():
                category = request.POST.get('category')
                subcategory = request.POST.get('subcategory')
                searchTags = request.POST.get('search_tags')
                item = request.FILES['item']

                # writing file to the given path
                path = f'items/{item.name}'
                storage = GoogleCloudMediaStorage()
                new_path = storage.save(path, item)
                item_path = storage.url(new_path)

                # creating other size file and writing file
                for i in [2,3]:
                    path = f'items/{i}_{item.name}'
                    image = resizeImage(item.name, i)
                    img_byte_arr = BytesIO()
                    image.save(img_byte_arr, format=image.format)
                    storage.save(path, img_byte_arr)

                # creating item
                created_item = create_item(
                    uuid=ProfileManager(user, username).getUniqueID(),
                    itemName=item.name,
                    path=item_path,
                    category=item_category(int(category)),
                    subcategory=item_subcategory(int(subcategory)),
                    searchTags=searchTags,
                    liked_by=ProfileManager(user, username).getUniqueID()
                )
                created_item.save()

                # saving uploads to user Uploads Model
                user_uuid = ProfileManager(user,username).getUniqueID()
                if Uploads.objects.filter(uuid=user_uuid).exists():
                    uploaded_item = Uploads.objects.get(uuid=user_uuid)
                    uploaded_item_IDs = uploaded_item.uploaded + '|' + created_item.item_id
                    uploaded_item.uploaded = uploaded_item_IDs
                    uploaded_item.save()
                else:
                    uploaded_item = Uploads(uuid=user_uuid,uploaded=f'{created_item.item_id}')
                    uploaded_item.save()

                messages.add_message(request, messages.SUCCESS, 'Uploaded Successfully!')
            else:
                messages.add_message(request, messages.ERROR, 'You are not Allowed to Post or Upload anything!')

        # Fetching all Uploads by the user
        all_uploads = [[],[],[],[]]
        user_uuid = ProfileManager(request.user, request.user.username).getUniqueID()
        if Uploads.objects.filter(uuid=user_uuid).exists():
            user_upload = Uploads.objects.get(uuid=user_uuid)
            all_uploads_IDs = user_upload.uploaded.split('|')
            length = len(all_uploads_IDs)
            if length <= 4:
                for i in range(length):
                    all_uploads[i].append(ItemManager(all_uploads_IDs[i]).getItem())
            else:
                count, temp_length = 0, length
                for i in range(ceil(length/4)):
                    n = 4 if temp_length/4 >= 1 else temp_length
                    for j in range(n):
                        all_uploads[j].append(ItemManager(all_uploads_IDs[j + count]).getItem())
                    count += 4
                    temp_length -= 4

        context = {
            'form_action_url': '/account/logoutacc',
            'button_title': 'Logout',
            'auth_status': True,
            'profile_pic_url': f'{ProfileManager(request.user, request.user.username).getProfilePicPath()}',
        }
        # adding uploads in context if there are uploads greater than 1
        if len(all_uploads[0]) > 0:
            context['uploads'] = all_uploads

        return render(request, 'home/uploads.html', context)
    else:
        return redirect('loginacc')

# API
def edituploads(request):
    try:
        if request.user.is_authenticated:
            item_id = request.POST.get('item_id')
            item = ItemManager(item_id=item_id).getItem()
            if item.uuid == f'{ProfileManager(user=request.user, username=request.user.username).getUniqueID()}':
                category = request.POST.get('category')
                subcategory = request.POST.get('subcategory')
                searchTags = request.POST.get('tags')
                searchable = request.POST.get('searchable')
                if searchable == 'true':
                    searchable = True
                else:
                    searchable = False

                # saving edited item
                item.category = item_category(int(category))
                item.subcategory = item_subcategory(int(subcategory))
                item.search_tags = searchTags
                item.searchable = searchable
                item.save()

                return HttpResponse('done')
            else:
                return HttpResponse('invalid request')
        else:
            return HttpResponse('invalid request')
    except:
        return HttpResponse('invalid request')

# API
def showuploads(request):
    try:
        if request.user.is_authenticated:
            item_id = request.POST.get('item_id')
            item = ItemManager(item_id=item_id)
            if item.getUserID() == f'{ProfileManager(user=request.user, username=request.user.username).getUniqueID()}':
                json = {
                    'date': item.getDate(),
                    'likes': item.getLikes(),
                    'searchable': item.isSearchable(),
                    'downloads': item.getDownloadsCount(),
                    'category': item_category_sno(item.getItemCategory()),
                    'subcategory': item_subcategory_sno(item.getSubcategory()),
                    'resolution': ImageManager(name=item.getItemName()).getImageResolution(),
                    'tags': item.getSearchTags(),
                }
                return JsonResponse(json, safe=False)
            else:
                return HttpResponse('invalid request')
        else:
            return HttpResponse('invalid request')
    except:
        return HttpResponse('invalid request')

@csrf_exempt
def search(request):
    if request.method == 'GET':
        search_category = request.GET.get('search_item_category')
        search = request.GET.get('search_query')
        search_tags = search.split(' ')

        # Query and listing all search items in pages using paginator
        queried_item = [[], [], [], []]
        query_data = makeQuery(search_tags=search_tags, search_category=search_category)

        paginator = Paginator(query_data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        query = page_obj.object_list
        length = len(query)
        if length <= 4:
            for i in range(length):
                queried_item[i].append(query[i])
        else:
            count, temp_length = 0, length
            for i in range(ceil(length / 4)):
                n = 4 if temp_length / 4 >= 1 else temp_length
                for j in range(n):
                    queried_item[j].append(query[j + count])
                count += 4
                temp_length -= 4

        search_text = ''
        for i in search_tags:
            search_text = search_text + '+' + i

        if request.user.is_authenticated:
            context = {
                'form_action_url': '/account/logoutacc',
                'button_title': 'Logout',
                'auth_status': True,
                'profile_pic_url': f'{ProfileManager(request.user, request.user.username).getProfilePicPath()}',
                'search': search,
                'search_category': search_category,
            }
        else:
            context = {
                'form_action_url': '/account/',
                'button_title': 'Login',
                'auth_status': False,
                'search': search,
                'search_category': search_category,
            }

        if len(queried_item[0]) > 0:
            context['queried_items'] = queried_item
            context['page_obj'] = page_obj
            context['search_text'] = search_text[1:]

        return render(request, 'home/search.html', context)

# API
def showitemdetails(request):
    try:
        item_id = request.GET.get('item_id')
        item = ItemManager(item_id=item_id)
        user_data = get_photo_path_username(item.getUserID())
        json = {
            'date': item.getDate(),
            'likes': item.getLikes(),
            'downloads': item.getDownloadsCount(),
            'resolution': ImageManager(name=item.getItemName()).getImageResolution(),
            'user_profile_pic': user_data[0],
            'username': user_data[1],
            'auth_state': request.user.is_authenticated,
        }
        if request.user.is_authenticated:
            uuid = ProfileManager(user=request.user, username=request.user.username).getUniqueID()
            json['like_state'] = True if uuid in item.getLikeBy() else False
            json['same_user'] = True if item.getUserID() in ProfileManager(user=request.user, username=request.user.username).getUniqueID() else False
        return JsonResponse(json, safe=False)
    except:
        return HttpResponse('invalid request')

# API
@csrf_protect
def createlike(request):
    try:
        if request.user.is_authenticated and request.method == 'POST':
            item_id = request.POST.get('item_id')

            profile = ProfileManager(user=request.user, username=request.user.username)
            item_manager = ItemManager(item_id=item_id)
            item = item_manager.getItem()
            like = item_manager.getLikes()

            if profile.getUniqueID() in item_manager.getLikeBy():
                item.likes = int(like) - 1
                liked_by = item_manager.getLikeBy()
                liked_by_change = ''
                for i, v in enumerate(liked_by):
                    if v != profile.getUniqueID() and v != '':
                        liked_by_change = liked_by_change + v
                item.liked_by = liked_by_change
                item.save()

                return HttpResponse(f'exist|{item.likes}')
            else:
                item.likes = int(like) + 1
                item.liked_by = item.liked_by + '|' + profile.getUniqueID()
                item.save()

                return HttpResponse(f'done|{item.likes}')

    except:
        return HttpResponse('invalid|0')

# APT
@csrf_protect
def download(request):
    try:
        if request.method == 'POST':
            item = ItemManager(item_id=request.POST.get('item_id'))
            res = request.POST.get('res')

            path = f'items/{item.getItemName()}'
            if res == 2:
                path = f'items/2_{item.getItemName()}'
            if res == 3:
                path = f'items/3_{item.getItemName()}'

            storage = GoogleCloudMediaStorage()
            file = storage.open(path)

            file_info = create_item_download_name(item.getItemName())
            http_response = HttpResponse(file.read(), content_type=f"image/f{file_info[1]}")
            http_response['Content-Disposition'] = 'attachment; filename=' + file_info[0]
            return http_response
        else:
            return HttpResponse('invalid')
    except:
        return HttpResponse('invalid')

def about(request):
    auth_check = request.user.is_authenticated
    if auth_check == True:
        context = {
            'form_action_url': '/account/logoutacc',
            'button_title': 'Logout',
            'auth_status': True,
            'profile_pic_url': f'{ProfileManager(request.user, request.user.username).getProfilePicPath()}'
        }
        return render(request, 'home/about.html', context)
    else:
        context = {
            'form_action_url': '/account/',
            'button_title': 'Login',
            'auth_status': False,
        }
        return render(request, 'home/about.html', context)

def contact(request):
    auth_check = request.user.is_authenticated
    if auth_check == True:
        context = {
            'form_action_url': '/account/logoutacc',
            'button_title': 'Logout',
            'auth_status': True,
            'profile_pic_url': f'{ProfileManager(request.user, request.user.username).getProfilePicPath()}'
        }
        return render(request, 'home/contact.html', context)
    else:
        context = {
            'form_action_url': '/account/',
            'button_title': 'Login',
            'auth_status': False,
        }
        return render(request, 'home/contact.html', context)

