import re, random, sqlite3, pymorphy2
morph = pymorphy2.MorphAnalyzer()


#finds an exiting joke (not really)
def bd_parse(character):
    character = re.sub('[^А-ЯЁёа-я]', '', character.lower())
    normalized = morph.parse(character)[0][2]
    anecdotes = []
    global c
    c.execute('SELECT * FROM catBanecdotes ORDER BY post_id')
    all_posts = c.fetchall()
    possible_options = len(c.fetchall())
    n = 0
    for post in all_posts:
        normalized_text = post[2]
        if normalized in normalized_text and normalized != '':
            post_id = post[0]
            anecdotes.append(post_id)
            n += 1
        else:
            n += 1
    if len(anecdotes) == 0:
        anecdote = 'извините, таких анекдотов нет...'
    else:
        c.execute('SELECT * FROM catBanecdotes WHERE post_id=?', (random.choice(anecdotes),))
        raw_anecdote = (c.fetchone()[1])
        stop_words = ['хуй', 'хуя', 'хер', 'хера', 'мудак']
        for word in stop_words:
            raw_anecdote = re.sub(word, 'МАЙ', raw_anecdote)
        anecdote = raw_anecdote
    return anecdote


# connects to db
def data_base():
    conn = sqlite3.connect('catBanecdotes.db', check_same_thread=False)
    global c
    c = conn.cursor()


def main():
    data_base()
    character = 'петька'
    bd_parse(character)


if __name__ == '__main__':
    main()

