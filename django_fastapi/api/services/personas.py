from ..models import Persona

from ..utils.app_exceptions import AppException
from ..utils.service_result import ServiceResult

from asgiref.sync import sync_to_async

class PersonaService:

    async def create(self, request, user) -> ServiceResult:
        await Persona.objects.acreate(
            nombre = request.nombre,
            edad = request.edad
        )
        return ServiceResult({'Msg': 'Persona Creada Exitosamente'})

    async def get_by_name(self, name, user) -> ServiceResult:
        persona = await Persona.objects.filter(nombre = name).afirst()

        if (not persona):
            return ServiceResult(AppException.FooGetAll({'Msg': f'No existe la persona: {name}'}))

        return ServiceResult(persona.data())

    async def deleted(self, name, user) -> ServiceResult:
        persona = await Persona.objects.filter(nombre = name).afirst()

        if (not persona):
            return ServiceResult(AppException.FooGetAll({'Msg': f'No existe la persona: {name}'}))

        await sync_to_async(persona.delete)()

        return ServiceResult({'Msg': 'Persona eliminada'})

    async def update(self, name, item, user) -> ServiceResult:
        persona = await Persona.objects.filter(nombre = name).afirst()

        if (not persona):
            return ServiceResult(AppException.FooGetAll({'Msg': f'No existe la persona: {name}'}))

        persona.nombre = item.nombre
        persona.edad = item.edad

        await sync_to_async(persona.save)()

        return ServiceResult({'Msg': 'Persona actualizada'})