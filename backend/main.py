from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from database import get_async_session
from typing import List,Any
from sqlalchemy import func  
from fastapi.middleware.cors import CORSMiddleware
from model import Book
from contextlib import asynccontextmanager
from database import create_db
import asyncio

# app = FastAPI()

# Ensure tables exist before handling requests
# ✅ Use lifespan for startup event
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("🚀 Initializing Database...")
#     await create_db()  # Ensures tables exist before handling requests
#     print("✅ Database initialized successfully")
#     yield  # Application starts here

# version 2
# FastAPI app with lifespan and db_ready event
db_ready = asyncio.Event()  # Signals when DB is ready

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Initializing Database...")
    await create_db()  # Create tables
    await asyncio.sleep(2)  # Wait 2 seconds for Neon
    db_ready.set()  # Mark DB as ready
    print("✅ Database initialized successfully")
    yield  # Application runs here
    print("🛑 Shutting down...")

app = FastAPI(lifespan=lifespan)

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to ensure DB is ready
async def wait_for_db():
    await db_ready.wait()  # Block until DB is ready

# Add a new Book
@app.post("/add_book/")
async def create_book(title: str, author: str, genre: str, publication_year: int, session: AsyncSession = Depends(get_async_session)):
    book = Book(title=title, author=author, genre=genre, publication_year=publication_year)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return {"message": "Book created ✅", "book": book}

