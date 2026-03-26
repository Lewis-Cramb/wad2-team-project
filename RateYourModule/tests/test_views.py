from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from RateYourModule.models import Module, Review, UserProfile
from datetime import date

def add_user(username, password="realpassword123", is_staff=False, email=None) -> User:
    if email is None:
        email = f"{username}@example.com"
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        is_staff=is_staff,
    )
    UserProfile.objects.get_or_create(user=user)
    return user


def add_module(moduleID, short_name, full_name) -> Module:
    module = Module.objects.get_or_create(
        moduleID=moduleID,
        defaults={
            "short_name": short_name,
            "full_name": full_name,
        },
    )[0]
    # Overwrite fields if they already existed
    module.short_name = short_name
    module.full_name = full_name
    module.save()
    return module


def add_review(user, module, rating=3.0, message="Test review", likes=0) -> Review:
    profile = UserProfile.objects.get(user=user)
    review = Review.objects.get_or_create(
        student=profile,
        module=module,
        defaults={
            "date": date.today(),
            "rating": rating,
            "message": message,
            "likes": likes,
        },
    )[0]
    # Overwrite fields if they already existed
    review.date = date.today()
    review.rating = rating
    review.message = message
    review.likes = likes
    review.save()
    return review


class IndexViewTests(TestCase):
    def test_index_view(self):
        add_module("COMPSCI2021", "WAD2", "Web Application Development 2")
        response = self.client.get(reverse("rateyourmodule:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")


class UserLoginViewTests(TestCase):
    def test_login_get(self):
        add_user("testuser")
        response = self.client.get(reverse("rateyourmodule:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_post_valid(self):
        add_user("testuser")
        response = self.client.post(
            reverse("rateyourmodule:login"),
            {"username": "testuser", "password": "realpassword123"},
        )
        self.assertRedirects(response, reverse("rateyourmodule:index"))


class UserLogoutViewTests(TestCase):
    def test_logout_requires_login(self):
        add_user("testuser")
        response = self.client.get(reverse("rateyourmodule:logout"))
        self.assertEqual(response.status_code, 302)

    def test_logout_logged_in(self):
        add_user("testuser")
        self.client.login(username="testuser", password="realpassword123")
        response = self.client.get(reverse("rateyourmodule:logout"))
        self.assertRedirects(response, reverse("rateyourmodule:index"))


class SignupViewTests(TestCase):
    def test_signup_get(self):
        response = self.client.get(reverse("rateyourmodule:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_signup_post_valid(self):
        response = self.client.post(
            reverse("rateyourmodule:signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "password12321?",
                "password2": "password12321?",
            },
        )
        self.assertRedirects(response, reverse("rateyourmodule:index"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(UserProfile.objects.filter(user__username="newuser").exists())


class ShowProfileViewTests(TestCase):
    def test_show_profile_view(self):
        user = add_user("testuser")
        module = add_module("COMPSCI2021", "WAD2", "Web Application Development 2")
        add_review(user, module, rating=4.0, message="Good module")

        response = self.client.get(
            reverse("rateyourmodule:show_profile", kwargs={"username": "testuser"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")


class EditProfileViewTests(TestCase):
    def test_edit_profile_requires_login(self):
        add_user("testuser")
        response = self.client.get(
            reverse("rateyourmodule:edit_profile", kwargs={"username": "testuser"})
        )
        self.assertEqual(response.status_code, 302)


class DeleteProfileViewTests(TestCase):
    def setUp(self):
        self.user = add_user("testuser1")
        self.other_user = add_user("testuser2")
        self.staff_user = add_user("admin", is_staff=True)

    def test_delete_own_profile(self):
        self.client.login(username="testuser1", password="realpassword123")
        response = self.client.get(
            reverse("rateyourmodule:delete_profile", kwargs={"username": "testuser1"})
        )
        self.assertRedirects(response, reverse("rateyourmodule:index"))
        self.assertFalse(User.objects.filter(username="testuser1").exists())

    def test_can_not_delete_other_profile(self):
        self.client.login(username="testuser1", password="realpassword123")
        response = self.client.get(
            reverse("rateyourmodule:delete_profile", kwargs={"username": "testuser2"})
        )
        self.assertRedirects(
            response,
            reverse("rateyourmodule:show_profile", kwargs={"username": "testuser2"}),
        )
        self.assertTrue(User.objects.filter(username="testuser2").exists())

    def test_staff_can_delete_profile(self):
        self.client.login(username="admin", password="realpassword123")
        response = self.client.get(
            reverse("rateyourmodule:delete_profile", kwargs={"username": "testuser2"})
        )
        self.assertRedirects(response, reverse("rateyourmodule:index"))
        self.assertFalse(User.objects.filter(username="testuser2").exists())


class ModuleListViewTests(TestCase):
    def test_module_list_view(self):
        add_module("COMPSCI2021", "WAD2", "Web Application Development 2")
        response = self.client.get(reverse("rateyourmodule:modules"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "modules.html")


class ShowModuleViewTests(TestCase):
    def setUp(self):
        self.user = add_user("testuser")
        self.module1 = add_module("COMPSCI2021", "WAD2", "Web Application Development 2")
        self.module2 = add_module("COMPSCI2003", "AF2", "Algorithmic Foundations 2")
        add_review(self.user, self.module1, rating=4.0, message="Good module")

    def test_show_module_view(self):
        response = self.client.get(
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module1.moduleID})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "module.html")

    def test_show_module_post_add_review(self):
        self.client.login(username="testuser", password="realpassword123")
        response = self.client.post(
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module2.moduleID}),
            {"action": "new_review", "rating": 5, "message": "Very good"},
        )
        self.assertRedirects(
            response,
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module2.moduleID}),
        )
        self.assertTrue(Review.objects.filter(module=self.module2).exists())


class AddModuleViewTests(TestCase):
    def setUp(self):
        self.user = add_user("testuser")
        self.staff_user = add_user("admin", is_staff=True)

    def test_add_module_staff_success(self):
        self.client.login(username="admin", password="realpassword123")
        response = self.client.post(
            reverse("rateyourmodule:add_module"),
            {
                "moduleID": "COMPSCI2021",
                "short_name": "WAD2",
                "full_name": "Web Application Development 2",
            },
        )
        self.assertRedirects(response, reverse("rateyourmodule:modules"))
        self.assertTrue(Module.objects.filter(moduleID="COMPSCI2021").exists())

    def test_can_not_add_module_non_staff(self):
        self.client.login(username="testuser", password="realpassword123")
        response = self.client.post(
            reverse("rateyourmodule:add_module"),
            {
                "moduleID": "COMPSCI2021",
                "short_name": "WAD2",
                "full_name": "Web Application Development 2",
            },
        )
        self.assertEqual(response.status_code, 302)


class DeleteModuleViewTests(TestCase):
    def setUp(self):
        self.user = add_user("testuser")
        self.staff_user = add_user("admin", is_staff=True)
        self.module = add_module("COMPSCI2021", "WAD2", "Web Application Development 2")

    def test_delete_module_staff_success(self):
        self.client.login(username="admin", password="realpassword123")
        response = self.client.get(
            reverse("rateyourmodule:delete_module", kwargs={"moduleID": self.module.moduleID})
        )
        self.assertRedirects(response, reverse("rateyourmodule:modules"))
        self.assertFalse(Module.objects.filter(moduleID=self.module.moduleID).exists())

    def test_can_not_delete_module_non_staff(self):
        self.client.login(username="testuser", password="realpassword123")
        response = self.client.get(
            reverse("rateyourmodule:delete_module", kwargs={"moduleID": self.module.moduleID})
        )
        self.assertEqual(response.status_code, 302)


class AddReviewViewTests(TestCase):
    def setUp(self):
        self.user = add_user("testuser")
        self.module1 = add_module("COMPSCI2021", "WAD2", "Web Application Development 2")
        self.module2 = add_module("COMPSCI2003", "AF2", "Algorithmic Foundations 2")
        add_review(self.user, self.module1, rating=3.0, message="Alright module")

    def test_add_review_success(self):
        self.client.login(username="testuser", password="realpassword123")
        response = self.client.post(
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module2.moduleID}),
            {"action": "new_review", "rating": 5, "message": "Such a good module!!"},
        )
        self.assertRedirects(
            response,
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module2.moduleID}),
        )
        self.assertTrue(Review.objects.filter(module=self.module2).exists())

    def test_can_not_add_review_duplicate(self):
        self.client.login(username="testuser", password="realpassword123")
        response = self.client.post(
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module1.moduleID}),
            {"action": "new_review", "rating": 1, "message": "Duplicate"},
        )
        self.assertRedirects(
            response,
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module1.moduleID}),
        )
        self.assertEqual(Review.objects.filter(module=self.module1).count(), 1)


