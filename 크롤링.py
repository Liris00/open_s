from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random
import re
import os
from datetime import datetime

def extract_number_from_help_text(help_text):
    if not help_text:
        return 0
    numbers = re.findall(r'\d+', help_text)
    return int(numbers[0]) if numbers else 0

def safe_get_text(element, selector, default=""):
    try:
        text = element.find_element(By.CSS_SELECTOR, selector).text
        return text if text.strip() else "제목없음"
    except:
        return default

def get_unique_filename(base_filename):
    counter = 1
    filename = base_filename
    while os.path.exists(filename):
        name, ext = os.path.splitext(base_filename)
        filename = f"{name}_{counter}{ext}"
        counter += 1
    return filename

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--disable-blink-features=AutomationControlled') # 중요 설정 자동화 탐지 방지
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--enable-unsafe-swiftshader')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)

start_time = time.time()



#https://www.coupang.com/vp/products/6870487256 무선충전기 
#908개 리뷰
# https://www.coupang.com/vp/products/8082654809?itemId=22798183173&vendorItemId=89833126170&q=%EB%AC%B4%EC%84%A0+%EC%9D%B4%EC%96%B4%ED%8F%B0&itemsCount=36&searchId=e3c129b3440047ce8da60b7208b0608d&rank=1&searchRank=1&isAddedCart=  무선이어폰
#1469개 리뷰
#https://www.coupang.com/vp/products/6641056251?itemId=15181053236&vendorItemId=82402320512&q=%ED%99%94%EC%9E%A5%ED%92%88&itemsCount=36&searchId=115a933c68134862ac804700ea52e501&rank=0&searchRank=0&isAddedCart=      화장품
#1022개 리뷰
#https://www.coupang.com/vp/products/6137107889?itemId=11744003733&vendorItemId=79017906112&pickType=COU_PICK&q=%ED%99%94%EC%9E%A5%ED%92%88&itemsCount=36&searchId=115a933c68134862ac804700ea52e501&rank=10&searchRank=10&isAddedCart=     화장품
#1650개 리뷰
#https://www.coupang.com/vp/products/7937124717?itemId=21849951719&vendorItemId=86420134711&pickType=COU_PICK&q=%EB%A7%88%EC%82%AC%EC%A7%80%EA%B1%B4&itemsCount=36&searchId=96bfe70a38ca4e67af60cdc377963180&rank=0&searchRank=0&isAddedCart=    마사지건
#557개 리뷰
#https://www.coupang.com/vp/products/1459597335?itemId=2511514635&vendorItemId=70504555828&pickType=COU_PICK&q=%EC%97%90%EC%96%B4%ED%94%84%EB%9D%BC%EC%9D%B4%EA%B8%B0&itemsCount=36&searchId=37050a981adb4d7893cd7aac42b5e6b3&rank=1&searchRank=1&isAddedCart=    애어프라이기
#842개 리뷰
#http://coupang.com/vp/products/7830644825?itemId=15642964239&searchId=6f0ba64d11ce41f8b588be90ee6d0d88&sourceType=brandstore_sdp_atf-all_products&storeId=70649&subSourceType=brandstore_sdp_atf-all_products&vendorId=C00332039&vendorItemId=82859025129 운동화(중국 직구)
#187개 리뷰
#https://www.coupang.com/vp/products/8145067451?itemId=19848126302&vendorItemId=70778258892&pickType=COU_PICK&q=%EB%A1%9C%EC%A7%80%ED%85%8D+g102&itemsCount=36&searchId=e8c1751f017342d9ba475955c0aa7829&rank=0&searchRank=0&isAddedCart=  마우스
#1650개 리뷰
#https://www.coupang.com/vp/products/153770361?itemId=20316107081&vendorItemId=3939959153&sourceType=srp_product_ads&clickEventId=f7714460-b519-11ef-94a3-174913c9fb17&korePlacement=15&koreSubPlacement=1&q=%EC%8B%9D%ED%92%88&itemsCount=36&searchId=dbe1ed3f46b6429797b193ea29a663d9&rank=0&searchRank=0&isAddedCart=   식품 귤
#1650개 리뷰
#https://www.coupang.com/vp/products/6047099050?itemId=11072516037&vendorItemId=78351988633&q=%EC%98%B7&itemsCount=36&searchId=0f7b88bde6204b188a01ce2d84c46ccf&rank=1&searchRank=1&isAddedCart=    옷
#301개 리뷰
#https://www.coupang.com/vp/products/7913373530?itemId=21720000237&vendorItemId=88146647233&q=%EB%B7%B0%EB%94%94%EC%95%84%EB%8B%88&itemsCount=36&searchId=134f0005154443b9a2286aab7a49d176&rank=0&searchRank=0&isAddedCart=   화장품
#1649개 리뷰




