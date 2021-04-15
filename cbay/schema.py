import graphene
import backend.schema

class Query(backend.schema.Query, graphene.ObjectType):
    # This is a dummy class. Its only role is to inherit Query classes
    # of all the apps in the project. Currently, our only app is 
    # "backend" so it is only inheriting one Query class.
    pass

class Mutation(backend.schema.Mutation, graphene.ObjectType):
    # This is a dummy class. Its only role is to inherit Mutation classes
    # of all the apps in the project. Currently, our only app is 
    # "backend" so it is only inheriting one Mutation class.
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)