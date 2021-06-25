#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None):
        """
        Creates and saves a User with the given data.
        """
        if not email:
            raise ValueError('Vous devez entrer un email valide')

        user = self.model(
            username=self.normalize_username(username),
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

class User(AbstractUser):
    """
        xxx
    """
    # Names
    username = models.CharField(max_length=30, unique=True, verbose_name='Pseudonyme')
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Prénom')
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Nom')
    # Contact
    email = models.EmailField(
        verbose_name='Adresse email',
        max_length=255,
        unique=True
        )
    # About
    avatar = models.ImageField()
    # Registration
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Dernière modification')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    
    # Main Field for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ('-created_at', '-updated_at', )
        
    def get_full_name(self):
        if self.first_name:
            return f'{self.first_name}  {self.last_name}'
        
        return self.email.split('@')[0]

# class Substitute(models.Model):
#     """
#         xxx
#     """

#     Users = models.ManyToManyField(User, related_name='substitutes')
    
#     def __str__(self):
#         return self.username
    
#     class Meta:
#         verbose_name_plural = "substitutes"