class EditReviewViewTests(TestCase):
    def setUp(self):
        self.user = add_user("testuser1")
        self.other_user = add_user("testuser2")
        self.module = add_module("COMPSCI2021", "WAD2", "Web Application Development 2")
        self.review = add_review(self.user, self.module, rating=5.0, message="Amazing!")
        self.other_review = add_review(self.other_user, self.module, rating=2.0, message="Not great")

    def test_edit_review_success(self):
        self.client.login(username="testuser1", password="realpassword123")
        response = self.client.post(
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module.moduleID}),
            {
                "action": "edit_review",
                "reviewID": self.review.id,
                "rating": 1,
                "message": "Updated",
            },
        )
        self.assertRedirects(
            response,
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module.moduleID}),
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.message, "Updated")

    def test_can_not_edit_review_other_users_review(self):
        self.client.login(username="testuser1", password="realpassword123")
        response = self.client.post(
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module.moduleID}),
            {
                "action": "edit_review",
                "reviewID": self.other_review.id,
                "rating": 5,
                "message": "This shouldn't work",
            },
        )
        self.assertRedirects(
            response,
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module.moduleID}),
        )
        self.other_review.refresh_from_db()
        self.assertEqual(self.other_review.message, "Not great")


class DeleteReviewViewTests(TestCase):
    def setUp(self):
        self.user = add_user("testuser1")
        self.other_user = add_user("testuser2")
        self.module = add_module("COMPSCI2021", "WAD2", "Web Application Development 2")
        self.review = add_review(self.user, self.module, rating=4.0, message="Good module")
        self.other_review = add_review(self.other_user, self.module, rating=2.0, message="Not great")

    def test_delete_review_success(self):
        self.client.login(username="testuser1", password="realpassword123")
        response = self.client.post(
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module.moduleID}),
            {"action": "delete_review", "reviewID": self.review.id},
        )
        self.assertRedirects(
            response,
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module.moduleID}),
        )
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_can_not_delete_other_users_review(self):
        self.client.login(username="testuser1", password="realpassword123")
        response = self.client.post(
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module.moduleID}),
            {"action": "delete_review", "reviewID": self.other_review.id},
        )
        self.assertRedirects(
            response,
            reverse("rateyourmodule:show_module", kwargs={"moduleID": self.module.moduleID}),
        )
        self.assertTrue(Review.objects.filter(id=self.other_review.id).exists())


class LikeReviewViewTests(TestCase):
    def test_like_review_success(self):
        user = add_user("testuser")
        module = add_module("COMPSCI2021", "WAD2", "Web Application Development 2")
        review = add_review(user, module, rating=2.0, message="Alright module")

        self.client.login(username="testuser", password="realpassword123")
        response = self.client.get(
            reverse("rateyourmodule:like_category"),
            {"review_id": str(review.id)},
        )

        review.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(review.likes, 1)


class ModuleSuggestionViewTests(TestCase):
    def test_module_suggestion_view(self):
        add_module("COMPSCI2021", "WAD2", "Web Application Development 2")
        response = self.client.get(
            reverse("rateyourmodule:suggest"),
            {"suggestion": "WA"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "module_suggestions.html")