# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение
# должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе. Например,
# URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg — Программа должна использовать
# многопоточный, многопроцессорный и асинхронный подходы. — Программа должна иметь возможность задавать список
# URL-адресов через аргументы командной строки. — Программа должна выводить в консоль информацию о времени скачивания
# каждого изображения и общем времени выполнения программы.



# Для запуска можно использовать строку ниже (в конце строки установить значение аргумента --approach threaded / multiprocess / async)

# python homework_4.py https://dragon-island.ru/wa-data/public/shop/products/89/04/489/images/1114/1114.0x900.jpg https://hi-news.ru/wp-content/uploads/2022/10/biggest_python_5-750x475.jpg https://panteric.ru/files/583/31025747960_059035510.jpg https://icdn.lenta.ru/images/2017/02/07/15/20170207155911707/detail_34a4eb305d80473b2e52207fe9a12236.jpg https://panteric.ru/files/gallery/4269/big/dsc_2262-1_1600256142.jpg --approach async


import argparse
import os
import requests
import time
import concurrent.futures
import multiprocessing
import asyncio
import aiohttp


def download_image(url, output_dir):
    filename = url.split("/")[-1]
    filepath = os.path.join(output_dir, filename)
    response = requests.get(url)
    with open(filepath, "wb") as file:
        file.write(response.content)
    print(f"Downloaded {filename} to {filepath}")


async def download_image_async(session, url, output_dir):
    filename = url.split("/")[-1]
    filepath = os.path.join(output_dir, filename)
    async with session.get(url) as response:
        with open(filepath, "wb") as file:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                file.write(chunk)
    print(f"Downloaded {filename} to {filepath}")


def download_images_multithreaded(urls, output_dir):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda url: download_image(url, output_dir), urls)


def download_images_multiprocess(urls, output_dir):
    with multiprocessing.Pool() as pool:
        pool.starmap(download_image, [(url, output_dir) for url in urls])


async def download_images_async(urls, output_dir):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(download_image_async(session, url, output_dir))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Downloader")
    parser.add_argument("urls", nargs="+", help="List of image URLs")
    parser.add_argument("--approach", choices=["threaded", "multiprocess", "async"], default="threaded", help="Approach for downloading images")
    parser.add_argument("--output-dir", default=".", help="Output directory for downloaded files")
    args = parser.parse_args()

    start_time = time.time()

    if args.approach == "threaded":
        download_images_multithreaded(args.urls, args.output_dir)
    elif args.approach == "multiprocess":
        download_images_multiprocess(args.urls, args.output_dir)
    elif args.approach == "async":
        asyncio.run(download_images_async(args.urls, args.output_dir))

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time} seconds")
