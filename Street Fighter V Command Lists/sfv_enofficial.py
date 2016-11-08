import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

# r = Response，讀取網頁的回應
# 這裡讀取的是所有角色列表的頁面
r = urllib.request.urlopen("http://streetfighter.com/characters/")

# html，讀取網頁原始碼
html = r.read().decode('utf-8')

# s = BeautifulSoup，轉換為 BeautifulSoup 物件
s = BeautifulSoup(html, "html5lib")

# 擷取所有角色頁面的網址，並 append 進 character_list
character_list = []
for tag in s.find_all("figcaption", { "class" : "portrait"}):
    character_list.append(tag.a.attrs['href'])

print(character_list)

# 擷取各個角色的招式表內容
for page in character_list:
    # r = Response，讀取網頁的回應
    # 這裡讀取的是各個角色的頁面
    r = urllib.request.urlopen(page)

    # html，讀取網頁原始碼
    html = r.read().decode('utf-8')

    # s = BeautifulSoup，轉換為 BeautifulSoup 物件
    s = BeautifulSoup(html, "html5lib")

    # filename，檔名使用該頁面的角色名稱
    filename = s.find("h1", { "class" : "entry-title" }).text

    # 測試
    print(filename)

    # find div.movelist-container，資料為角色的招式表
    fdata = s.find("div", { "class" : "movelist-container"} )  # bs4.element.Tag

    shortcode_bracket_left = "{{< sfv-"
    shortcode_bracket_right = " >}}"

    # 完整招式表
    command_list = []

    # 設定 recursive=False（不會繼續輪詢），取得 fdata 裡，所有第一層的 Tag
    # 再判斷有沒有特定的 class
    for tag in fdata.find_all(["h5", "div"], recursive=False):
        # 如果 tag.name == "h5"，這個 Tag 就是一種招式類別的標題
        # 把招式類型 (command_type) 寫為 tag.strong.text
        # 在讀取到下一個招式類型以前，所有的招式都套用這個類型
        if tag.name == "h5" :
            command_type = tag.text
        # 如果 tag.name == "div"，這個 Tag 就是招式
        elif tag.name == "div":
            # 確認 attribute "class" 裡面有 "move-container" 這個 value
            if "move-container" in tag['class']:
                # 招式名稱，先存進 command_name_list，再 Join 成一個物件
                command_name_list = []
                command_name_list.append(tag.find("div", { "class" : "move-name" }).strong.text)
                # 如果發現 Ex 的圖示，就加上 shortcode_bracket_left & right，再 append
                if (tag.find("div", { "class" : "move-name" }).strong.find('i')):
                    command_name_list.append(shortcode_bracket_left + tag.find("div", { "class" : "move-name" }).strong.find('i')['class'][-1] + shortcode_bracket_right)
                command_name = (' ').join(command_name_list)
                # 招式指令，先存進 command_move_list Join 成一個物件
                command_move_list = []
                for child in tag.find("div", { "class" : "move-commands" }).p.children:
                    if str(type(child)) == "<class 'bs4.element.NavigableString'>":  # 如果只是文字的指令描述，就直接 append
                        command_move_list.append(child.title())
                    else:  # 如果是指令圖示，就加上 shortcode_bracket_left & right，再 append
                        if child.has_attr("class"):  # 確定 Tag 裡有 "Class" 這個 Attribute
                                                     # 以免遇到像 <br> 這種 Tag 會出錯
                            command_move_list.append(shortcode_bracket_left + child['class'][-1] + shortcode_bracket_right)
                command_move = ('').join(command_move_list)

                command_list_row = []  # 一行招式，內容為 [command_type ,command_name, command_move]
                command_list_row.append(command_type)
                command_list_row.append(command_name)
                command_list_row.append(command_move)
                command_list.append(command_list_row)
    
    command_list_df = pd.DataFrame(command_list, dtype='object', columns=["Command Type", "Command Name", "Command Move"])
    command_list_df.to_csv("./csv/" filename + ".csv", index=False)


# [TODO] 看要不要改用 Requests 取代 urllib
# requests.get("http://...").text
