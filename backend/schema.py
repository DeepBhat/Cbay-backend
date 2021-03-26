import graphene
from graphene.types.scalars import String
from graphene.types.structures import List
from graphene_django import DjangoObjectType

from .models import Category, Image, Listing, User

# ========== MODELS ===============
class UserType(DjangoObjectType):
    class Meta:
        model = User

class ListingType(DjangoObjectType):
    class Meta:
        model = Listing

class ImageType(DjangoObjectType):
    class Meta:
        model = Image

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


## ========== QUERIES =================
# We specify the GraphQL Type for Graphene. But graphene_django
# can create types out of Django models so it handles that for us.

# Class to resolve queries made to GraphQL. Queries
# are just the READ operations for all models. 
class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    # We wish to be able to filter the listings based on
    # all of its parameters.
    listings = graphene.List(ListingType, 
    name=graphene.String(required=False, default_value=None),
    maxPrice=graphene.Decimal(required=False,default_value=None),
    minPrice=graphene.Decimal(required=False, default_value=None),
    negotiable=graphene.Boolean(required=False,default_value=None),
    condition=graphene.String(required=False,default_value=None),
    location=graphene.String(required=False,default_value=None),
    date_created=graphene.Date(required=False,default_value=None),
    userID=graphene.Int(required=False,default_value=None),
    university=graphene.String(required=False,default_value=None)
    )


    categories = graphene.List(CategoryType)
    images = graphene.List(ImageType)

    user = graphene.Field(UserType, id=graphene.Int(required=False, default_value=None), email=graphene.String(required=False, default_value=None))
    listing = graphene.Field(ListingType, id=graphene.Int())
    category = graphene.Field(CategoryType, id=graphene.Int())
    image = graphene.Field(ImageType, id=graphene.Int())


    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_listings(self, info, **kwargs):
        '''
        Return istings filtered based off the optional parameters passed.
        1. name (string): if the given name is contained in the item name
        2. maxPrice (Decimal): if the item price is less than or equal to parameter
        3. minPrice (Decimal): if the item price is greater than or equal to parameter
        4. negotiable (Boolean): if the item is negotiable
        5. condition (String): if the condition of the item matches the given condition
        6. location (String): if the location of the item matches the given location
        # TODO: add location filtering (within 1km, etc.)
        7. dateCreated (date): if the item is created on the same date as the given parameter
        8. #TODO: timeframe (time): if the item was created in the given timeframe
        9. userID (int): if the user through the user ID created the listing
        10. university (String): if the user's university matches the given university

        If none of the parameters are passed, all of the listings will be returned
        '''

        # initialize the query set
        listing_objects = Listing.objects

        # parse the parameters
        item_name = kwargs.get('name')
        max_price = kwargs.get('maxPrice')
        min_price = kwargs.get('minPrice')
        negotiable = kwargs.get('negotiable')
        condition = kwargs.get('negotiable')
        location = kwargs.get('location')
        date_created = kwargs.get('dateCreated')
        user_id = kwargs.get('userID')
        university = kwargs.get('university')

        # if no parameters are passed, return all the listings
        if not any([item_name, max_price, min_price, negotiable, condition, location, date_created, user_id, university]):
            return Listing.objects.all()

        # otherwise filter the query set
        if item_name is not None:
            listing_objects =  listing_objects.filter(item_name__contains=item_name)
        if max_price is not None:
            listing_objects = listing_objects.filter(price__lte=max_price)     
        if min_price is not None:
            listing_objects = listing_objects.filter(price__gte=min_price)
        if negotiable is not None:
            listing_objects = listing_objects.filter(negotiable=negotiable)
        if condition is not None:
            listing_objects = listing_objects.filter(condition=condition)
        if location is not None:
            listing_objects = listing_objects.filter(location=location)
        if date_created is not None:
            listing_objects = listing_objects.filter(date_created=date_created)
        if user_id is not None:
            listing_objects = listing_objects.filter(user__id=user_id)
        if university is not None:
            listing_objects = listing_objects.filter(user__university=university)

        return listing_objects

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()
    
    def resolve_images(self, info, **kwargs):
        return Image.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        email = kwargs.get('email')

        if id is not None:
            return User.objects.get(pk=id)
        elif email is not None:
            result = User.objects.filter(email__exact=email)
            if len(result) > 0:
                return result[0]
        
        return None

    def resolve_listing(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Listing.objects.get(id=id)
        
        return None

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        

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
    id = graphene.ID()
    item_name = graphene.String()
    price = graphene.Decimal()
    negotiable = graphene.Boolean()
    condition = graphene.String()
    description = graphene.String(default_value="")
    location = graphene.String()
    date_created = graphene.Date()
    user_id = graphene.ID()
    images = graphene.List(of_type=String)
    categories = graphene.List(of_type=String)


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
class CreateListing(graphene.Mutation):
    # Pass in the input class created above to specify
    # that all the fields of the class are required arguments
    class Arguments:
        input = ListingInput(required=True)
    
    # ok will be true if the mutation is successful
    ok = graphene.Boolean()
    # create a user field to accept UserType
    listing = graphene.Field(ListingType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True

        # find the user with the given user id
        user = User.objects.get(pk=input.user_id)

        # If User does not exist, return an error
        if not user:
            ok = False
            return CreateListing(ok=ok, listing=None)
        
        # Otherwise create the listing instance 
        listing_instance = Listing(
            item_name = input.item_name,
            price = input.price,
            negotiable = input.negotiable,
            condition = input.condition,
            description = input.condition,
            location = input.location,
            date_created = input.date_created,
            user = user
        )
        listing_instance.save()
        
        # Now create images and categories for the listing
        for image_url in input.images:
            image = Image(image_url=image_url, listing=listing_instance)
            image.save()

        for category_name in input.categories:
            category = Category(category_name=category_name, listing=listing_instance)
            category.save()

        # return the newly created instance
        return CreateListing(ok=ok, listing=listing_instance)

class UpdateListing(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ListingInput(required=True)

    ok = graphene.Boolean()
    listing = graphene.Field(ListingType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        listing_instance = Listing.objects.get(pk=id)
        if not listing_instance:
            return UpdateListing(ok=ok, listing=None)

        ok = True

        # Update the respective fields
        if input.item_name: listing_instance.item_name = input.item_name
        if input.price: listing_instance.price = input.price
        if input.negotiable: listing_instance.negotiable = input.negotiable
        if input.condition: listing_instance.condition = input.condition
        if input.description: listing_instance.description = input.description
        if input.location: listing_instance.location = input.location
        if input.date_created: listing_instance.date_created = input.date_created
        
        # Update the user if a new user ID is provided
        if input.user_id:
            new_user = User.objects.get(pk=input.user_id)
            if not new_user:
                ok = False
                return UpdateListing(ok=ok, listing=None)
            listing_instance.user = new_user

        # save the updated instance
        listing_instance.save()

        # Update the new images
        if input.images:
            for image_url in input.images:
                image = Image(image_url=image_url, listing=listing_instance)
                image.save()
        
        # Update the new categories
        if input.categories:
            for category_name in input.categories:
                category = Category(category_name=category_name, listing=listing_instance)
                category.save()

        return UpdateListing(ok=ok, listing=listing_instance)

class DeleteListing(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = True
        listing_instance = Listing.objects.get(pk=id)
        listing_instance.delete()
        return DeleteListing(ok=ok)



class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    # TODO: Uncomment the respective mount instance after creating the class.

    create_listing = CreateListing.Field()
    update_listing = UpdateListing.Field()
    # delete_listing = DeleteListing.Field()


# Creating the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
