import logging
from django.shortcuts import render
from .mongo_collection import person_collection
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from .serializers import PersonSerializer,UpdatePersonSerializer,GetPersonSerializer,DeletePersonSerializer
from rest_framework.views import APIView
from bson import ObjectId 

def index(request):
    return HttpResponse("<h1>App is running...</h1>")

class AddPersonAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            # Extracting validated data and filtering out None values
            validated_data = {key: value for key, value in serializer.validated_data.items() if value is not None}
            print(validated_data)
            # If there is any validated data, insert into MongoDB
            if validated_data:
                person_collection.insert_one(validated_data)
                return Response({"message": "Person added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "No valid data provided"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdatePersonAPIView(APIView):
    
    def put(self, request, person_id, *args, **kwargs):
        try:
            person_object_id = ObjectId(person_id)

           
            if person_collection.find_one({"_id": person_object_id}):
                serializer = UpdatePersonSerializer(data=request.data)
                if serializer.is_valid():
                    updated_fields = {key: value for key, value in serializer.validated_data.items() if key != "_id" and value is not None}
                    if updated_fields:
                        person_collection.update_one({"_id": person_object_id}, {"$set": updated_fields})
                        return Response({"message": "Person updated successfully"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "No fields to update"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Person not found"}, status=status.HTTP_404_NOT_FOUND) 

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    


class DeletePersonAPIView(APIView):
    def delete(self, request, person_id, *args, **kwargs):
        try:
            person_object_id = ObjectId(person_id)

            # Check if the person with the specified _id exists
            if person_collection.find_one({"_id": person_object_id}):
                serializer = DeletePersonSerializer(data={"_id": person_object_id})
                if serializer.is_valid():
                    result = person_collection.delete_one({"_id": person_object_id})
                    if result.deleted_count == 1:
                        return Response({"message": "Person deleted successfully"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "Person not found"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Person not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetPersonAPIView(APIView):
    def get(self, request, person_id, *args, **kwargs):
        try:
            person_object_id = ObjectId(person_id)
            person = person_collection.find_one({"_id": person_object_id})

            if person:
                serializer = GetPersonSerializer(person)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Person not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
           
    
# def add_person(request):
#     records ={
#         "first_name":"Tom",
#         "last_name":"Mathew",
#         "address":"265 MPB Road USA"
#     }

#     person_collection.insert_one(records)
#     return HttpResponse("<h1>Person added successfully...</h1>")

# def get_all_person(request):
#     persons = person_collection.find()
#     return HttpResponse(persons)