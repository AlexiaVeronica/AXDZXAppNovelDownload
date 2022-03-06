import asyncio
import aiofiles


async def async_write(file_path: str, write_info: str):
    # 异步方式执行with操作,修改为 async with
    async with aiofiles.open(file_path, 'a', encoding="utf-8") as file_:
        await file_.write(write_info)


async def async_read(file_path: str):
    async with aiofiles.open(file_path, 'r', encoding="utf-8") as file_:
        return await file_.read()


async def async_read_lines(file_path: str):
    async with aiofiles.open(file_path, 'r', encoding="utf-8") as file_:
        async for line in file_:
            return line


# async with aiofiles.open(self.path(self.config_book, book_name), 'r', encoding="utf-8") as file:
#     content = await file.read()
#     self.epub.add_chapter(
#         file_name.split('-')[1].replace('.txt', ''), content.replace('\n', '</p>\r\n<p>'),
#         file_name.split('-')[0]
#     )
#     file_txt_path = self.path(self.save_book, book_name, f'{book_name}.txt')
#     async with aiofiles.open(file_txt_path, "w", encoding="utf-8") as fp:
#         await fp.write(content)
# self.epub.save()
