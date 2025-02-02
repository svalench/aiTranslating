from typing import List, Literal
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, validator
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from transformers import MarianTokenizer, MarianMTModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
model_name = "Helsinki-NLP/opus-mt-tc-bible-big-mul-mul"
TOKENIZER = MarianTokenizer.from_pretrained(model_name)
MODEL = MarianMTModel.from_pretrained(model_name)

LANGS = ['eng', 'rus', 'ukr', 'fra', "kaz", "bel", "deu"]
template = """

"""

class Translate(BaseModel):
    text: str
    lang: Literal[*LANGS]

    @validator('lang')
    def lang_must_be_one_of(cls, v):
        allowed_langs = LANGS
        if v not in allowed_langs:
            raise ValueError(f"Language must be one of: {allowed_langs}")
        return v


class TranslateList(BaseModel):
    data: List[Translate]

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"LANGS": LANGS})

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(request=request, name="about.html", context={})


@app.get("/translate/{to_lang}/{text}")
async def translate_get(to_lang: str, text: str):
    return {"result": {text: translate_text([f">>{to_lang}<< {text}"])}}


@app.post("/translate")
def translate_post(data: TranslateList):
    return [i for i in translate_text([f">>{i.lang}<< {i.text}" for i in data.data])]


def translate_text(text):
    if not MODEL or not TOKENIZER: raise HTTPException(detail='Ошибка данных! не найдены предзагруженные модели', status_code=400)
    return [TOKENIZER.decode(t, skip_special_tokens=True) for t in MODEL.generate(**TOKENIZER(text, return_tensors="pt", padding=True))]
