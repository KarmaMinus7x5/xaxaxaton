from aiogram import BaseMiddleware, types
import logging

logger = logging.getLogger("middleware")

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = chat_id = None

        try:
            if isinstance(event, types.Message):
                user_id = event.from_user.id if event.from_user else None
                chat_id = event.chat.id if event.chat else None
            elif isinstance(event, types.CallbackQuery):
                user_id = event.from_user.id if event.from_user else None
                chat_id = event.message.chat.id if event.message else None
            elif isinstance(event, types.Update):
                if event.message:
                    user_id = event.message.from_user.id
                    chat_id = event.message.chat.id
                elif event.callback_query:
                    user_id = event.callback_query.from_user.id
                    chat_id = event.callback_query.message.chat.id
                elif event.inline_query:
                    user_id = event.inline_query.from_user.id
                elif event.chat_member:
                    user_id = event.chat_member.from_user.id
                    chat_id = event.chat_member.chat.id
        except Exception:
            pass

        state = data.get("state")
        state_str = None
        if state:
            try:
                state_str = await state.get_state()
            except Exception:
                state_str = "<unavailable>"

        logger.info("Update: %s user=%s chat=%s state=%s", type(event).__name__, user_id, chat_id, state_str)
        return await handler(event, data)
