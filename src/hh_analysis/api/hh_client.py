import requests
from typing import Any
from bs4 import BeautifulSoup

from hh_analysis.config.settings import HH_API_BASE_URL, REQUEST_TIMEOUT
from datetime import datetime


def get_areas() -> list:
    """Fetch HH areas reference."""
    response = requests.get(f"{HH_API_BASE_URL}/areas", timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()

def get_indusries() -> list:
    """ Функция возвращает список отраслей"""
    responce = requests.get(f"{HH_API_BASE_URL}/industries", timeout=REQUEST_TIMEOUT)
    responce.reise_for_status()
    return responce.json()


def get_vacancies_page(
    text: str,
    area: int | None = None,
    page: int = 0,
    per_page: int = 100,
    period: int | None = None,
    only_with_salary: bool = False,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> dict[str, Any]:
    """
    Fetch one page of vacancies from HH API.

    Args:
        text: Search query, for example "data engineer".
        area: HH area id.
        page: Page number, starts from 0.
        per_page: Number of items per page. HH usually allows up to 100.
        period: Search period in days, for example 1, 3, 7, 30.
        only_with_salary: If True, request only vacancies with salary specified.

    Returns:
        Parsed JSON response from HH API.
    """
    params: dict[str, Any] = {
        "text": text,
        "page": page,
        "per_page": per_page,        
    }

    if area is not None:
        params["area"] = area

    if period is not None and date_from is None and date_to is None:
        params["period"] = period

    if only_with_salary:
        params["only_with_salary"] = "true"

    if date_from is not None and date_to is not None and period is None:
        params["date_from"] = date_from.isoformat()
        params["date_to"] = date_to.isoformat()
     


    '''
    headers = {
    "User-Agent": "hh-analysis/1.0 (kosoukhovsa@gmail.com)"
    }
    '''

    response = requests.get(
        f"{HH_API_BASE_URL}/vacancies",
        params=params,        
        timeout=REQUEST_TIMEOUT,
        #headers=headers,
    )
    response.raise_for_status()
    return response.json()

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n")


def get_vacancy_detail(vacancy_id: int | str) -> dict[str, Any]:
    """
    Fetch detailed vacancy information from HH API.

    Args:
        vacancy_id: HH vacancy id.

    Returns:
        Parsed JSON response with detailed vacancy data.
    """
    response = requests.get(
        f"{HH_API_BASE_URL}/vacancies/{vacancy_id}",
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()

def get_employer_detail(employer_id: int | str) -> dict[str, Any]:
    """
    Загрузка детальных данных по работодателю
    """
    response = requests.get(
        f"{HH_API_BASE_URL}/employers/{employer_id}",
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


