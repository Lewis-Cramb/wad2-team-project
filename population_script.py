import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team3D.settings')

import django
django.setup()

from django.contrib.auth.models import User
from RateYourModule.models import Module, UserProfile, Review
from datetime import date


def create_modules() -> dict[str, Module]:
    example_modules = [
        {
            "id": "COMPSCI2021",
            "short_name": "WAD2",
            "full_name": "Web Application Development 2"
        },
        {
            "id": "COMPSCI2008",
            "short_name": "OOSE2",
            "full_name": "Object-Oriented Software Engineering 2"
        },
        {
            "id": "COMPSCI2007",
            "short_name": "ADS2",
            "full_name": "Algorithms & Data Structures 2 "
        },
    ]

    modules = {}
    for m in example_modules:
        module = Module.objects.get_or_create(
            moduleID=m["id"],
            short_name=m["short_name"],
            full_name=m["full_name"]
        )

        modules[m["id"]] = module[0]

    print("Added modules:")
    for m in Module.objects.all():
        print(f'- {m}')
    
    return modules


def create_profiles() -> dict[str, UserProfile]:
    example_profiles = [
        {
            "username": "JanCasey123",
            "email": "jancasey@gmail.com",
            "password": "password123"
        },
        {
            "username": "Ted_Johnson",
            "email": "tJohnson@outlook.com",
            "password": "realpassword"
        },
        {
            "username": "jane-smith",
            "email": "janesmith@hotmail.com",
            "password": "12345"
        },
    ]

    profiles = {}
    for p in example_profiles:
        user, created = User.objects.get_or_create(
            username=p["username"], 
            defaults={"email": p["email"]}
        )

        if created:
            user.set_password(p["password"])
            user.save()

        profile = UserProfile.objects.get_or_create(user=user)[0]

        if p["username"] == "JanCasey123":
            profile.picture = "profile_images/JanCasey123.png"
            profile.save()

        profiles[p["username"]] = profile

    print("Added profiles:")
    for p in UserProfile.objects.all():
        print(f'- {p}')
    
    return profiles


def create_reviews(modules, profiles):
    example_reviews = [
        {
            "date": date(2026, 3, 14),
            "rating": 5.0,
            "likes": 100,
            "message": "WAD2 is a fantastic module, good content and amazing lecturers.",
            "student": "JanCasey123",
            "module": "COMPSCI2021"
        },
        {
            "date": date(2025, 4, 4),
            "rating": 4.0,
            "likes": 94,
            "message": "The content of this course was very engaging.",
            "student": "Ted_Johnson",
            "module": "COMPSCI2021"
        },
        {
            "date": date(2026, 3, 14),
            "rating": 3.0,
            "likes": 75,
            "message": "Pretty good course.",
            "student": "jane-smith",
            "module": "COMPSCI2021"
        },
        {
            "date": date(2025, 10, 24),
            "rating": 2.5,
            "likes": 51,
            "message": "OOSE2 is great, but the pace was too fast.",
            "student": "JanCasey123",
            "module": "COMPSCI2008"
        },
        {
            "date": date(2026, 1, 28),
            "rating": 3.5,
            "likes": 33,
            "message": "",
            "student": "jane-smith",
            "module": "COMPSCI2008"
        },
    ]

    for review in example_reviews:
        Review.objects.get_or_create ( 
            student=profiles[review["student"]],
            module=modules[review["module"]],
            defaults={
                "date": review["date"],
                "rating": review["rating"],
                "likes": review["likes"],
                "message": review["message"]
            }
        )
    
    print("Added reviews:")
    for r in Review.objects.all():
        print(f'- {r}')


def populate():
    modules = create_modules()    
    profiles = create_profiles()
    create_reviews(modules, profiles)


if __name__ == "__main__":
    print("Running RateYourModule population script...")
    print("[NOTE]: If ran twice it does not duplicate entries.")
    populate()