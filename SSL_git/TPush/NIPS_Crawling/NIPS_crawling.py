import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


# 연도 별 페이지 추출
root_url = "https://proceedings.neurips.cc"
page = requests.get(root_url)
soup = bs(page.text,"html.parser")

year_elements = soup.select('div.col-sm a')

year = []
links = []

for index,element in enumerate(year_elements,1):
    if index == 3:
        break;
    year.append(element.text)
    links.append(root_url+element.attrs['href'])
    
    
year_df = pd.DataFrame()
year_df['year'] = year
year_df['links'] = links

year_df.to_csv('./temp/NIPS_year_link.csv')

# 논문 이름 추출
link_list = year_df['links'].tolist()    

paper = pd.DataFrame()
paper_name = []
paper_links = []

for l in link_list:
    year_url = l
    print(l)
    page = requests.get(year_url)
    soup = bs(page.text,"html.parser")
    
    paper_list = soup.select('div.col a')
    
    #paper_df = pd.DataFrame()
    
    for element in paper_list:
        paper_name.append(element.text)
        paper_links.append(root_url+element.attrs['href'])
        
    
paper['paper_name'] = (paper_name)
paper['paper_links'] = (paper_links)
paper = paper[1:]
paper.to_csv('./temp/NIPS_paper_link.csv')


# 논문 별 정보 추출
paper_list_link = paper['paper_links'].tolist() 

paper_info = pd.DataFrame()

title_list = []
author_list = []
abstract_list = []
cnt = 0
for pl in paper_list_link:
    paper_url = pl
    page = requests.get(paper_url)
    soup = bs(page.text,"html.parser")
    
    title = soup.select('div.col h4')[0].get_text() # 1번째 h4
    author = soup.select('div.col p i')[0].get_text()
    
    if len(soup.select('div.col p'))>3:
        abstract = soup.select('div.col p')[3].get_text()
    else:
        abstract = soup.select('div.col p')[2].get_text()
    
    cnt+=1
    # print(len(soup.select('div.col p')))
    print(cnt,'/',len(paper_list_link))
    
    title_list.append(title)
    author_list.append(author)
    abstract_list.append(abstract)
    
paper_info['title'] = title_list
paper_info['author'] = author_list
paper_info['abstract'] = abstract_list
paper_info.to_csv('./temp/NIPS_paper_info.csv')
    
    
    


