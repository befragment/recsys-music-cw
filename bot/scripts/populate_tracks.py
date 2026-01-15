"""
Скрипт для парсинга MP3 файлов из data/fma_small и заполнения таблицы tracks
"""
import asyncio
import os
from pathlib import Path
from typing import Optional

from loguru import logger
from mutagen import File as MutagenFile
from mutagen.mp3 import MP3
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import async_session_factory, engine, Base
from repository._orm import TrackORM


def get_mp3_metadata(file_path: Path) -> Optional[dict]:
    """
    Извлекает метаданные из MP3 файла
    
    Args:
        file_path: Путь к MP3 файлу
        
    Returns:
        Словарь с метаданными или None если не удалось извлечь
    """
    try:
        audio = MP3(file_path)
        
        # Извлекаем метаданные
        title = None
        artist = None
        album = None
        
        # Пробуем получить теги из различных форматов (ID3v2, ID3v1, etc.)
        if audio.tags:
            # ID3 теги
            title = str(audio.tags.get('TIT2', [''])[0]) if audio.tags.get('TIT2') else None
            artist = str(audio.tags.get('TPE1', [''])[0]) if audio.tags.get('TPE1') else None
            album = str(audio.tags.get('TALB', [''])[0]) if audio.tags.get('TALB') else None
        
        # Если теги не найдены, используем имя файла
        if not title:
            title = file_path.stem  # Имя файла без расширения
        
        if not artist:
            artist = "Unknown Artist"
            
        # Длительность в миллисекундах
        duration_ms = int(audio.info.length * 1000) if audio.info else None
        
        return {
            'title': title,
            'artist': artist,
            'album': album,
            'duration_ms': duration_ms,
            'local_path': str(file_path),
        }
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return None


def find_all_mp3_files(data_dir: Path) -> list[Path]:
    """
    Находит все MP3 файлы в директории
    
    Args:
        data_dir: Путь к директории с данными
        
    Returns:
        Список путей к MP3 файлам
    """
    mp3_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.mp3'):
                mp3_files.append(Path(root) / file)
    return mp3_files


async def populate_tracks_table(data_dir: Path, batch_size: int = 100, skip_if_exists: bool = False):
    """
    Заполняет таблицу tracks данными из MP3 файлов
    
    Args:
        data_dir: Путь к директории с MP3 файлами
        batch_size: Количество записей для вставки за раз
        skip_if_exists: Если True, пропускает заполнение если данные уже есть
    """
    logger.info(f"Поиск MP3 файлов в {data_dir}...")
    mp3_files = find_all_mp3_files(data_dir)
    logger.info(f"Найдено {len(mp3_files)} MP3 файлов")
    
    if not mp3_files:
        logger.warning("MP3 файлы не найдены!")
        return
    
    async with async_session_factory() as session:
        # Проверяем, есть ли уже данные в таблице
        result = await session.execute(select(TrackORM).limit(1))
        existing = result.scalar_one_or_none()
        
        if existing:
            if skip_if_exists:
                logger.info("Таблица tracks уже содержит данные. Пропускаем заполнение.")
                return
            else:
                logger.warning("Таблица tracks уже содержит данные. Очистить? (y/n)")
                response = input().strip().lower()
                if response == 'y':
                    logger.info("Очистка таблицы tracks...")
                    await session.execute(TrackORM.__table__.delete())
                    await session.commit()
                else:
                    logger.info("Отмена операции")
                    return
        
        tracks_to_insert = []
        success_count = 0
        error_count = 0
        
        for i, mp3_path in enumerate(mp3_files, 1):
            metadata = get_mp3_metadata(mp3_path)
            
            if metadata:
                track = TrackORM(
                    title=metadata['title'][:255],  # Обрезаем до размера поля
                    artist=metadata['artist'][:255],
                    album=metadata['album'][:255] if metadata['album'] else None,
                    duration_ms=metadata['duration_ms'],
                    local_path=metadata['local_path'],
                )
                tracks_to_insert.append(track)
                success_count += 1
            else:
                error_count += 1
            
            # Вставляем батчами
            if len(tracks_to_insert) >= batch_size:
                session.add_all(tracks_to_insert)
                await session.commit()
                logger.info(f"Обработано {i}/{len(mp3_files)} файлов (успешно: {success_count}, ошибок: {error_count})")
                tracks_to_insert = []
        
        # Вставляем оставшиеся записи
        if tracks_to_insert:
            session.add_all(tracks_to_insert)
            await session.commit()
        
        logger.success(f"Завершено! Успешно добавлено: {success_count}, ошибок: {error_count}")
        
        # Показываем статистику
        result = await session.execute(select(TrackORM))
        total_tracks = len(result.scalars().all())
        logger.info(f"Всего записей в таблице tracks: {total_tracks}")


async def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Заполнение таблицы tracks из MP3 файлов")
    parser.add_argument(
        "--skip-if-exists",
        action="store_true",
        help="Пропустить заполнение если данные уже есть (для автоматического запуска)"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Путь к директории с MP3 файлами"
    )
    
    args = parser.parse_args()
    
    # Определяем путь к директории с данными
    if args.data_dir:
        data_dir = Path(args.data_dir)
    else:
        script_dir = Path(__file__).parent.parent.parent
        data_dir = script_dir / "data" / "fma_small"
    
    if not data_dir.exists():
        logger.error(f"Директория {data_dir} не найдена!")
        return
    
    logger.info(f"Начало заполнения таблицы tracks из {data_dir}")
    await populate_tracks_table(data_dir, skip_if_exists=args.skip_if_exists)
    
    # Закрываем соединение с БД
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

