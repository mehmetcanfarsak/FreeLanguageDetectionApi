from fastapi import FastAPI, Query
from typing import Union, List

from pydantic import BaseModel, Field
import markdown2
from fastapi.responses import HTMLResponse, JSONResponse
from langdetect import detect_langs

app = FastAPI()


class LanguageProbabilityClass(BaseModel):
    lang: str
    prob: float


class LanguageResult(BaseModel):
    most_probable_language: Union[str, None]
    probable_languages: List[LanguageProbabilityClass]
    text: str


class TextToDetectModel(BaseModel):
    text_to_detect_language: str = Field(description="For high accuracy please write at least 3 words",default="how are you")


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
def root():
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()
    return markdown2.markdown(readme_content)


@app.get("/detect_language", response_model=LanguageResult,
         description="Returns probabilties of possible languages and most probable language")
def detect_language_from_query(
        text_to_detect_language: str = Query(description="For high accuracy please write at least 3 words",default="how are you")):
    detection_result = detect_langs(text_to_detect_language)
    if (len(detection_result) > 0):
        probable_languages = []
        for probable_language in detection_result:
            probable_languages.append({"lang": probable_language.lang, "prob": probable_language.prob})
        return {"most_probable_language": detection_result[0].lang, "probable_languages": probable_languages,"text":text_to_detect_language}
    return LanguageResult()


@app.post("/detect_language", response_model=LanguageResult,
          description="Returns probabilties of possible languages and most probable language. For high accuracy please write at least 3 words")
def detect_language_from_query(texttodetect: TextToDetectModel):
    detection_result = detect_langs(texttodetect.text_to_detect_language)
    if (len(detection_result) > 0):
        probable_languages = []
        for probable_language in detection_result:
            probable_languages.append({"lang": probable_language.lang, "prob": probable_language.prob})
        return {"most_probable_language": detection_result[0].lang, "probable_languages": probable_languages,"text":texttodetect.text_to_detect_language}
    return LanguageResult()


@app.get("/get_list_of_languages", response_class=JSONResponse, description="Get all available languages list.")
def get_list_of_languages():
    return ["af", "ar", "bg", "bn", "ca", "cs", "cy", "da", "de", "el", "en", "es", "et", "fa", "fi, fr, gu, he",
            "hi", "hr", "hu", "id", "it", "ja", "kn", "ko", "lt", "lv", "mk", "ml", "mr", "ne", "nl", "no", "pa", "pl",
            "pt", "ro", "ru", "sk", "sl", "so", "sq", "sv", "sw", "ta", "te", "th", "tl", "tr", "uk", "ur", "vi",
            "zh-cn", "zh-tw"]
