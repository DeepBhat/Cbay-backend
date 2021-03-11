import graphene
from graphene_django import DjangoObjectType

from .models import Listing, User

## ========== QUERIES =================
# We specify the GraphQL Type for Graphene. But graphene_django
# can create types out of Django models so it handles that for us.
class UserType(DjangoObjectType):
    class Meta:
        model = User

class ListingType(DjangoObjectType):
    class Meta:
        model = Listing

# Class to resolve queries made to GraphQL. Queries
# are just the READ operations for all models. 
class Query(graphene.ObjectType):
    # TODO: add the other two models and queries for other two models
    users = graphene.List(UserType)
    listings = graphene.List(ListingType)
    user = graphene.Field(UserType, id=graphene.Int())
    listing = graphene.Field(ListingType, id=graphene.Int())

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_listings(self, info, **kwargs):
        return Listing.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return User.objects.get(pk=id)
        
        return None

    def resolve_listing(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Listing.objects.get(id=id)

        return None

## =============== MUTATIONS =====================
# Class to define what fields can be changed with the API.
# For our use case, these fields are the same as the model
# because everything in our models can be changed.
class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    email = graphene.String()
    first_name = graphene.String()   
    last_name = graphene.String()
    university = graphene.String()
    thumbs_up = graphene.Int(default_value=0)
    thumbs_down = graphene.Int(default_value=0)
    bio = graphene.String()
    classification = graphene.String()

class ListingInput(graphene.InputObjectType):
    # TODO: fill the fields for this model
    pass


# USER mutations
class CreateUser(graphene.Mutation):
    # Pass in the input class created above to specify
    # that all the fields of the class are required arguments
    class Arguments:
        input = UserInput(required=True)
    
    # ok will be true if the mutation is successful
    ok = graphene.Boolean()
    # create a user field to accept UserType
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user_instance = User(
            email = input.email,
            first_name = input.first_name,
            last_name = input.last_name,
            university = input.university,
            thumbs_up = input.thumbs_up,
            thumbs_down = input.thumbs_down,
            bio = input.bio,
            classification = input.classification
        )

        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)
    
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user_instance = User.objects.get(pk=id)
        if not user_instance:
            return UpdateUser(ok=ok, user=None)
        
        ok = True
        if input.email: user_instance.email = input.email
        if input.first_name: user_instance.first_name = input.first_name
        if input.last_name: user_instance.last_name = input.last_name
        if input.university: user_instance.university = input.university
        if input.thumbs_up: user_instance.thumbs_up = input.thumbs_up
        if input.thumbs_down: user_instance.thumbs_down = input.thumbs_down
        if input.bio: user_instance.bio = input.bio
        if input.classification: user_instance.classification = input.classification
        user_instance.save()
        return UpdateUser(ok=ok, user=user_instance)

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        ok = True
        user_instance = User.objects.get(pk=id)
        user_instance.delete()
        return DeleteUser(ok=ok)


# Listing mutations
# TODO: create listing mutations similar to user mutations
# class CreateListing(graphene.Mutation)
# class UpdateListing(graphene.Mutation)
# class DeleteListing(graphene.Mutation)



class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    # TODO: Uncomment the respective mount instance after creating the class.

    # create_listing = CreateListing.Field()
    # update_listing = UpdateListing.Field()
    # delete_listing = DeleteListing.Field()


# Creating the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
