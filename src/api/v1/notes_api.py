from http import HTTPStatus
from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.authentication import auth_dep
from schemas.note_schema import NoteCreate, NoteUpdate, NoteInDB, TagInDB
from services.note_service import NoteService, get_note_service

router = APIRouter()


@router.get('/',
            description='Получить список всех заметок',
            status_code=status.HTTP_200_OK)
async def get_notes(authorize: AuthJWT = Depends(auth_dep),
                    note_service: NoteService = Depends(get_note_service)):

    await authorize.jwt_required()
    note = await note_service.get_notes()

    return note


@router.get('/{note_id}',
            description='Получение информации об одной заметке',
            status_code=status.HTTP_200_OK)
async def get_note_by_id(note_id: UUID,
                         authorize: AuthJWT = Depends(auth_dep),
                         note_service: NoteService = Depends(get_note_service)):

    await authorize.jwt_required()
    note = await note_service.get_note(note_id)
    if not note:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Note not found')
    return note


@router.post('/',
             description='Создать заметку',
             response_model=NoteInDB,
             status_code=status.HTTP_201_CREATED)
async def create_note(note_create: NoteCreate,
                      authorize: AuthJWT = Depends(auth_dep),
                      note_service: NoteService = Depends(get_note_service)):

    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    note = await note_service.create_note(note_create, user_id)

    return note


@router.put('/{note_id}',
            description='Изменить заметку',
            response_model=NoteInDB,
            status_code=status.HTTP_200_OK)
async def update_note(note_id: UUID, note_update: NoteUpdate,
                      authorize: AuthJWT = Depends(auth_dep),
                      note_service: NoteService = Depends(get_note_service)):

    await authorize.jwt_required()
    note = await note_service.update_note(note_id, note_update)
    if not note:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Note not found')

    return note


@router.delete('/{note_id}',
               description='Удалить заметку',
               status_code=status.HTTP_200_OK)
async def delete_note(note_id: UUID,
                      authorize: AuthJWT = Depends(auth_dep),
                      note_service: NoteService = Depends(get_note_service)):

    # await authorize.jwt_required()
    note = await note_service.delete_note(note_id)
    if not note:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Note not found')

    return note
