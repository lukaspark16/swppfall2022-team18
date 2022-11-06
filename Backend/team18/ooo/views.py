'''
views of ooo
'''
import json
import ast

from json.decoder import JSONDecodeError
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseBadRequest
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Outfit, SampleCloth, UserCloth, Closet, LabelSet

def index():
    '''
    test
    '''
    return HttpResponse("Hello, world")

def signup(request):
    '''
    signup : django default user
    '''
    if request.method == 'POST':
        req_data = json.loads(request.body.decode())
        
        username = req_data['username']
        password = req_data['password']
        new_user = User.objects.create_user(username=username, password=password)
        Closet.objects.create(user=new_user)

        return HttpResponse(status=201)
    return HttpResponseNotAllowed(['POST'], status=405)

def signin(request):
    '''
    signin : django default user
    '''
    if request.method == 'POST':
        req_data = json.loads(request.body.decode())
        username = req_data['username']
        password = req_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=204)

        return HttpResponse(status=401)
    return HttpResponseNotAllowed(['POST'], status=405)

def signout(request):
    '''
    signout : django default user
    '''
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse(status=204)
        return HttpResponse('Unauthorized', status=401)
    return HttpResponseNotAllowed(['GET'], status=405)

def closet(request):
    '''
    closet : get or create user's closet items
    '''
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    
    user = User.objects.get(id=request.user.id)
    user_closet = Closet.objects.get(user=user)

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        closet_item_list = [closet_item for closet_item in UserCloth.objects.filter(closet=user_closet).values()]
        return JsonResponse(closet_item_list, safe=False)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        try:
            req_data = json.loads(request.body.decode())

            name = req_data['name']
            image_id = req_data['image_id']
            closet = user_closet
            type = req_data['type']
            color = req_data['color']
            pattern = req_data['pattern']

            label_set_obj, _ = LabelSet.objects.get_or_create(
                type=type, color=color, pattern=pattern
            )
            label_set = label_set_obj

        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()

        closet_item = UserCloth(
            name=name,
            image_id=image_id,
            closet=closet,
            type=type,
            color=color,
            pattern=pattern,
            label_set=label_set,
            # dates - created as default value []
        )
        closet_item.save()
        return HttpResponse(status=200)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'], status=405)

def closet_item(request, cloth_id):
    '''
    closet_item : get, edit or delete user's closet item / post date a user wore the cloth
    '''
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    try:
        target_item_obj = UserCloth.objects.get(id=cloth_id)
        dates_history = ast.literal_eval(target_item_obj.dates)
    except UserCloth.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        try:
            target_item_dict = UserCloth.objects.filter(id=cloth_id).values()[0]
        except UserCloth.DoesNotExist:
            return HttpResponseNotFound()

        return JsonResponse(target_item_dict)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        try:
            req_data = json.loads(request.body.decode())
            dates = req_data['dates']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()

        if dates not in dates_history:
            dates_history.append(dates)
            target_item_obj.dates = json.dumps(dates_history)

            target_item_obj.save()

        return HttpResponse(status=200)

    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        try:
            req_data = json.loads(request.body.decode())

            name = req_data['name']
            image_id = req_data['image_id']
            type = req_data['type']
            color = req_data['color']
            pattern = req_data['pattern']

            label_set_obj, _ = LabelSet.objects.get_or_create(
                type=type, color=color, pattern=pattern
            )
            label_set = label_set_obj
            old_date = req_data['old_date']
            new_date = req_data['new_date']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()

        target_item_obj.name = name
        target_item_obj.image_id = image_id
        target_item_obj.type = type
        target_item_obj.color = color
        target_item_obj.pattern = pattern
        target_item_obj.label_set = label_set

        if old_date in dates_history:
            old_date_idx = dates_history.index(old_date)
            dates_history[old_date_idx] = new_date
        else:
            dates_history.append(new_date)
        target_item_obj.dates = json.dumps(dates_history)

        target_item_obj.save()

        response_dict = {
            "id": target_item_obj.id,
            "name": target_item_obj.name,
            "image_id": target_item_obj.image_id,
            "type": target_item_obj.type,
            "color": target_item_obj.color,
            "pattern": target_item_obj.pattern,
            "dates": target_item_obj.dates,
        }
        return JsonResponse(response_dict, status=200)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        try:
            target_item_obj.delete()
            return HttpResponse(status=200)
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()

    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'], status=405)

@ensure_csrf_cookie
def token(request):
    '''
    get csrf token
    '''
    if request.method == 'GET':
        return HttpResponse(status=204)
    return HttpResponseNotAllowed(['GET'], status=405)