# Get All Books
@app.get("/get_books/")
async def get_books(session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        result = await session.execute(select(Book))
        books = result.scalars().all()
        return books


# Search Book by ID, Title, or Author
@app.get("/search_books/")
async def search_books(query: str = Query(...), session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        from sqlalchemy import or_
        
        
        conditions:List[Any] =  []
        
        # Try to convert to int for ID comparison
        try:
            id_query = int(query)
            conditions.append(Book.id == id_query)
        except ValueError:
            # If conversion fails, don't add ID condition
            pass
            
        # Add text search conditions
        conditions.append(func.lower(Book.title).like(func.lower(f"%{query}%")))
        conditions.append(func.lower(Book.author).like(func.lower(f"%{query}%")))
        
        # Combine all conditions with or_()
        search_condition = or_(*conditions)
        
        result = await session.execute(select(Book).where(search_condition))
        books = result.scalars().all()
        if not books:
            raise HTTPException(status_code=404, detail="No matching books found 🚫")
        return books



# Update Read Status by ID, Title, or Author

@app.put("/update_read_status/")
async def update_read_status(query: str, read_status: bool, session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        from sqlalchemy import or_
        
        conditions:List[Any] =  []
        
        # Try to convert to int for ID comparison
        try:
            id_query = int(query)
            conditions.append(Book.id == id_query)
        except ValueError:
            # If conversion fails, don't add ID condition
            pass
            
        # Add text search conditions
        conditions.append(func.lower(Book.title).like(func.lower(f"%{query}%")))
        conditions.append(func.lower(Book.author).like(func.lower(f"%{query}%")))
        
        # Combine all conditions with or_()
        search_condition = or_(*conditions)
        
        result = await session.execute(select(Book).where(search_condition))
        book = result.scalars().first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found 🚫")
        book.read_status = read_status
        # await session.commit()
        # await session.refresh(book)
        await session.commit()
        return {"message": "Book Read Status Updated ✅", "book": book}

# Delete Book by ID, Title, or Author

@app.delete("/delete_book/")
async def delete_book(query: str, session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        from sqlalchemy import or_
        
        conditions:List[Any] = []
        
        # Try to convert to int for ID comparison
        try:
            id_query = int(query)
            conditions.append(Book.id == id_query)
        except ValueError:
            # If conversion fails, don't add ID condition
            pass
            
        # Add text search conditions
        conditions.append(func.lower(Book.title).like(func.lower(f"%{query}%")))
        conditions.append(func.lower(Book.author).like(func.lower(f"%{query}%")))
        
        # Combine all conditions with or_()
        search_condition = or_(*conditions)
        
        result = await session.execute(select(Book).where(search_condition))
        book = result.scalars().first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found 🚫")
        await session.delete(book)
        await session.commit()
        return {"message": "Book Deleted 🗑️ Successfully ✅"}


# Book Statistics
@app.get("/book_statistics/")
async def get_book_statistics(session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        result = await session.execute(select(Book))
        books = result.scalars().all()
        total_books = len(books)
        read_books = sum(1 for book in books if book.read_status)
        read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
        return {
            "total_books": total_books,
            "read_books": read_books,
            "unread_books": total_books - read_books,
            "read_percentage": f"{read_percentage:.2f}%"
        }


# from fastapi import FastAPI, Depends, HTTPException, Query
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlmodel import select
# from database import get_async_session
# from sqlalchemy import op
# from fastapi.middleware.cors import CORSMiddleware
# from model import Book

# app = FastAPI()

# # Middleware for CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Add a new Book
# @app.post("/add_book/")
# async def create_book(title: str, author: str, genre: str, publication_year: int, session: AsyncSession = Depends(get_async_session)):
#     book = Book(title=title, author=author, genre=genre, publication_year=publication_year)
#     session.add(book)
#     await session.commit()
#     await session.refresh(book)
#     return {"message": "Book created ✅", "book": book}

# # Get All Books
# @app.get("/get_books/")
# async def get_books(session: AsyncSession = Depends(get_async_session)):
#     async with session.begin():
#         result = await session.execute(select(Book))
#         books = result.scalars().all()
#         return books

# # Search Book by ID, Title, or Author
# @app.get("/search_books/")
# async def search_books(query: str = Query(...), session: AsyncSession = Depends(get_async_session)):
#     async with session.begin():
#         result = await session.execute(select(Book).where((Book.id == query) | (op(Book.title).ilike(f"%{query}%")) | (op(Book.author).ilike(f"%{query}%"))))
#         books = result.scalars().all()
#         if not books:
#             raise HTTPException(status_code=404, detail="No matching books found 🚫")
#         return books


# # Update Read Status by ID, Title, or Author
# @app.put("/update_read_status/")
# async def update_read_status(query: str, read_status: bool, session: AsyncSession = Depends(get_async_session)):
#     async with session.begin():
#         result = await session.execute(select(Book).where((Book.id == query) |(op(Book.title).ilike(f"%{query}%")) | (op(Book.author).ilike(f"%{query}%"))))
#         book = result.scalars().first()
#         if not book:
#             raise HTTPException(status_code=404, detail="Book not found 🚫")
#         book.read_status = read_status
#         await session.commit()
#         await session.refresh(book)
#         return {"message": "Book Read Status Updated ✅", "book": book}

# # Delete Book by ID, Title, or Author
# @app.delete("/delete_book/")
# async def delete_book(query: str, session: AsyncSession = Depends(get_async_session)):
#     async with session.begin():
#         result = await session.execute(select(Book).where((Book.id == query) | (op(Book.title).ilike(f"%{query}%")) | (op(Book.author).ilike(f"%{query}%"))))
#         book = result.scalars().first()
#         if not book:
#             raise HTTPException(status_code=404, detail="Book not found 🚫")
#         await session.delete(book)
#         await session.commit()
#         return {"message": "Book Deleted 🗑️ Successfully ✅"}

# # Book Statistics
# @app.get("/book_statistics/")
# async def get_book_statistics(session: AsyncSession = Depends(get_async_session)):
#     async with session.begin():
#         result = await session.execute(select(Book))
#         books = result.scalars().all()
#         total_books = len(books)
#         read_books = sum(1 for book in books if book.read_status)
#         read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
#         return {
#             "total_books": total_books,
#             "read_books": read_books,
#             "unread_books": total_books - read_books,
#             "read_percentage": f"{read_percentage:.2f}%"
#         }







# from fastapi import FastAPI, Depends, HTTPException
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlmodel import select
# from database import get_async_session
# from fastapi.middleware.cors import CORSMiddleware
# from model import Book

# app = FastAPI()

# # Middleware for CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# #  Add a new Book  Endpoint
# @app.post("/add_book/")
# async def create_book(title: str, author: str, genre: str, publication_year: int, session: AsyncSession = Depends(get_async_session)):
#     book = Book(title=title, author=author, genre=genre, publication_year=publication_year)
#     session.add(book)
#     await session.commit()
#     await session.refresh(book)
#     return {"message": "Book created ✅", "book": book}

# #  Get All Books Endpoint
# @app.get("/get_books/")
# async def get_books(session: AsyncSession = Depends(get_async_session)):
#     async with session.begin():
#         result = await session.execute(select(Book))
#         books = result.scalars().all()
#         return books

# # Get a Specific Book Endpoint
# @app.get("/get_book/{book_id}")
# async def get_specific_book(book_id: str, session: AsyncSession = Depends(get_async_session)):
#     async with session.begin():
#         result = await session.execute(select(Book).where(Book.id == book_id))
#         book = result.scalars().first()
#         if not book:
#             raise HTTPException(status_code=404, detail="Book not found 🚫")
#         return book

# # Update Read Status Endpoint
# @app.put("/update_read_status/{book_id}")
# async def update_book_status(book_id: str, read_status: bool, session: AsyncSession = Depends(get_async_session)):
#     async with session.begin():
#         result = await session.execute(select(Book).where(Book.id == book_id))
#         book = result.scalars().first()
#         if not book:
#             raise HTTPException(status_code=404, detail="Book not found 🚫")
#         book.read_status = read_status
#         await session.commit()
#         await session.refresh(book)
#         return {"message": "Book Read Status Updated ✅", "book_id": book_id}

# #  Delete Book  Endpoint
# @app.delete("/delete_book/{book_id}")
# async def delete_book(book_id: str, session: AsyncSession = Depends(get_async_session)):
#     async with session.begin():
#         result = await session.execute(select(Book).where(Book.id == book_id))
#         book = result.scalars().first()
#         if not book:
#             raise HTTPException(status_code=404, detail="Book not found")
#         await session.delete(book)
#         await session.commit()
#         return {"message": "Book Deleted 🗑️ Successfully ✅", "book_id": book_id}

# #  Book Statistics Endpoint
# @app.get("/book_statistics/")
# async def get_book_statistics(session: AsyncSession = Depends(get_async_session)):
#     async with session.begin():
#         result = await session.execute(select(Book))
#         books = result.scalars().all()

#         total_books = len(books)
#         read_books = sum(1 for book in books if book.read_status)
#         read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0

#         return {
#             "total_books": total_books,
#             "read_books": read_books,
#             "unread_books": total_books - read_books,
#             "read_percentage": f"{read_percentage:.2f}%"
#         }

















