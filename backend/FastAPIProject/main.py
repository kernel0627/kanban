from fastapi import FastAPI , Depends , HTTPException , status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models , schemas  , hashing  , jwt_handler
from database import  engine , get_db
from oauth2 import get_current_user
from typing import List
from fastapi.middleware.cors import CORSMiddleware

def get_list_for_current_user(
        list_id: int ,
        db: Session = Depends(get_db) ,
        current_user : models.User = Depends(get_current_user),
) -> models.List:
    lst = db.query(models.List).get(list_id)
    if not lst:
        raise HTTPException(status_code=404, detail="List not found or access denied")
    board = db.query(models.Board).filter(models.Board.id == lst.board_id , models.Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=403, detail="Access denied")
    return lst


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kanbango API",
    description="A simple Kanban board API built with FastAPI and SQLAlchemy.",
    version="1.0.0",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)


@app.get("/")
async def root():
    return {"msg":"fine"}


@app.post("/api/register"  , response_model=schemas.User , status_code = status.HTTP_201_CREATED)
async def register(request : schemas.UserCreate , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user :
        raise HTTPException(status_code=409 , detail='Email already registered')

    new_user = models.User(
        username=request.username,
        email=request.email,
        hashed_password=hashing.Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/api/login', response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not hashing.Hash.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},  # 修正为 Bearer
            detail='Invalid Credentials'
        )
    access_token = jwt_handler.create_access_token(
        data={'sub': user.email, 'id': user.id}
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get('/api/me' , response_model=schemas.User)
async def me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@app.post('/api/boards' , response_model=schemas.Boards , status_code=status.HTTP_201_CREATED , tags=["Boards"])
async def create_board( request : schemas.BoardCreate , db: Session = Depends(get_db) , current_user: models.User = Depends(get_current_user)):
    new_board = models.Board(
        title=request.title,
        user_id=current_user.id
    )
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

@app.get("/api/boards" , response_model=List[schemas.Boards] , tags=["Boards"])
async def get_boards(db:Session = Depends(get_db) , current_user: models.User = Depends(get_current_user)):
    boards = db.query(models.Board).filter(models.Board.user_id == current_user.id).all()
    return boards

@app.get("/api/boards/{board_id}", response_model=schemas.Boards, tags=['Boards'])
async def get_board(board_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found or access denied")
    return board

@app.put('/api/boards/{board_id}' , response_model=schemas.Boards , tags=['Boards'])
async def  update_board(board_id:int , request: schemas.BoardCreate , db :Session = Depends(get_db) , current_user: models.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id , models.Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404 , detail = "Board not found or access denied")
    board.title = request.title
    db.commit()
    db.refresh(board)
    return board

@app.delete('/api/boards/{board_id}' , status_code=status.HTTP_204_NO_CONTENT , tags=["Boards"] )
async def delete_board(board_id : int , db: Session = Depends(get_db) , current_user: models.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id , models.Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404 , detail="Board not found or access denied")
    db.delete(board)
    db.commit()

@app.put("/api/boards/update_order" , tags=["Boards"])
async def update_board_structure(request : schemas.Boards , db:Session = Depends(get_db) , current_user: models.User = Depends(get_current_user)):
    board_from_db = db.query(models.Board).filter(models.Board.id == request.id , models.Board.user_id == current_user.id).first()
    if not board_from_db:
        raise HTTPException(status_code=404 , detail="Board not found or access denied")

    for list_index , list_data in enumerate(request.lists):
        list_from_db = db.query(models.List).get(list_data.id)
        if list_from_db and list_from_db.board_id == board_from_db.id :
            list_from_db.order  = list_index
            for card_index , card_data in enumerate(list_data.cards) :
                card_from_db  = db.query(models.Card) .get(card_data.id)
                if card_from_db:
                    card_from_db.list_id = list_from_db.id
                    card_from_db.order = card_index

    db.commit()
    return {'msg': "Board structure updated successfully"}

@app.post('/api/boards/{board_id}/lists' , response_model=schemas.Lists , status_code=status.HTTP_201_CREATED , tags=["Lists"])
async def create_list(board_id: int, request: schemas.ListCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail='Board not found or access denied')
    new_order = db.query(models.List).filter_by(board_id=board.id).count()  # 用数据库统计数量
    new_list = models.List(
        title=request.title,
        order=new_order,
        board_id=board.id
    )
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

@app.put('/api/lists/{list_id}' , response_model=schemas.Lists , tags=["Lists"])
async def update_list(list_id: int , request: schemas.ListCreate , db : Session = Depends(get_db) , current_user: models.User = Depends(get_current_user)):
    lst = db.query(models.List).get(list_id)
    if not lst :
        raise HTTPException(status_code=404 , detail="List not found or access denied")
    board = db.query(models.Board).filter(models.Board.user_id == current_user.id , models.Board.id == lst.board_id).first()
    if not board or lst.board_id != board.id:
        raise HTTPException(status_code=404 , detail="List not found or access denied")
    lst.title = request.title
    db.commit()
    db.refresh(lst)

    return lst

@app.delete('/api/lists/{list_id}' , status_code = status.HTTP_204_NO_CONTENT , tags = ['Lists'])
async def delete_list(list_id : int , db : Session = Depends(get_db) , current_user: models.User = Depends(get_current_user)):
    lst = db.query(models.List).get(list_id)
    if not lst :
        raise HTTPException(status_code=404 , detail="List not found or access denied")
    board = db.query(models.Board).filter(models.Board.id == lst.board_id , models.Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=403 , detail="Access denied")
    db.delete(lst)
    db.commit()

@app.post('/api/lists/{list_id}/cards' , response_model = schemas.Cards , status_code = status.HTTP_201_CREATED, tags = ['Cards'])
async def create_card(list_id: int, request: schemas.CardCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    lst = db.query(models.List).get(list_id)
    if not lst:
        raise HTTPException(status_code=404, detail="List not found or access denied")
    board = db.query(models.Board).filter(models.Board.id == lst.board_id, models.Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=403, detail="Access denied")
    new_order = db.query(models.Card).filter_by(list_id=lst.id).count()  # 用数据库统计数量
    new_card = models.Card(
        content=request.content,
        order=new_order,
        list_id=lst.id
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

@app.put('/api/cards/{card_id}' , response_model=schemas.Cards , tags=['Cards'])
async def update_card(card_id : int , request : schemas.CardCreate , db : Session = Depends(get_db) , current_user : models.User = Depends(get_current_user)):
    card = db.query(models.Card).get(card_id)
    if not card :
        raise HTTPException(status_code=404 , detail="Card not found or access denied")
    lst = db.query(models.List).get(card.list_id)
    board = db.query(models.Board).filter(models.Board.id == lst.board_id , models.Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=403 , detail="Access denied")
    card.content = request.content
    card.order = request.order
    db.commit()
    db.refresh(card)
    return card

@app.delete('/api/cards/{card_id}' , status_code=status.HTTP_204_NO_CONTENT , tags=['Cards'])
async def delete_card(card_id : int , db : Session = Depends(get_db) , current_user: models.User = Depends(get_current_user)):
    card = db.query(models.Card).get(card_id)
    if not card :
        raise HTTPException(status_code=404 , detail="Card not found or access denied")
    lst = db.query(models.List).get(card.list_id)
    board = db.query(models.Board).filter(models.Board.id == lst.board_id , models.Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=403 , detail="Access denied")
    db.delete(card)
    db.commit()