#outfit part start
def outfit_list(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        cursor = int(request.GET.get('cursor', '99999999999999').replace('/',''))
        page_size = int(request.GET.get('pageSize', '12').replace('/',''))

        #it should be change to use filter()
        #frontend must give filters in request body or params
        all_outfits = list(Outfit.objects.all().order_by("-popularity"))
        outfits_count = len(all_outfits)
        response_outfit_range = min(outfits_count, cursor + page_size + 1)

        outfit_list = all_outfits[cursor:response_outfit_range]

        is_last = False

        if len(outfit_list) != page_size + 1:
            is_last = True
        
        if not is_last:
            outfit_list.pop()
            newCursor = cursor + page_size
        else:
            newCursor = 0
        
        json_outfit_list = []
        for outfit in outfit_list:
            json_outfit = {
                "id" : outfit.id,
                "outfit_info": outfit.outfit_info,
                "popularity" : outfit.popularity,
                "image_id": outfit.image_id,
                "putchase_link": outfit.purchase_link
            }
            json_outfit_list.append(json_outfit)

        content = {
            'isLast': is_last,
            'cursor': newCursor,
            'outfits': json_outfit_list
        }
        return JsonResponse(content, status=200)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        cursor = int(request.GET.get('cursor', '99999999999999').replace('/',''))
        page_size = int(request.GET.get('pageSize', '12').replace('/',''))

        try:
            req_data = json.loads(request.body.decode())
            filter_type = req_data["type"]
            filter_color = req_data["color"]
            filter_pattern = req_data["pattern"]
            filter_userhave = req_data["userHave"]
            filter_recommend = req_data["recommend"]
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()
        
        using_labelset = False
        No_cloth_filter = True
        if filter_type or filter_color or filter_pattern:
            No_cloth_filter = False

        if filter_type and filter_color and filter_pattern:
            try:
                filter_labelset = LabelSet.objects.get(
                    Q(type=filter_type) & Q(color=filter_color) & Q(pattern=filter_pattern))
                using_labelset = True
            except LabelSet.DoesNotExist:
                using_labelset = False

        closet = Closet.objects.get(user=request.user)
        
        if filter_recommend == "True" or filter_userhave == "True":
            usercloth_list = list(UserCloth.objects.filter(closet=closet))

            labelset_list = []
            for usercloth in usercloth_list:
                labelset_list.append(usercloth.label_set)
            
            labelset_list = list(set(labelset_list))

            samplecloth_list = []
            for labelset in labelset_list:
                sampleclothes = list(SampleCloth.objects.filter(label_set=labelset))
                samplecloth_list = samplecloth_list + sampleclothes

            if using_labelset:
                filtered_samplecloth_list = [x for x in samplecloth_list if x.label_set == filter_labelset]
            else:
                filtered_samplecloth_list = samplecloth_list
                if filter_type:
                    filtered_samplecloth_list = [x for x in samplecloth_list if x.type == filter_type]
                if filter_color:
                    filtered_samplecloth_list = [x for x in samplecloth_list if x.color == filter_color]
                if filter_pattern:
                    filtered_samplecloth_list = [x for x in samplecloth_list if x.pattern == filter_pattern]

            all_outfits = []
            for samplecloth in filtered_samplecloth_list:
                all_outfits.append(samplecloth.outfit)

            all_outfits = list(set(all_outfits))
            all_outfits = sorted(all_outfits, key=lambda outfit: outfit.popularity, reverse=True)
            if filter_recommend == "True":
                recommend = []
                for outfit in all_outfits:
                    outfit_cloth_list = list(outfit.sample_cloth.all())

                    can_recommend = True
                    for cloth in outfit_cloth_list:
                        if not cloth in samplecloth_list:
                            can_recommend = False
                    if can_recommend:
                        recommend.append(outfit)   
                all_outfits = recommend
 
        else:
            if using_labelset:
                samplecloth_list = SampleCloth.objects.filter(label_set = filter_labelset)
            else:
                samplecloth_list = SampleCloth.objects.all()
                if filter_type:
                    samplecloth_list = [x for x in samplecloth_list if x.type == filter_type]
                if filter_color:
                    samplecloth_list = [x for x in samplecloth_list if x.color == filter_color]
                if filter_pattern:
                    samplecloth_list = [x for x in samplecloth_list if x.pattern == filter_pattern]
            all_outfits = []
            for samplecloth in samplecloth_list:
                all_outfits.append(samplecloth.outfit)

            all_outfits = list(set(all_outfits))
            all_outfits = sorted(all_outfits, key=lambda outfit: outfit.popularity, reverse=True)
        
        outfits_count = len(all_outfits)
        response_outfit_range = min(outfits_count, cursor + page_size + 1)

        outfit_list = all_outfits[cursor:response_outfit_range]

        is_last = False

        if len(outfit_list) != page_size + 1:
            is_last = True
        
        if not is_last:
            outfit_list.pop()
            newCursor = cursor + page_size
        else:
            newCursor = 0

        json_outfit_list = []
        for outfit in outfit_list:
            json_outfit = {
                "id" : outfit.id,
                "outfit_info": outfit.outfit_info,
                "popularity" : outfit.popularity,
                "image_id": outfit.image_id,
                "putchase_link": outfit.purchase_link
            }
            json_outfit_list.append(json_outfit)

        content = {
            'type': filter_type,
            'color': filter_color,
            'pattern': filter_pattern,
            'useLabelSet': using_labelset,
            'userHave': filter_userhave,
            'recommend': filter_recommend,
            'isLast': is_last,
            'cursor': newCursor,
            'outfits': json_outfit_list
        }

        return JsonResponse(content, status=200)


    return HttpResponseNotAllowed(['GET', 'POST'], status=405)

def outfit(request, outfit_id):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        try:
            outfit = Outfit.objects.get(id=outfit_id)
        except Outfit.DoesNotExist:
            return HttpResponseNotFound()

        sample_cloth_list = SampleCloth.objects.filter(outfit=outfit)

        json_outfit = {
            "id" : outfit.id,   
            "outfit_info": outfit.outfit_info,
            "popularity" : outfit.popularity,
            "image_id": outfit.image_id,
            "putchase_link": outfit.purchase_link
        }

        json_samplecloth_list = []
        for samplecloth in sample_cloth_list:
            json_samplecloth = {
                "id": samplecloth.id,
                "name": samplecloth.name,
                "image_id": samplecloth.image_id,
                "purchase_link": samplecloth.purchase_link,
                "outfit": samplecloth.outfit.id,
                "type": samplecloth.type,
                "color": samplecloth.color,
                "pattern": samplecloth.pattern
            }
            json_samplecloth_list.append(json_samplecloth)

        content = {
            'outfit': json_outfit,
            "sampleclothes": json_samplecloth_list
        }
        return JsonResponse(content, status=200)

    return HttpResponseNotAllowed(['GET'], status=405)


def sample_cloth(request, samplecloth_id):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        try:
            samplecloth = SampleCloth.objects.get(id=samplecloth_id)
        except SampleCloth.DoesNotExist:
            return HttpResponseNotFound()

        user_closet = Closet.objects.get(user=request.user)
        try:
            usercloth = UserCloth.objects.get(Q(closet=user_closet) & Q(label_set=samplecloth.label_set))
            json_usercloth = {
                "id": usercloth.id,
                "image_id": usercloth.image_id,
                "type": usercloth.type,
                "color": usercloth.color,
                "pattern": usercloth.pattern,
                "user" : usercloth.closet.user.id,
                "dates" : usercloth.dates
            }
        except UserCloth.DoesNotExist:
            json_usercloth = {}
        
        json_samplecloth = {
                "id": samplecloth.id,
                "name": samplecloth.name,
                "image_id": samplecloth.image_id,
                "purchase_link": samplecloth.purchase_link,
                "outfit": samplecloth.outfit.id,
                "type": samplecloth.type,
                "color": samplecloth.color,
                "pattern": samplecloth.pattern
            }
        
        content = {
            "usercloth": json_usercloth,
            "samplecloth": json_samplecloth
        }
        return JsonResponse(content, status=200)

    return HttpResponseNotAllowed(['GET'], status=405)

def today_outfit(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        closet = Closet.objects.get(user=request.user)
        usercloth_list = list(UserCloth.objects.filter(closet=closet))

        labelset_list = []
        for usercloth in usercloth_list:
            labelset_list.append(usercloth.label_set)
        
        labelset_list = list(set(labelset_list))

        samplecloth_list = []
        for labelset in labelset_list:
            sampleclothes = list(SampleCloth.objects.filter(label_set=labelset))
            samplecloth_list = samplecloth_list + sampleclothes

        outfit_list = []
        for samplecloth in samplecloth_list:
            outfit_list.append(samplecloth.outfit)

        outfit_list = list(set(outfit_list))
        outfit_list = sorted(outfit_list, key=lambda outfit: outfit.popularity, reverse=True)

        recommend = []
        for outfit in outfit_list:
            outfit_cloth_list = list(outfit.sample_cloth.all())

            can_recommend = True
            for cloth in outfit_cloth_list:
                if not cloth in samplecloth_list:
                    can_recommend = False
            if can_recommend:
                recommend.append(outfit)
                break
        
        json_outfit = {
            "id" : recommend[0].id,   
            "outfit_info": recommend[0].outfit_info,
            "popularity" : recommend[0].popularity,
            "image_id": recommend[0].image_id,
            "putchase_link": recommend[0].purchase_link
        }

        return JsonResponse(json_outfit, status=200)
            
    return HttpResponseNotAllowed(['GET'], status=405)

#outfit part end
