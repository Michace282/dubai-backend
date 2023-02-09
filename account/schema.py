import graphene
import graphql_jwt
import graphql_social_auth
from django import forms
from django.contrib.auth.models import User
from graphene import relay
from graphene_django.types import DjangoObjectType, ErrorType
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from backend.mixin import DjangoModelFormMutation
from .models import Subscribe, Contact, Guest, Profile, PayLink


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact
        interfaces = (relay.Node,)


class SubscribeType(DjangoObjectType):
    class Meta:
        model = Subscribe
        interfaces = (relay.Node,)


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email_or_phone', 'name', 'text']


class PayLinkType(DjangoObjectType):
    class Meta:
        model = PayLink
        interfaces = (graphene.relay.Node,)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        interfaces = (graphene.relay.Node,)


class GuestType(DjangoObjectType):
    class Meta:
        model = Guest
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    user = graphene.Field(UserType)
    guest_detail = graphene.Field(GuestType, uuid=graphene.String())
    pay_link_detail = graphene.Field(PayLinkType, id=graphene.ID())

    @login_required
    def resolve_user(self, info, **Nodekwargs):
        return info.context.user

    def resolve_guest_detail(self, info, uuid):
        return Guest.objects.filter(uuid=uuid).first()

    def resolve_pay_link_detail(self, info, id):
        return PayLink.objects.filter(id=from_global_id(id)[1]).first()


class GuestCreateMutation(graphene.Mutation):
    guest = graphene.Field(GuestType)

    @classmethod
    def mutate(cls, root, info):
        return GuestCreateMutation(guest=Guest.objects.create())


class SubscribeCreateMutation(DjangoModelFormMutation):
    class Meta:
        form_class = SubscribeForm


class ContactCreateMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ContactForm


class RefreshJSONWebToken(graphql_jwt.Refresh):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        if info.context.user.is_authenticated:
            return cls(user=info.context.user)
        return cls()


class RegistrationForm(forms.ModelForm):
    guest_uuid = forms.UUIDField(required=False)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    password_repeat = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name','last_name','password', 'password_repeat', 'guest_uuid')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")
        guest_uuid = cleaned_data.get("guest_uuid")

        if password != password_repeat:
            self.add_error('password_repeat', "Пароли не совпадают")

        if User.objects.filter(username=email).exists():
            self.add_error('email', "Такой аккаунт существует")

        if guest_uuid:
            if not Guest.objects.filter(uuid=guest_uuid).exists():
                self.add_error('guest_uuid', "Такого гостя не существует")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = dict([(k, v) for k, v in self.cleaned_data.items() if v != ""])
        instance.username = cleaned_data.get('email')
        instance.first_name = cleaned_data.get('first_name')
        instance.last_name = cleaned_data.get('last_name')
        instance.email = cleaned_data.get('email')

        if commit:
            instance.set_password(instance.password)
            instance.save()

            guest_uuid = cleaned_data.get('guest_uuid')

            if guest_uuid:
                guest = Guest.objects.filter(uuid=guest_uuid).first()
                if guest:
                    for productwishlist in guest.productwishlist_set.all():
                        productwishlist.user = instance
                        productwishlist.save()

                    for feedback in guest.feedback_set.all():
                        feedback.user = instance
                        feedback.save()

                    for basket in guest.basket_set.all():
                        basket.user = instance
                        basket.save()

                    guest.delete()

        return instance


class RegistrationMutation(DjangoModelFormMutation):
    user = graphene.Field(UserType)

    class Meta:
        form_class = RegistrationForm


from graphql_jwt.decorators import token_auth



class Test(graphql_jwt.ObtainJSONWebToken):
    user = graphene.Field(UserType)

    class Arguments:
        guest_uuid = graphene.UUID(required=False)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        user = None
        if info.context.user.is_authenticated:
            user = info.context.user

            guest_uuid = kwargs.get('guest_uuid')

            if guest_uuid:
                guest = Guest.objects.filter(uuid=guest_uuid).first()
                if guest:
                    for productwishlist in guest.productwishlist_set.all():
                        productwishlist.user = user
                        productwishlist.save()

                    for feedback in guest.feedback_set.all():
                        feedback.user = user
                        feedback.save()

                    for basket in guest.basket_set.all():
                        basket.user = user
                        basket.save()
        return cls(user=user)

    @classmethod
    @token_auth
    def mutate(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)


class UserUpdateForm(forms.ModelForm):
    country = forms.CharField(required=False)
    city = forms.CharField(required=False)
    address = forms.CharField(required=False)
    postal_code = forms.CharField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'country', 'city', 'address', 'postal_code', 'phone')

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = dict([(k, v) for k, v in self.cleaned_data.items() if v != ""])
        instance.username = cleaned_data.get('email')
        instance.email = cleaned_data.get('email')
        instance.profile.country = cleaned_data.get('country')
        instance.profile.city = cleaned_data.get('city')
        instance.profile.address = cleaned_data.get('address')
        instance.profile.postal_code = cleaned_data.get('postal_code')
        instance.profile.phone = cleaned_data.get('phone')

        if commit:
            instance.save()
        return instance


class UserUpdateMutation(DjangoModelFormMutation):
    user = graphene.Field(UserType)

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = {"data": input}

        if info.context.user.is_authenticated:
            instance = cls._meta.model._default_manager.get(pk=info.context.user.pk)
            kwargs["instance"] = instance
            kwargs["request"] = info.context

        return kwargs

    @classmethod
    def perform_mutate(cls, form, info):
        errors = []
        if info.context.user.is_authenticated:
            if form.cleaned_data.get('email') != info.context.user.email and User.objects.filter(
                    email=info.context.user.email).first():
                errors.append(ErrorType(field='user', messages=['Такой E-mail уже существует']))
            else:
                obj = form.save()
                kwargs = {cls._meta.return_field_name: obj}
        else:
            kwargs = {}
            errors.append(ErrorType(field='user', messages=['Вы не авторизованы']))
        return cls(errors=errors, **kwargs)

    class Meta:
        form_class = UserUpdateForm


class Mutation(graphene.ObjectType):
    guest_create = GuestCreateMutation.Field()
    token_auth = Test.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = RefreshJSONWebToken.Field()
    social_auth = graphql_social_auth.relay.SocialAuthJWT.Field()
    registration = RegistrationMutation.Field()
    user_update = UserUpdateMutation.Field()

    contact_create = ContactCreateMutation.Field()
    # subscribe_create = SubscribeCreateMutation.Field()
