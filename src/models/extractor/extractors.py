import lxml.html

# Extractor for 2019 version of the game
def extract_words_v1(text):
    results_html = lxml.html.fromstring(text)
    
    words = {}
    score_board = results_html.cssselect("div.points-result")
    if not score_board:
        return words

    rows = score_board[0]

    for row in rows:
        word = row.cssselect("div.word")[0].text_content().lower()
        points = int(row.cssselect("div.points")[0].cssselect("div.left")[0].text_content())
        words[word] = points
    
    return words

# Extractor for 2020 version of the game
def extract_words_v2(text):
    html = lxml.html.fromstring(text)

    words = []
    rows = html.cssselect("div.duel-result-row")
    for row in rows:
        word = row.cssselect("div.word")
        if len(word) == 0:
            continue
        word = word[0].text_content().lower()
        word = word.strip()
        words.append(word)

    return words
    