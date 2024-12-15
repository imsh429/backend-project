import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

TECH_STACK_KEYWORDS = [
    "Java", "Python", "C++", "C#", "Django", "Flask", 
    "React", "Vue", "Angular", "Spring", "Node.js", 
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "SQL", "NoSQL"
]

def extract_tech_stack(sector_raw):
    """Extract tech stack and sector from raw sector string."""
    tech_stack = [tech for tech in TECH_STACK_KEYWORDS if tech in sector_raw]

    # Remove tech stack keywords from the sector string
    for tech in tech_stack:
        sector_raw = sector_raw.replace(tech, "").strip()

    # Remove unnecessary information like registration date
    sector_raw = re.sub(r'(수정일|등록일)\s\d{2}/\d{2}/\d{2}', '', sector_raw).strip()    

    # Create a list of sectors by splitting the remaining string
    sector_list = [s.strip() for s in sector_raw.split(",") if s.strip()]
    return tech_stack, sector_list


def crawl_saramin(keyword, pages=1, retries=3):
    seen_keys = set()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    job_data_list = []

    for page in range(1, pages + 1):
        url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page}"
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                job_listings = soup.select('.item_recruit')

                for job in job_listings:
                    try:
                        link = 'https://www.saramin.co.kr' + job.select_one('.job_tit a')['href']
                        company = job.select_one('.corp_name a').text.strip()
                        title = job.select_one('.job_tit a').text.strip()

                        unique_key = f"{title}-{company}-{link}"
                        if unique_key in seen_keys:
                            continue
                        seen_keys.add(unique_key)

                        conditions = job.select('.job_condition span')
                        location = conditions[0].text.strip() if len(conditions) > 0 else ''
                        experience = conditions[1].text.strip() if len(conditions) > 1 else ''
                        education = conditions[2].text.strip() if len(conditions) > 2 else ''
                        employment_type = conditions[3].text.strip() if len(conditions) > 3 else ''
                        salary = conditions[4].text.strip() if len(conditions) > 4 else ''
                        deadline = job.select_one('.job_date .date').text.strip()
                        job_sector = job.select_one('.job_sector')
                        sector_raw = job_sector.text.strip() if job_sector else ''
                        created_at_tag = job.select_one('.job_day')
                        created_at = created_at_tag.text.strip() if created_at_tag else ''

                        # Extract tech stack and sector list
                        tech_stack, sector_list = extract_tech_stack(sector_raw)

                        job_data_list.append({
                            'company': company,
                            'title': title,
                            'link': link,
                            'location': location,
                            'experience': experience,
                            'education': education,
                            'employment_type': employment_type,
                            'deadline': deadline,
                            'sector': sector_list,
                            'salary': salary,
                            'created_at': created_at,
                            'views': 0,  # 초기값 설정
                            'tech_stack': tech_stack
                        })
                    except AttributeError as e:
                        print(f"HTML 파싱 실패: {e}")
                        continue

                print(f"{page}페이지 크롤링 완료")
                time.sleep(2)
                break
            except requests.RequestException as e:
                print(f"페이지 요청 실패: {e}")
                if attempt < retries - 1:
                    print(f"재시도 {attempt + 1}/{retries}")
                    time.sleep(2)
                else:
                    print("최대 재시도 횟수 초과")
    return pd.DataFrame(job_data_list)


if __name__ == "__main__":
    df = crawl_saramin('개발', pages=5)
    df.to_csv('saramin_python.csv', index=False)
