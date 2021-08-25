import logging

from aiohttp import web

from server.web.exceptions import Error


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except Error as e:
        return web.json_response(
            {"code": e.code, "description": e.description}, status=e.status
        )
    except web.HTTPException:
        raise
    except Exception as e:
        logging.exception(str(e))
        return web.json_response(
            {"code": "internal_error", "description": "Internal error"}, status=500
        )


@web.middleware
async def resp_middleware(request, handler):
    result = await handler(request)

    if not isinstance(result, web.StreamResponse):
        orig_handler = request.match_info.handler
        sub_handler = getattr(orig_handler, request.method.lower(), None)
        schema = None
        if hasattr(sub_handler, "__apispec__"):
            schema = sub_handler.__apispec__["responses"]["200"]["schema"]
        result = schema.dump(result)
        return web.json_response({"data": result})

    return result


@web.middleware
async def auth_mw(request: web.Request, handler):
    session_id = request.cookies.get("session_id")
    if session_id:
        session = await request.app["store"].session.get_by_id(session_id)
        if session:
            request["session"] = session

    return await handler(request)
