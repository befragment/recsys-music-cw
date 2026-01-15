from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from loguru import logger

from core.container import Container
from handler._keyboards import create_player_keyboard
from domain.entity.interaction import InteractionAction

router = Router()

class PlayerStates(StatesGroup):
    playing = State()


@router.message(Command("music"))
async def cmd_music(message: Message, state: FSMContext, container: Container):
    """Запуск музыкального плеера"""
    track_service = container.track_service()
    tracks = await track_service.get_all_tracks()
    
    if not tracks:
        await message.answer(
            "❌ <b>Треки не найдены!</b>\n\n"
            "Убедитесь, что в папке data/fma_small/ есть mp3 файлы.",
            parse_mode=ParseMode.HTML
        )
        return

    
    await message.answer("🎧 <b>Запускаю музыкальный плеер...</b>", parse_mode=ParseMode.HTML)
    
    # Сохраняем данные в состоянии
    await state.update_data({
        'track_index': 0,
        'tracks': tracks
    })
    
    await state.set_state(PlayerStates.playing)
    await play_current_track(message, state)

async def play_current_track(message: Message, state: FSMContext):
    """Воспроизводит текущий трек"""
    data = await state.get_data()
    track_index = data.get('track_index', 0)
    tracks = data.get('tracks', [])
    
    if not tracks:
        await message.answer("❌ Нет треков для воспроизведения")
        await state.clear()
        return
    
    if track_index >= len(tracks):
        track_index = 0
    
    track = tracks[track_index]
    
    try:
        # Отправляем аудиофайл
        audio_file = FSInputFile(track.local_path)
        
        await message.answer_audio(
            audio=audio_file,
            title=track.title,
            performer=track.artist,
            reply_markup=create_player_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Ошибка при отправке трека: {e}")
        await message.answer(
            f"🎵 <b>Сейчас играет:</b> {track.title}\n\n"
            "Нажмите кнопки ниже для взаимодействия:",
            reply_markup=create_player_keyboard(),
            parse_mode=ParseMode.HTML
        )

@router.callback_query(F.data.startswith("player:"), PlayerStates.playing)
async def handle_player_action(callback: CallbackQuery, state: FSMContext, container: Container):
    """Обработка действий в плеере"""
    
    action = callback.data.split(":")[1]  # like, dislike, skip
    data = await state.get_data()
    
    # Сохраняем взаимодействие если это like или dislike
    if action in ['like', 'dislike']:
        user_service = container.user_service()
        interaction_service = container.interaction_service()
        
        try:
            # Проверяем, существует ли пользователь
            user = await user_service.get_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("❌ Сначала пройдите регистрацию через /start")
                return
            
            current_track_index = data.get('track_index', 0)
            tracks = data.get('tracks', [])
            
            if tracks and current_track_index < len(tracks):
                track = tracks[current_track_index]
                
                # Сохраняем взаимодействие
                interaction_action = InteractionAction.like if action == 'like' else InteractionAction.dislike
                await interaction_service.handle_user_interaction(
                    telegram_id=callback.from_user.id,
                    track_id=track.id,
                    interaction_type=interaction_action
                )
                
                if action == 'like':
                    await callback.answer("❤️ Лайк сохранен!")
                else:
                    await callback.answer("💔 Дизлайк сохранен!")
                    
        except Exception as e:
            logger.error(f"Ошибка сохранения взаимодействия: {e}")
            await callback.answer("⚠️ Не удалось сохранить")
    else:
        await callback.answer()
    
    # Переключаем трек
    if action in ['skip', 'like', 'dislike']:
        current_index = data.get('track_index', 0)
        tracks = data.get('tracks', [])
        
        if not tracks:
            await callback.answer("❌ Нет треков")
            return
        
        next_index = (current_index + 1) % len(tracks)
        
        await state.update_data(track_index=next_index)
        await callback.message.delete()

        # Воспроизводим следующий трек
        await play_current_track(callback.message, state)


@router.message(Command("liked"))
async def cmd_liked(message: Message, container: Container):
    """Показывает понравившиеся треки"""
    user_service = container.user_service()
    
    try:
        # Пробуем через user_service
        user_service = container.user_service()
        
        try:
            user = await user_service.get_by_telegram_id(message.from_user.id)
            if user:
                liked_tracks = await user_service.get_liked_tracks(user.id)
                
                if liked_tracks:
                    response = "❤️ <b>Вам понравились:</b>\n\n"
                    for i, track in enumerate(liked_tracks[:10], 1):
                        response += f"{i}. {track.title}\n"
                    await message.answer(response, parse_mode=ParseMode.HTML)
                else:
                    await message.answer("📭 У вас пока нет понравившихся треков")
            else:
                await message.answer("❌ Сначала заполните анкету через /start")
                
        except AttributeError:
            await message.answer("⚠️ Функция временно недоступна")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer("❌ Ошибка при получении списка")


@router.message(Command("disliked"))
async def cmd_disliked(message: Message, container: Container):
    """Показывает непонравившиеся треки"""
    # Аналогично /liked
    await message.answer("⚠️ Функция временно недоступна")