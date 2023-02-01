from fastapi import Request, HTTPException, APIRouter

from app.utils.db import db


router = APIRouter()

'''
@router.get('/settings')
async def settings(request: Request):
    if request.client.host == '(ip админа)':
        return templates.TemplateResponse('settings.html', context={"request": request}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')


@router.get('/settings/delete')
async def settings_delete_get(request: Request):
    if request.client.host == '(ip админа)':
        all_sources = await db.get_all_sources()
        return templates.TemplateResponse('delete.html', context={'request': request, 'sources': all_sources}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')


@router.post('/settings/delete')
async def settings_delete_post(request: Request, source: str = Form()):
    if request.client.host == '(ip админа)':
        all_sources = await db.get_all_sources()
        try:
            await db.delete_user(source)
            return templates.TemplateResponse('delete.html', context={'request': request, 'sources': all_sources, 'status': 'Удален'}, status_code=200)
        except Exception as ex:
            return templates.TemplateResponse('delete.html', context={'request': request, 'sources': all_sources, 'status': ex }, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')


@router.get('/settings/add')
async def settings_add_get(request: Request):
    if request.client.host == '(ip админа)':
        return templates.TemplateResponse('add.html', context={"request": request}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')

@router.post('/settings/add')
async def settings_add_post(request: Request, source: str = Form(), telegram: str = Form(None), email: str = Form(None), vk: str = Form(None), website: str = Form(None)):
    if request.client.host == '(ip админа)':
        try:
            await db.add_new_user(source=source, email=email, telegram=telegram, vk=vk, website=website)
            return templates.TemplateResponse('add.html', context={"request": request, "status": 'Добавлен'}, status_code=200)
        except Exception as ex:
            return templates.TemplateResponse('add.html', context={"request": request, "status": ex}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')

@router.get('/settings/edit')
async def settings_edit_pick_get(request: Request):
    if request.client.host == '(ip админа)':
        all_sources = await db.get_all_sources()
        return templates.TemplateResponse('edit.html', context={'request': request, 'sources': all_sources}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')

@router.post('/settings/edit')
async def settings_edit_get(request: Request, source: str = Form(), telegram: str = Form(None), email: str = Form(None), vk: str = Form(None), website: str = Form(None)):
    if request.client.host == '(ip админа)':
        all_sources = await db.get_all_sources()
        try:
            user = (await db.get_user(source=source))[1:]
            services = [email, telegram, vk, website]
            for i in range(3):
                if user[i] is not None:
                    services[i] = user[i]
            await db.edit_user(source=source, email=services[0], telegram=services[1], vk=services[2], website=services[3])
            return templates.TemplateResponse('edit.html', context={'request': request, 'sources': all_sources, 'status': 'Изменен'}, status_code=200)
        except Exception as ex:
            return templates.TemplateResponse('edit.html', context={'request': request, 'sources': all_sources, 'status': ex}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')
'''