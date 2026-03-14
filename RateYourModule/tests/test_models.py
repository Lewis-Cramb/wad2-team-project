from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from RateYourModule import models
from datetime import date

def create_test_user() -> models.UserProfile:
    user = User.objects.create_user(username="bob", password="test321") 
    profile = models.UserProfile.objects.create(user=user)
    return profile

def create_test_module() -> models.Module:
    module = models.Module.objects.create(
        moduleID="COMPSCI2021",
        short_name="WAD2",
        full_name="Web Application Development 2"
    )
    return module


class UserProfileModelTests(TestCase):
    def test_profile_image_can_be_blank(self):
        profile = create_test_user()

        self.assertEqual(profile.picture, "")
        self.assertTrue(models.UserProfile.objects.filter(pk=profile.pk).exists())


class ModuleModelTests(TestCase):
    def test_moduleID_is_unique(self):
        module1 = models.Module.objects.create(
            moduleID="COMPSCI2021",
            short_name="WAD2",
            full_name="Web Application Development 2"
        )

        with self.assertRaises(IntegrityError):
            models.Module.objects.create(
                moduleID="COMPSCI2021",
                short_name="DIFF",
                full_name="DIFFERENT"
            )
    

    def test_short_name_is_unique(self):
        module1 = models.Module.objects.create(
            moduleID="COMPSCI2021",
            short_name="WAD2",
            full_name="Web Application Development 2"
        )

        with self.assertRaises(IntegrityError):
            models.Module.objects.create(
                moduleID="COMPSCI0000",
                short_name="WAD2",
                full_name="DIFFERENT COURSE 2"
            )


class ReviewModelTests(TestCase):
    def test_ensure_likes_default(self):
        profile = create_test_user()
        module = create_test_module()
        
        review = models.Review.objects.create(
            date=date.today(),
            rating=4.4,
            student=profile,
            module=module
        )

        self.assertEqual(review.likes, 0)

    def test_ensure_likes_are_positive(self):
        profile = create_test_user()
        module = create_test_module()
        
        # Should throw an error
        with self.assertRaises(IntegrityError):
            models.Review.objects.create(
                date=date.today(),
                rating=4.4,
                likes=-1,
                student=profile,
                module=module
            )

    
    def test_ensure_rating_range_upper(self):
        profile = create_test_user()
        module = create_test_module()
        
        review = models.Review(
            date=date.today(),
            rating=5.1, # Above max 5
            likes=5,
            student=profile,
            module=module
        )

        # Should throw an error
        with self.assertRaises(ValidationError):
            # Checks validators (use before saving)
            review.full_clean() 

    
    def test_ensure_rating_range_lower(self):
        profile = create_test_user()
        module = create_test_module()
        
        review = models.Review(
            date=date.today(),
            rating=-0.1, # Below min 0
            likes=5,
            student=profile,
            module=module
        )

        # Should throw an error
        with self.assertRaises(ValidationError):
            # Checks validators (use before saving)
            review.full_clean() 

    
    def test_ensure_same_student_cant_review_same_module_twice(self):
        profile = create_test_user()
        module = create_test_module()
        
        review = models.Review.objects.create(
            date=date.today(),
            rating=4.9, 
            student=profile,
            module=module
        )

        # Should throw an error
        with self.assertRaises(IntegrityError):
            models.Review.objects.create(
                date=date.today(),
                rating=3, 
                student=profile,
                module=module
            )
    

    def test_deleting_student_deletes_review(self):
        profile = create_test_user()
        module = create_test_module()
        
        review = models.Review.objects.create(
            date=date.today(),
            rating=4.0, 
            student=profile,
            module=module
        )

        self.assertEqual(models.Review.objects.count(), 1)

        profile.delete()

        self.assertEqual(models.Review.objects.count(), 0)
        self.assertFalse(models.Review.objects.filter(pk=review.pk).exists())


    def test_deleting_module_deletes_review(self):
        profile = create_test_user()
        module = create_test_module()
        
        review = models.Review.objects.create(
            date=date.today(),
            rating=4.0, 
            student=profile,
            module=module
        )

        self.assertEqual(models.Review.objects.count(), 1)

        module.delete()

        self.assertEqual(models.Review.objects.count(), 0)
        self.assertFalse(models.Review.objects.filter(pk=review.pk).exists())