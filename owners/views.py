
import json
#json은 js의 오브젝트 타입이기 때문에 이 라이브러리를 이용해서 json타입의 데이터를 딕셔너리로 바꿔서 사용한다.

from django.http import JsonResponse
#JsonResponse는 우리가 만든 데이터를 json으로 보낼 수 있다. 
#이때 json으로 데이터를 보내려면 데이터를 딕셔너리로 바꿔서 보내줘야 한다.

from django.views import View
#django에서 제공해주는 view기능을 사용하기 위해 추가

from owners.models import Owner, Dog
#app안의 models에서 정의한 class들을 가져온다.


class OwnerView(View):
    def post(self, request):
        data = json.loads(request.body)

        Owner.objects.create(
            name  = data['name'],
            email = data['email'],
            age   = data['age']
        )

        return JsonResponse({'message' : 'created'}, status=201)

    def get(self, request):
        owners = Owner.objects.all()
        result = []

        for owner in owners:
            dogs = owner.dog_set.all()
            dog_list = []

            for dog in dogs:
                dog_list.append(
                    {
                       "name" : dog.name,
                       "age" : dog.age, 
                    }
                )

         #결과를 바로 리턴하는게 아닌 밑의 dog_list로 간다 
           
            result.append(
                {
                "owner_id" : owner.id,
                "name"  : owner.name,
                "email" : owner.email,
                "age"   : owner.age,
                "dogs"  : dog_list
                }
            )

        return JsonResponse({"result" : result}, status=200)




class DogView(View):
    def post(self, request):
        data = json.loads(request.body)

        if Owner.objects.filter(id=data['owner_id']).exists():
            return JsonResponse({'message' : 'Not Found'}, status=404)

        Dog.objects.create(
            name  = data['name'],
            age   = data['age'],
            # owner = Owner.objects.get(name=data['owner'])
            owner_id = data['owner_id']
            )

        return JsonResponse({'message' : 'created'}, status=201)

    def get(self, request):
        dogs = Dog.objects.all()
        result = []

        for dog in dogs:
            result.append(
                {
                "name"  : dog.name,
                "age"   : dog.age,
                "owner" : dog.owner.name       
                }
            )

        return JsonResponse({"result" : result}, status=200)
