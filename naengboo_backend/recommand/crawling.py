import requests
from bs4 import BeautifulSoup
import time
import csv

def get_recipe_links(page):
    """
    지정된 페이지에서 레시피 상세 페이지의 링크를 추출합니다.
    """
    base_url = "https://www.10000recipe.com"
    list_url = f"{base_url}/recipe/list.html?order=reco&page={page}"
    recipe_links = []

    try:
        resp = requests.get(list_url, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 레시피 목록은 <li class="common_sp_list_li"> 형태로 감싸져 있음
        recipe_items = soup.select("li.common_sp_list_li")
        for item in recipe_items:
            link_tag = item.select_one("a.common_sp_link")
            if link_tag:
                recipe_links.append(base_url + link_tag.get("href"))
    except Exception as e:
        print(f"[get_recipe_links] 페이지 {page} 크롤링 중 오류: {e}")

    return recipe_links

def parse_recipe_detail(url):
    """
    레시피 상세 페이지에 접속해 '요리 이름', '재료', '양념' 등을 파싱합니다.
    """
    result = {
        "url": url,
        "title": None,
        "ingredients": [],
        "seasonings": []
    }
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 1) 레시피 제목 파싱
        title_tag = soup.select_one("div.view2_summary h3")
        if title_tag:
            result["title"] = title_tag.get_text(strip=True)

        # 2) 재료/양념 파싱
        #   기존처럼 <div class="ready_ingre3">가 여러 개 있을 수 있음
        ingre_sections = soup.select("div.ready_ingre3")
        if ingre_sections:
            for idx, section in enumerate(ingre_sections):
                # 예: 0번 인덱스 → 주재료, 1번 인덱스 → 양념(부재료)
                li_tags = section.select("ul li")
                
                for li in li_tags:
                    # ⓐ 이름 부분: div.ingre_list_name a 만 추출
                    name_tag = li.select_one("div.ingre_list_name a")
                    # ⓑ 양이나 기타 정보는 무시 (원한다면 div.ingre_list_ea 등으로 따로 파싱 가능)
                    
                    # ⓐ에서 텍스트만 추출
                    name_text = name_tag.get_text(strip=True) if name_tag else ""
                    
                    # 내용이 없으면 건너뛰기
                    if not name_text:
                        continue
                    
                    # idx == 0 → 주재료, idx != 0 → 양념
                    if idx == 0:
                        result["ingredients"].append(name_text)
                    else:
                        result["seasonings"].append(name_text)

    except Exception as e:
        print(f"[parse_recipe_detail] 상세 페이지 크롤링 중 오류: {e}")

    return result


def main():
    # 테스트를 위해 1~5페이지만 크롤링 (전체 6015페이지는 실행 시 부담이 큽니다)
    start_page = 1
    end_page = 13

    all_recipes = []

    for page in range(start_page, end_page + 1):
        print(f"===== {page}페이지 처리 중 =====")
        
        recipe_links = get_recipe_links(page)
        print(f" - 레시피 링크 {len(recipe_links)}개 발견")

        for link in recipe_links:
            detail = parse_recipe_detail(link)
            all_recipes.append(detail)

        # 서버 과부하 방지를 위해 잠시 대기
        time.sleep(0.2)

    # CSV 파일로 저장 (seasonings 컬럼 없이)
    with open("new_recipes.csv", "w", encoding="utf-8-sig", newline="") as f:
        fieldnames = ["url", "title", "ingredients"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for recipe in all_recipes:
            row = {
                "url": recipe.get("url", ""),
                "title": recipe.get("title", ""),
                "ingredients": ", ".join(recipe.get("ingredients", []))
            }
            writer.writerow(row)

    print(f"\n크롤링 완료! 총 {len(all_recipes)}개의 레시피를 수집했습니다.")
    print("결과는 new_recipes.csv 파일로 저장되었습니다.")

if __name__ == "__main__":
    main()