try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver,15)  # 대기 시간 5초로 단축
    reviews_data = []
    max_reviews = 4000
    empty_review_count = 0
    MAX_EMPTY_REVIEWS =50

    driver.get("https://www.coupang.com/vp/products/7913373530?itemId=21720000237&vendorItemId=88146647233&q=%EB%B7%B0%EB%94%94%EC%95%84%EB%8B%88&itemsCount=36&searchId=134f0005154443b9a2286aab7a49d176&rank=0&searchRank=0&isAddedCart=")   # 크롤링할 URL 입력
    time.sleep(2)  # 초기 로딩 대기 시간 단축

    current_page = 1
    while len(reviews_data) < max_reviews:
        try:
            driver.execute_script("window.scrollBy(0, 800)")
            time.sleep(1)  # 스크롤 대기 시간 단축

            

            

            reviews = wait.until(EC.presence_of_all_elements_located((
                By.XPATH, "//article[contains(@class, 'sdp-review__article__list')]"
            )))

            if not reviews:
                print("더 이상 리뷰가 없습니다.")
                break

            for review in reviews:
                if len(reviews_data) >= max_reviews:
                    break

                try:
                    content = safe_get_text(review, "div.sdp-review__article__list__review__content", "")
                    
                    if not content.strip():
                        empty_review_count += 1
                        if empty_review_count >= MAX_EMPTY_REVIEWS:
                            print(f"내용 없는 리뷰가 {empty_review_count}개 이상 연속 발견되어 크롤링을 종료합니다.")
                            break
                        continue
                    
                    empty_review_count = 0

                    title = safe_get_text(review, "div.sdp-review__article__list__headline", "제목없음")
                    
                    try:
                        rating_element = review.find_element(By.CSS_SELECTOR, "div.sdp-review__article__list__info__product-info__star-orange")
                        rating_text = rating_element.get_attribute("style")
                        rating = float(rating_text.split("width: ")[1].split("%")[0]) / 20
                    except:
                        rating = 0

                    author = safe_get_text(review, "span.sdp-review__article__list__info__user__name", "알 수 없음")
                    date = safe_get_text(review, "div.sdp-review__article__list__info__product-info__reg-date", "")

                    try:
                        help_text = review.find_element(By.CSS_SELECTOR, "div.sdp-review__article__list__help").text
                        helpful_count = extract_number_from_help_text(help_text)
                    except:
                        helpful_count = 0

                    reviews_data.append({
                        "작성자ID": author,
                        "제목": title,
                        "내용": content,
                        "별점": rating,
                        "작성일": date,
                        "추천수": helpful_count
                    })

                except Exception as e:
                    print(f"리뷰 데이터 추출 중 오류: {str(e)}")
                    continue
            

            

            print(f"현재 {len(reviews_data)}개의 리뷰 수집 완료 (페이지: {current_page})")

            # 현재 페이지의 모든 숫자 버튼 찾기
            page_buttons =driver.find_elements(By.CSS_SELECTOR, "button.sdp-review__article__page__num")
            
            # 현재 페이지 버튼 클릭
            clicked = False
            for button in page_buttons:
                if button.text.strip() == str(current_page):
                    button.click()
                    clicked = True
                    time.sleep(random.uniform(0.1,0.3))  # 클릭 후 대기 시간 단축
                    break

            if not clicked:
                # 다음 페이지 그룹으로 이동
                next_button = wait.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, "button.sdp-review__article__page__next"
                )))
                next_button.click()
                time.sleep(0.1)
                current_page = current_page
                continue
            
            if empty_review_count >= MAX_EMPTY_REVIEWS:
                break
                
            current_page += 1

        except TimeoutException:
            print("페이지 로딩 시간 초과")
            break
        except Exception as e:
            print(f"페이지 처리 중 오류: {str(e)}")
            break

except Exception as e:
    print(f"크롤링 중 오류 발생: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
    
    if reviews_data:
        base_filename = "coupang_reviews.csv"
        final_filename = get_unique_filename(base_filename)
        df = pd.DataFrame(reviews_data)
        df.to_csv(final_filename, index=False, encoding="utf-8-sig")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print("\n크롤링 완료!")
        print(f"총 수집된 리뷰 수: {len(reviews_data)}개")
        print(f"실행 시간: {execution_time:.2f}초")
        print(f"저장된 파일명: {final_filename}")