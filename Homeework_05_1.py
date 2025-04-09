import asyncio
import aiofiles
import shutil
from pathlib import Path
import argparse
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file: Path, output_folder: Path):
    try:
        ext = file.suffix[1:] if file.suffix else 'unknown'
        target_folder = output_folder / ext
        target_folder.mkdir(parents=True, exist_ok=True)
        target_path = target_folder / file.name

        async with aiofiles.open(file, 'rb') as src:
            content = await src.read()
            async with aiofiles.open(target_path, 'wb') as dest:
                await dest.write(content)

        logging.info(f'Copied: {file} -> {target_path}')
    except Exception as e:
        logging.error(f'Error copying {file}: {e}')

async def read_folder(source_folder: Path, output_folder: Path):
    try:
        tasks = []
        for item in source_folder.rglob('*'):
            if item.is_file():
                tasks.append(copy_file(item, output_folder))
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f'Error reading folder {source_folder}: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Async file sorter based on extensions')
    parser.add_argument('--source', type=str, required=True, help='Path to the source folder')
    parser.add_argument('--output', type=str, required=True, help='Path to the output folder')

    args = parser.parse_args()
    source_folder = Path(args.source)
    output_folder = Path(args.output)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error('Invalid source folder path')
    else:
        asyncio.run(read_folder(source_folder, output_folder))


'запуск скрипту'
# python3 Homework_05_1.py --source ./source_folder --output ./output_folder