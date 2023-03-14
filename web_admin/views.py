from django.shortcuts import render

import requests
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
import json
import hashlib

url = "https://simsvendapi-production.up.railway.app/"


class RoleEditForm(forms.Form):
    user_id = forms.IntegerField(label="User_ID", required=True)
    role_id = forms.IntegerField(
        label="Role_ID 1=Normal, 2=Admin", required=True, )


class UserEditForm(forms.Form):
    user_id = forms.IntegerField(label="User_ID", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'User ID'}))
    elo = forms.IntegerField(label="Elo", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Elo'}))
    points = forms.IntegerField(label="Points", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Points'}))
    wins = forms.IntegerField(label="Wins", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Wins'}))
    losses = forms.IntegerField(label="Losses", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Losses'}))


class TourEditForm(forms.Form):
    id = forms.IntegerField(label="ID", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'ID'}))
    name = forms.CharField(label="Navn", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Navn'}))
    how_many = forms.IntegerField(label="How_many", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'How_many'}))
    place_id = forms.IntegerField(label="Place_ID", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Place ID'}))
    gender = forms.CharField(label="Køn", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Køn'}))
    elo = forms.IntegerField(label="Elo", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Elo'}))
    PricePool = forms.IntegerField(label="PricePool", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Price pool'}))
    Dec = forms.CharField(label="Description", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Beskrivelser'}))


class TourForm(forms.Form):
    name = forms.CharField(label="Navn", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Navn'}))
    how_many = forms.IntegerField(label="How_many", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'How_many'}))
    place_id = forms.IntegerField(label="Place_ID", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Place ID'}))
    gender = forms.CharField(label="Køn", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Køn'}))
    elo = forms.IntegerField(label="Elo", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Elo'}))
    PricePool = forms.IntegerField(label="PricePool", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Price pool'}))
    Dec = forms.CharField(label="Description", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Beskrivelser'}))


def index(request):

    if request.session.get('token'):

        print(request.session.get('token'))

        return render(request, "index.html", {

        })

    else:

        return HttpResponseRedirect(reverse("login"))


def edit_role(request):

    roleForm = RoleEditForm(request.POST)

    if roleForm.is_valid():

        token = request.session.get("token")

        headers = {"Authorization": "Bearer " + token}

        user_id = roleForm.cleaned_data["user_id"]
        role_id = roleForm.cleaned_data["role_id"]

        obj = {
            "ID": user_id,
            "RoleID": role_id
        }

        role_url = "https://simsvendapi-production.up.railway.app/admin/role"

        x = requests.post(role_url, json=obj, headers=headers)
        json_response = x.json()

        return HttpResponseRedirect(reverse("users"))


def edit_tour(request):

    tourEditForm = TourEditForm(request.POST)

    print(tourEditForm)

    url = "https://kronborgapi.com/admin/tour/update"

    if tourEditForm.is_valid():

        token = request.session.get("token")

        id = tourEditForm.cleaned_data["id"]
        name = tourEditForm.cleaned_data["name"]
        how_many = tourEditForm.cleaned_data["how_many"]
        place_id = tourEditForm.cleaned_data["place_id"]
        elo = tourEditForm.cleaned_data["elo"]
        gender = tourEditForm.cleaned_data["gender"]
        PricePool = tourEditForm.cleaned_data["PricePool"]
        Dec = tourEditForm.cleaned_data["Dec"]

        obj = {
            "ID": id,
            "name": name,
            "how_many": how_many,
            "place_id": place_id,
            "elo": elo,
            "gender": gender,
            "Tour": {
                "price_pool": PricePool,
                "dec": Dec,
                "tournament_id": id,
            },
        }

        headers = {"Authorization": "Bearer " + token}

        response = requests.post(url, json=obj, headers=headers)

        response.raise_for_status()
        return HttpResponseRedirect(reverse("tournements"))


def users(request):

    tourForm = TourForm(request.POST)
    if tourForm.is_valid():

        token = request.session.get("token")

        headers = {"Authorization": "Bearer " + token}

        name = form.cleaned_data["name"]
        how_many = form.cleaned_data["how_many"]
        place_id = form.cleaned_data["place_id"]
        gender = form.cleaned_data["gender"]
        PricePool = form.cleaned_data["PricePool"]
        Dec = form.cleaned_data["Dec"]

    users_url = "https://simsvendapi-production.up.railway.app/admin/stats/"

    stats_url = "https://simsvendapi-production.up.railway.app/admin/all/"

    if request.session.get('token'):

        token = request.session.get("token")

        headers = {"Authorization": "Bearer " + token}

        response = requests.get(stats_url, headers=headers)

        response.raise_for_status()

        json_response = response.json()

        if request.method == "POST":

            form = UserEditForm(request.POST)

            roleForm = RoleEditForm(request.POST)

            if form.is_valid():

                user_id = form.cleaned_data["user_id"]
                elo = form.cleaned_data["elo"]
                points = form.cleaned_data["points"]
                wins = form.cleaned_data["wins"]
                losses = form.cleaned_data["losses"]

                myobj = {
                    "elo": elo,
                    "points": points,
                    "Wins": wins,
                    "losses": losses,
                    "userId": user_id
                }

                x = requests.post(users_url, json=myobj, headers=headers)
                json_response = x.json()

                return HttpResponseRedirect(reverse("users"))

        return render(request, "users.html", {

            "form": UserEditForm,
            "role_form": RoleEditForm,
            "users": json_response

        })
    else:

        return HttpResponseRedirect(reverse("login"))


def matches(request):

    if request.session.get('token'):

        return render(request, "matches.html")

    else:

        return HttpResponseRedirect(reverse("login"))


def tournements(request):

    if request.session.get('token'):

        tournements_url = "https://simsvendapi-production.up.railway.app/admin/tour/all"

        token = request.session.get("token")

        headers = {"Authorization": "Bearer " + token}

        x = requests.get(tournements_url, headers=headers)

        json_response = x.json()

        if request.method == "POST":

            tour_url = "https://simsvendapi-production.up.railway.app/admin/tour/"

            form = TourForm(request.POST)

            if form.is_valid():

                name = form.cleaned_data["name"]
                how_many = form.cleaned_data["how_many"]
                place_id = form.cleaned_data["place_id"]
                elo = form.cleaned_data["elo"]
                gender = form.cleaned_data["gender"]
                PricePool = form.cleaned_data["PricePool"]
                Dec = form.cleaned_data["Dec"]

                myobj = {
                    "name": name,
                    "how_many": how_many,
                    "place_id": place_id,
                    "elo": elo,
                    "gender": gender,
                    "Tour": {
                        "PricePool": PricePool,
                        "Dec": Dec
                    },

                }

                x = requests.post(tour_url, json=myobj, headers=headers)

                json_response = x.json()

                return HttpResponseRedirect(reverse("tournements"))

        return render(request, "tournements.html", {


            "form": TourForm,
            "edit_form": TourEditForm,
            "tours": json_response

        })

    else:

        return HttpResponseRedirect(reverse("login"))


def login(request):

    if request.method == "POST":
        # Attempt to sign user in

        email = request.POST["email_test"]
        password = request.POST["password"]

        amail = "augustschnellpedersen@gmail.com"
        apass = "Test"

        bmail = "mkronborg7@gmail.com"
        bpass = "Test"

        myobj = {'email': email, "password": password}
        x = requests.post(url + "auth/adminlogin", json=myobj)
        # print(requests.status_code)
        # if not x.status_code:
            # return HttpResponseRedirect(reverse("login"))
        print("*****************")
        print(x.status_code)
        print("*****************")
        if not x.status_code == 200:
            return HttpResponseRedirect(reverse("login"))

        json_response = x.json()

        token = json_response["token"]

        session = requests.session()
        request.session['token'] = token

        return HttpResponseRedirect(reverse("index"))

    else:

        return render(request, "login.html")


def logout(request):

    request.session['token'] = ""

    return HttpResponseRedirect(reverse("login"))
