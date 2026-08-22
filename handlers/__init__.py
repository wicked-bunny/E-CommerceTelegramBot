from aiogram import Dispatcher
from handlers.start import router as start_router
from handlers.сatalog import router as catalog_router
from handlers.profil import router as profil_router
from handlers.get_photoID import router as get_photoID_router
from handlers.info import router as info_router
from handlers.buy import router as buy_router
from handlers.orders import router as orders_router
from handlers.categories import router as  categories_router





def register_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(catalog_router)
    dp.include_router(profil_router)
    dp.include_router(get_photoID_router)
    dp.include_router(info_router)
    dp.include_router(buy_router)
    dp.include_router(orders_router)
    dp.include_router(categories_router)

