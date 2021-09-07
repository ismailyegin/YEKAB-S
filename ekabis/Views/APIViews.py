import uuid

from django.contrib.auth import logout
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from ekabis.models import Company, Employee, Yeka, Logs, YekaCompetition, ConnectionRegion
from ekabis.models.LogAPIObject import LogAPIObject
from ekabis.serializers.CompanySerializers import CompanyResponseSerializer
from ekabis.serializers.CompetitionSerializers import YekaCompetitionSerializer
from ekabis.serializers.EmployeeSerializers import EmployeeResponseSerializer
from ekabis.serializers.LogSerializers import LogResponseSerializer
from ekabis.serializers.YekaSerializer import YekaResponseSerializer
from ekabis.services import general_methods
from ekabis.services.services import EmployeeService, YekaService, LogsService, YekaCompetitionService


class GetCompany(APIView):

    def post(self, request, format=None):
        perm = general_methods.control_access(request)
        if not perm:
            logout(request)
            return redirect('accounts:login')
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        companiess = Company.objects.filter(isDeleted=False).filter(is_consortium=False).count()

        companies = Company.objects.filter(isDeleted=False).filter(is_consortium=False).filter(
            name__icontains=request.data['search[value]']).order_by('-id')[
                    int(start):end]

        filteredTotal = Company.objects.filter(isDeleted=False).filter(is_consortium=False).filter(
            name__icontains=request.data['search[value]']).count()

        logApiObject = LogAPIObject()
        logApiObject.data = companies
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(companiess)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,

        }
        serializer = CompanyResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetEmployee(APIView):

    def post(self, request, format=None):
        perm = general_methods.control_access(request)
        if not perm:
            logout(request)
            return redirect('accounts:login')
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        employeefilter = {
            'isDeleted': False,
        }
        employees = EmployeeService(request, employeefilter).count()

        employeess = Employee.objects.filter(isDeleted=False).filter(
            person__user__first_name__icontains=request.data['search[value]']).order_by('-id')[
                     int(start):end]

        filteredTotal = Employee.objects.filter(isDeleted=False).filter(
            person__user__first_name__icontains=request.data['search[value]']).count()

        logApiObject = LogAPIObject()
        logApiObject.data = employeess
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(employees)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,

        }
        serializer = EmployeeResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetYeka(APIView):

    def post(self, request, format=None):
        perm = general_methods.control_access(request)
        if not perm:
            logout(request)
            return redirect('accounts:login')
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        filter = {
            'isDeleted': False,
        }
        count = YekaService(request, filter).count()

        all_objects = Yeka.objects.filter(isDeleted=False).filter(yekaParent=None).filter(
            definition__icontains=request.data['search[value]']).order_by('-id')[
                      int(start):end]

        filteredTotal = Yeka.objects.filter(isDeleted=False).filter(yekaParent=None).filter(
            definition__icontains=request.data['search[value]']).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = YekaResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetSubYeka(APIView):

    def post(self, request, format=None):
        perm = general_methods.control_access(request)
        if not perm:
            logout(request)
            return redirect('accounts:login')
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        filter = {
            'isDeleted': False,
            'yekaParent': None

        }
        count = YekaService(request, filter).count()

        all_objects = Yeka.objects.filter(isDeleted=False).filter(yekaParent=None).filter(
            definition__icontains=request.data['search[value]']).order_by('-id')[
                      int(start):end]

        filteredTotal = Yeka.objects.filter(isDeleted=False).filter(yekaParent=None).filter(
            definition__icontains=request.data['search[value]']).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,

        }
        serializer = YekaResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetLog(APIView):

    def post(self, request, format=None):
        perm = general_methods.control_access(request)
        if not perm:
            logout(request)
            return redirect('accounts:login')
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        count = LogsService(request, None).count()

        all_objects = Logs.objects.filter(isDeleted=False).filter(
            user__first_name__icontains=request.data['search[value]']).filter(
            user__last_name__icontains=request.data['search[value]']).order_by('-id')[
                      int(start):end]

        filteredTotal = Logs.objects.filter(isDeleted=False).filter(
            user__first_name__icontains=request.data['search[value]']).filter(
            user__last_name__icontains=request.data['search[value]']).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,

        }
        serializer = LogResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)



class GetYekaCompetition(APIView):

    def post(self, request, format=None):
        perm = general_methods.control_access(request)
        if not perm:
            logout(request)
            return redirect('accounts:login')
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)
        if request.data['uuid']:
            region = ConnectionRegion.objects.get(uuid=uuid.UUID(request.data['uuid']).hex)

            count = region.yekacompetition.filter(isDeleted=False).count()
            logApiObject = LogAPIObject()
            logApiObject.data = region.yekacompetition.filter(isDeleted=False)
            logApiObject.draw = int(request.POST['draw'])
            logApiObject.recordsTotal = int(count)
            logApiObject.recordsFiltered = 0
        else:
            filter = {
                'isDeleted': False,
                'parent': None
            }
            count = YekaCompetitionService(request, filter).count()

            all_objects = YekaCompetition.objects.filter(isDeleted=False).filter(parent=None).filter(
                name__icontains=request.data['search[value]']).order_by('-id')[
                          int(start):end]

            filteredTotal = YekaCompetition.objects.filter(isDeleted=False).filter(parent=None).filter(
                name__icontains=request.data['search[value]']).count()

            logApiObject = LogAPIObject()
            logApiObject.data = all_objects
            logApiObject.draw = int(request.POST['draw'])
            logApiObject.recordsTotal = int(count)
            logApiObject.recordsFiltered = int(filteredTotal)
        serializer_context = {
            'request': request,
        }
        serializer = YekaCompetitionSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)